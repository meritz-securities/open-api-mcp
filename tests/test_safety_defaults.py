"""안전 기본값이 회귀하지 않게 잠근다.

모의계좌가 없다. 앱키에 묶인 계좌는 언제나 실계좌다. 이 서버는 AI 에이전트가
스스로 주문을 낼 수 있는 경로라, 기본값이 유일한 완충재다.

여기서 보는 것은 셋이다.
  ① 아무것도 설정하지 않으면 조회 전용인가
  ② 빈 값·공백·알아볼 수 없는 값에서 안전한 쪽으로 떨어지는가
  ③ 게이트가 도구 계층이 아니라 라이브러리(ApiClient.call) 안에 있는가
"""
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MERITZ_NO_ENV_FILE", "1")
sys.path.insert(0, str(ROOT))

from meritz import safety  # noqa: E402
from meritz.catalog import load_catalog  # noqa: E402
from meritz.client import ApiClient, MeritzError  # noqa: E402
from meritz.config import Settings, settings  # noqa: E402

CAT = load_catalog()
ORDER = CAT.get("orders_buy")
QUOTE = CAT.get("market_prices")


# ------------------------------------------------- 안전 스위치 기본값
def test_module_default_is_read_only():
    """진입점(server.py)이 아니라 **모듈 기본값**이 닫혀 있어야 한다.

    server.py 의 set_read_only_default(True) 에만 기대면, 라이브러리로
    직접 임포트해 쓰는 경로가 서버 경로보다 덜 안전해진다.
    """
    import meritz.config as cfg
    assert cfg._READ_ONLY_DEFAULT == "1"


def test_default_is_read_only(monkeypatch):
    monkeypatch.delenv("MERITZ_READ_ONLY", raising=False)
    assert settings().read_only is True


def test_dataclass_default_is_read_only():
    """환경변수를 거치지 않고 Settings 를 직접 만들어도 닫혀 있어야 한다."""
    assert Settings().read_only is True


@pytest.mark.parametrize("value", ["", "   ", "yes please", "참", "1 "])
def test_unreadable_switch_value_falls_back_to_safe(monkeypatch, value):
    """안전 스위치가 오타 하나로 열리면 안 된다."""
    monkeypatch.setenv("MERITZ_READ_ONLY", value)
    assert settings().read_only is True, f"{value!r} 에서 열렸다"


def test_env_can_open_orders(monkeypatch):
    """명시적으로 열 수는 있어야 한다 — 그렇지 않으면 주문을 쓸 수 없다."""
    monkeypatch.setenv("MERITZ_READ_ONLY", "0")
    assert settings().read_only is False


# ------------------------------------------------- 주문 경로 게이트
def test_orders_are_blocked_in_read_only():
    c = ApiClient(Settings(app_key="k", app_secret="s", read_only=True))
    with pytest.raises(MeritzError) as e:
        c.call(ORDER, {})
    assert e.value.code == "READ_ONLY"


def test_orders_need_a_confirm_token_even_from_the_library():
    """게이트는 라이브러리 계층에 있어야 한다.

    도구 계층에만 두면 ApiClient 를 직접 임포트해 쓰는 코드에서 주문이
    무확인으로 나간다.
    """
    c = ApiClient(Settings(app_key="k", app_secret="s", read_only=False))
    with pytest.raises(MeritzError) as e:
        c.call(ORDER, _order_body())
    assert e.value.code == "NEEDS_CONFIRMATION"
    assert "confirm_token" in (e.value.body or {})


def test_a_valid_token_passes_the_gate():
    s = Settings(app_key="k", app_secret="s", read_only=False)
    c = ApiClient(s)
    body = ORDER.body_params(_order_body())
    pv = safety.preview(ORDER, body, s.base_url, s.app_key)
    # 게이트만 본다 — 통과하면 예외가 없다. 전송은 하지 않는다.
    c.require_confirmation(ORDER, {**_order_body(),
                                   "confirm_token": pv["confirm_token"]})


def test_the_token_is_single_use():
    s = Settings(app_key="k", app_secret="s", read_only=False)
    c = ApiClient(s)
    params = _order_body()
    pv = safety.preview(ORDER, ORDER.body_params(params), s.base_url, s.app_key)
    params["confirm_token"] = pv["confirm_token"]
    c.require_confirmation(ORDER, params)
    with pytest.raises(MeritzError) as e:
        c.require_confirmation(ORDER, params)
    assert e.value.code == "NEEDS_CONFIRMATION"


def test_queries_do_not_need_a_token():
    c = ApiClient(Settings(app_key="k", app_secret="s", read_only=True))
    c.require_confirmation(QUOTE, {"iscd": "005930"})


def _order_body() -> dict:
    return {"iscd": "A005930", "odqt": "1", "oder_unpr": "50000",
            "oder_cls_code": "01", "oder_cond_cls_code": "0",
            "orgl_oder_no": "0", "whol_rctf_cncl_yn": "N",
            "warn_cnfr_yn": "N", "exch_kind_code": "01"}
