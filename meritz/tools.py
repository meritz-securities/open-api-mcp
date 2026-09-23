"""MCP 도구 등록.

카테고리마다 도구 하나를 만든다. 각 도구는 `api_type` 으로 어느 API 를 부를지 정한다.
도구 설명에 그 카테고리의 API 목록을 실어, 모델이 목록을 따로 묻지 않아도 되게 한다.
"""
from __future__ import annotations

import functools
import json
from typing import Any, NoReturn

import anyio.to_thread
from fastmcp.exceptions import ToolError

from .catalog import Api, Catalog
from .client import ApiClient, MeritzError
from .safety import blocked, is_state_changing

CATEGORY_KO = {
    "account": "계좌", "domestic_market": "국내주식 시세", "trading": "주문",
    "forex": "환전", "reference": "기준정보", "overseas_market": "해외주식 시세",
}
# 카탈로그 카테고리 → 도구 이름
TOOL_OF = {
    "account": "meritz_account",
    "domestic_market": "meritz_market",
    # 해외 시세는 국내와 종목코드·거래소 코드 체계가 달라 한 도구에 섞으면
    # 모델이 국내 파라미터를 그대로 넣는다. 카테고리대로 따로 낸다.
    "overseas_market": "meritz_overseas_market",
    "trading": "meritz_trading",
    "forex": "meritz_forex",
    "reference": "meritz_reference",
}
# 도구를 일부러 만들지 않는 카테고리. 빠뜨린 것과 구분하려고 이유까지 적어 둔다.
NO_TOOL = {
    "oauth2": "토큰 발급·폐기는 클라이언트가 캐시로 관리한다. "
              "도구로 노출하면 revoke 가 호출돼 진행 중인 세션이 전부 끊긴다.",
    "realtime": "웹소켓은 요청·응답 모델이 달라 별도 경로로 다룬다.",
}
_META = frozenset({"api_type", "confirm", "confirm_token", "tr_cont", "tr_cont_key"})


def _truthy(v: Any) -> bool:
    return str(v).strip().lower() in ("1", "true", "y", "yes", "예")


def describe(api: Api, catalog: Catalog, verbose: bool = False) -> str:
    """API 한 건의 사용법.

    응답 필드 설명까지 전부 실으면 한 번에 30KB 가 넘어 대화 컨텍스트를
    몇 번 만에 소진한다. 호출에 필요한 것(요청 파라미터·주의사항)은 늘
    싣고, 응답 필드 설명은 verbose 로 요청할 때만 싣는다.
    """
    lines = [f"{api.name}  [{api.key}]",
             f"  {api['method']} {api.path}   TR {api['tr_id']}"]
    if api.get("tps"):
        lines[-1] += f"   TPS {api['tps']}"
    if is_state_changing(api):
        lines.append("  ⚠ 상태변경 — 먼저 그대로 호출해 미리보기를 받으십시오. "
                     "응답의 confirm_token 을 params 에 넣어 다시 불러야 전송됩니다.")

    if api.params:
        lines.append("  요청 파라미터")
        for p in api.params:
            mark = "필수" if p.get("required") else "선택"
            loc = p.get("location") or ""
            lines.append(f"    {p['name']:<24} {mark} {p.get('type','')} [{loc}] "
                         f"{p.get('name_ko') or ''}")
            if p.get("description"):
                d = " ".join(str(p["description"]).replace("<br/>", " ").split())
                lines.append(f"        {d[:200]}")

    # 응답 필드 설명이 없으면 결과가 숫자 뭉치로만 보인다. 카탈로그에 다 있다.
    res = [f for f in (api.get("response") or {}).get("body", [])
           if f["name"] not in ("data", "rsp_cd", "rsp_msg", "tr_cont", "tr_cont_key")]
    if res:
        lines.append(f"  응답 필드 ({len(res)}개)")
        for f in res:
            lines.append(f"    {f['name']:<24} {f.get('type','')} {f.get('name_ko') or ''}")
            if verbose and f.get("description"):
                d = " ".join(str(f["description"]).replace("<br/>", " ").split())
                lines.append(f"        {d[:200]}")
        if not verbose:
            lines.append("    (필드 설명을 보시려면 params 에 verbose=true 를 넣으십시오)")

    for fx in catalog.corrections_for(api.key):
        lines.append(f"  ⚠ 응답 처리 참고사항 — {fx['kind']}")
        if fx.get("working_example"):
            lines.append(f"      적용 예시: {fx['working_example']}")
        if fx.get("actual_parameter"):
            lines.append(f"      실제 파라미터명: {fx['actual_parameter']}")
        if fx.get("if_you_follow_the_portal"):
            lines.append(f"      일반적인 처리 방식으로 호출하면: {fx['if_you_follow_the_portal']}")
        if fx.get("workaround"):
            lines.append(f"      대응: {fx['workaround']}")

    ex = (api.get("example") or {}).get("request")
    if ex:
        lines.append("  요청 예시")
        lines += [f"    {ln}" for ln in str(ex).splitlines()]
    return "\n".join(lines)


def validate(api: Api, params: dict) -> list[str]:
    """명세와 어긋나는 점을 모아 돌려준다. 판정은 client 와 같은 것을 쓴다."""
    return ApiClient.validate(api, params)


def _fail(payload: dict) -> NoReturn:
    """실패를 MCP 오류(isError)로 올린다.

    ``{"ok": false}`` 를 정상 응답으로 돌려주면 프로토콜 수준에서는 성공이라
    호스트가 실패를 세거나 재시도를 판단할 근거가 없다. 사람이 읽을 한 줄을
    앞에 두고, 기계가 쓸 세부는 JSON 으로 함께 싣는다.
    """
    head = payload.get("message") or payload.get("error") or "요청을 처리하지 못했습니다."
    raise ToolError(f"{head}\n{json.dumps(payload, ensure_ascii=False, indent=2)}")


def register(mcp, catalog: Catalog, client: ApiClient, settings) -> list[str]:
    """카테고리별 도구를 등록하고 등록된 도구 이름을 돌려준다."""
    made = []
    for category, tool_name in TOOL_OF.items():
        apis = [a for a in catalog.by_category(category) if not a.is_websocket]
        if not apis:
            continue
        listing = "\n".join(
            f"  {a.key:<24} {a['method']:<5} {a.name}"
            + ("   ⚠ 상태변경" if is_state_changing(a) else "")
            for a in sorted(apis, key=lambda x: x.key))
        desc = (f"메리츠 Open API — {CATEGORY_KO.get(category, category)} ({len(apis)}건).\n"
                f"api_type 으로 호출할 API 를 고르고 params 에 파라미터를 넣습니다.\n"
                f"api_type='describe' 로 부르면 파라미터 설명을 돌려줍니다.\n\n{listing}")

        def make(category=category, apis=apis):
            names = {a.key for a in apis}

            async def run(api_type: str, params: dict | None = None) -> dict:
                params = dict(params or {})
                if api_type in ("describe", "list", "help"):
                    target = params.get("api_type")
                    if target and target in names:
                        return {"ok": True,
                                "detail": describe(catalog.get(target), catalog,
                                                   verbose=_truthy(params.get("verbose")))}
                    if target:
                        # 조용히 목록으로 되돌아가면 모델은 자기가 요청한 상세를
                        # 받았다고 착각한다. 못 찾았다는 사실을 말한다.
                        _fail({"ok": False, "error": "UNKNOWN_API_TYPE",
                               "message": f"이 도구에 '{target}' 은 없습니다. "
                                          f"아래 이름 중에서 고르십시오.",
                               "available": sorted(names)})
                    return {"ok": True, "apis": sorted(names),
                            "hint": "params={'api_type': '<이름>'} 으로 상세를 봅니다."}
                if api_type not in names:
                    _fail({"ok": False, "error": "UNKNOWN_API_TYPE",
                           "message": f"이 도구에 없는 api_type: {api_type}",
                           "available": sorted(names)})

                api = catalog.get(api_type)
                if settings.read_only and is_state_changing(api):
                    _fail(blocked(api))

                problems = validate(api, params)
                if problems:
                    # describe 전문을 실으면 오류 하나가 15KB 가 되어 대화
                    # 컨텍스트를 먹는다. 무엇이 잘못됐는지만 말하고, 전체는
                    # 필요할 때 describe 로 보게 한다.
                    _fail({"ok": False, "error": "INVALID_PARAMS",
                           "message": "; ".join(problems),
                           "problems": problems,
                           "hint": f"params={{'api_type': '{api_type}'}} 으로 "
                                   f"describe 를 부르면 전체 파라미터를 봅니다."})

                # 확인 게이트는 ApiClient.call() 안에 있다. 여기서 따로 부르지
                # 않는다 — 토큰은 1회용이라 두 번 검사하면 두 번째가 실패한다.
                # 끌 수 있는 스위치는 두지 않는다. 있으면 언젠가 그 상태로
                # 돌아가고, 그때 주문이 무확인으로 나간다.
                try:
                    # 동기 HTTP 를 코루틴에서 그대로 부르면 이벤트 루프가 멈춘다.
                    # HTTP 로 여러 클라이언트를 붙였을 때 한 사람의 느린 조회가
                    # 나머지 전원을 세운다.
                    return await anyio.to_thread.run_sync(
                        functools.partial(client.call, api, params))
                except MeritzError as e:
                    if e.code == "NEEDS_CONFIRMATION":
                        # 미리보기는 실패가 아니다. 모델이 사용자에게 보이고
                        # 동의를 받아 confirm_token 과 함께 다시 부르면 된다.
                        out = dict(e.body or {})
                        if params.get("confirm_token") or _truthy(params.get("confirm")):
                            out["rejected"] = str(e)
                        return out
                    _fail(e.as_dict())
                except ToolError:
                    raise
                except Exception as e:                      # 네트워크 등
                    _fail({"ok": False, "error": type(e).__name__, "message": str(e)})
            return run

        # 힌트는 카테고리 이름이 아니라 실제 내용으로 정한다.
        # 조회 전용 카테고리에 상태변경 API 가 하나 추가돼도 자동으로 따라간다.
        writes = any(is_state_changing(a) for a in apis)
        mcp.tool(name=tool_name, description=desc,
                 annotations={"title": f"메리츠 {CATEGORY_KO.get(category, category)}",
                              "readOnlyHint": not writes,
                              "destructiveHint": writes,
                              "idempotentHint": not writes,
                              "openWorldHint": True})(make())
        made.append(tool_name)
    return made
