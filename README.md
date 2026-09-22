# 메리츠증권 Open API MCP 서버

> 현재 베타 서비스 기간입니다.

[개발자 포털](https://openapi.imeritz.com) · [API 신청](https://openapi.imeritz.com/api-apply) · [API 문서](https://openapi.imeritz.com/apiservice) · [문의](https://openapi.imeritz.com/qna)

[![test](https://github.com/meritz-securities/open-api-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/meritz-securities/open-api-mcp/actions/workflows/test.yml) [![release](https://img.shields.io/github/v/release/meritz-securities/open-api-mcp?label=%EC%84%A4%EC%B9%98%20%ED%8C%8C%EC%9D%BC)](https://github.com/meritz-securities/open-api-mcp/releases/latest) [![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

MCP를 지원하는 AI 클라이언트에 연결해, 메리츠증권 Open API의 시세·잔고·주문을
대화로 다루는 MCP 서버입니다. 내 PC에서 도는 로컬 서버이고, 단일 실행 파일이라
Python이나 uv를 따로 설치하지 않으셔도 됩니다.

기본값은 조회 전용입니다. 주문·환전은 `MERITZ_READ_ONLY=0`으로 두셔야 열립니다.

## 앱키

[개발자 포털](https://openapi.imeritz.com)에서 앱키(App Key)와 시크릿(App Secret)을 발급받으십시오.
앱키에는 계좌가 묶입니다. 요청에 계좌번호를 넣지 않아도 그 계좌가 조회되고, 주문도 그 계좌로 나갑니다.
실행 파일 안에는 앱키가 없습니다. 설치 화면이나 환경변수로 넣습니다.

## 설치

파일은 [릴리스 페이지](https://github.com/meritz-securities/open-api-mcp/releases/latest)에서 받으십시오.
쓰시는 것 하나만 받으시면 됩니다.

| 쓰시는 도구 | 방법 |
|---|---|
| Claude Desktop | OS에 맞는 `.mcpb` 파일을 내려받아 더블클릭 — [Mac Apple 칩](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-darwin-arm64.mcpb) · [Mac Intel](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-darwin-x64.mcpb) · [Windows](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-win32-x64.mcpb) |
| 아무 도구나 — 자동 설치 | `git clone` 후 `python3 install.py` — 실행 파일을 내려받고 등록 명령까지 만들어 줍니다 |
| Claude Code | `claude mcp add meritz --env MERITZ_APP_KEY=앱키 --env MERITZ_APP_SECRET=시크릿 -- <실행 파일 경로>` |
| Codex CLI · ChatGPT 데스크톱 | `codex mcp add meritz --env MERITZ_APP_KEY=앱키 --env MERITZ_APP_SECRET=시크릿 -- <실행 파일 경로>` |
| Gemini CLI | `gemini mcp add -e MERITZ_APP_KEY=앱키 -e MERITZ_APP_SECRET=시크릿 meritz <실행 파일 경로>` |
| Cursor · VS Code | [`docs/connect.html`](docs/connect.html)을 내려받아 브라우저로 열면 **한 번에 추가** 버튼이 만들어집니다 |

실행 파일은 [Mac Apple 칩](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-mcp-darwin-arm64) ·
[Mac Intel](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-mcp-darwin-x64) ·
[Windows](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-mcp-win32-x64.exe) 입니다.
Mac에서 직접 내려받으셨다면 `chmod +x`와 `xattr -d com.apple.quarantine`을 걸어 주십시오.
격리 속성이 남아 있으면 서버가 아무 메시지 없이 종료되어 도구 목록에 나타나지 않습니다.

OS 보안 경고, 체크섬 대조, 기동 대기 시간, Claude 웹·ChatGPT 웹을 조회 전용으로
붙이는 터널 연결은
[`docs/install.md`](docs/install.md)에 있습니다. `install.py`가 이 과정을 대신해 줍니다.

## 도구

설치하고 클라이언트를 다시 시작하면 도구 일곱 개가 뜹니다. "삼성전자 현재가 알려줘"처럼
그대로 물어보시면 됩니다. 분류마다 하나씩 여섯 개에, 서버 설정과 카탈로그 요약을 돌려주는
`meritz_info`까지 일곱 개이고, `api_type`으로 호출할 API를 고릅니다.

| 도구 | 다루는 것 | API |
|---|---|---:|
| `meritz_account` | 잔고·예수금·평가·거래내역·손익 | 11건 |
| `meritz_market` | 국내주식 시세·호가·체결·투자자별 매매 | 10건 |
| `meritz_overseas_market` | 해외주식 시세·호가·체결 | 6건 |
| `meritz_trading` | 주문·정정·취소·주문내역·예약주문 | 24건 |
| `meritz_forex` | 환율·환전 | 4건 |
| `meritz_reference` | 거래일·장 운영시간·거래소 등 참조 정보 | 5건 |

국내와 해외 시세를 한 도구에 담지 않은 것은 종목코드와 거래소 코드 체계가 서로 달라서입니다.
섞어 두면 모델이 국내 파라미터를 해외 조회에 그대로 넣습니다.
`api_type='describe'`로 부르면 파라미터와 응답 필드 설명을 돌려줍니다. REST 62건 중
60건을 도구로 노출하고, 토큰 발급·폐기 2건은 서버가 내부에서 처리합니다.

실시간(웹소켓)은 MCP의 요청·응답 모델과 맞지 않아 이 서버에서 다루지 않습니다.
실시간 코드는 [open-api-codegen-mcp](https://github.com/meritz-securities/open-api-codegen-mcp)에서 받으십시오.

## 환경변수

| 변수 | 기본값 | 설명 |
|---|---|---|
| `MERITZ_APP_KEY` / `MERITZ_APP_SECRET` | — | 포털에서 발급 |
| `MERITZ_BASE_URL` | `https://openapi.imeritz.com:9443` | 호출 대상 (https 만) |
| `MERITZ_READ_ONLY` | `1` | 기본이 조회 전용입니다. 주문·환전까지 쓰시려면 `0` |
| `MERITZ_TIMEOUT` | `15` | 요청 제한시간(초) |
| `MCP_TYPE` | `stdio` | `streamable-http`로 두면 HTTP 서버로 뜹니다 |
| `MCP_HOST` / `MCP_PORT` / `MCP_PATH` | `127.0.0.1` / `8000` / `/mcp` | HTTP 모드의 주소·포트·경로 |

## 주문은 두 단계입니다

주문과 환전은 첫 호출에서 전송하지 않고 보낼 내용과 `confirm_token`만 돌려줍니다.
사람이 내용을 확인한 뒤 토큰을 넣어 다시 호출해야 실제로 나갑니다. 토큰은 한 번만 쓸 수
있고 180초 뒤 만료되며, 보낼 내용·대상 서버·앱키 중 하나라도 바뀌면 무효가 됩니다.

이 절차는 실수를 막기 위한 것이지, 사람이 내용을 확인했다는 증거는 아닙니다.
게이트는 `ApiClient.call()` 에 있어, 도구로 호출하시든 같은 패키지의 클라이언트를
파이썬에서 직접 부르시든 똑같이 걸립니다. 한계와 주문 접수 판정은
[DISCLAIMER.md](DISCLAIMER.md)에 적어 두었습니다.

## 저장소가 네 개입니다

| 하고 싶으신 일 | 여기로 |
|---|---|
| AI 클라이언트에 붙이기 | **이 저장소** |
| 파이썬으로 직접 호출해 보기 | [open-api](https://github.com/meritz-securities/open-api) — 실행 예제 |
| 터미널에서 조회·주문하기 | [open-api-studio](https://github.com/meritz-securities/open-api-studio) — `meritz` CLI |
| 호출 코드를 받아 쓰기 | [open-api-codegen-mcp](https://github.com/meritz-securities/open-api-codegen-mcp) — MCP 서버 |

## 개발

```bash
uv sync
uv run pytest tests/ -q

./build_binary.sh                    # bin/meritz-mcp — PyInstaller 단일 실행 파일
python3 make_bundle.py darwin-arm64  # dist/meritz-open-api-darwin-arm64.mcpb
```

소스로 실행하실 때는 `.env.example`을 `.env`로 복사해 쓰셔도 됩니다. 단일 실행 파일은
`.env`를 읽지 않으니 환경변수로 넣어 주십시오. 릴리스는 태그를 밀면 GitHub Actions가
세 플랫폼을 빌드해 올립니다.

## 사용 전 확인해 주세요

- 대상 서버는 운영이 기본값이고, 앱키에 연결된 계좌는 실계좌입니다. 모의계좌는 없습니다
- 기본값은 조회 전용입니다. 주문·환전은 `MERITZ_READ_ONLY=0`으로 두셔야 열립니다
- 확인 절차는 실수를 막기 위한 것이지, 사람이 내용을 확인했다는 증거는 아닙니다
- 조회 결과는 연결하신 AI 서비스로 전송되며, 해당 서비스의 데이터 처리 정책이 적용됩니다
- 앱키와 시크릿을 저장소에 커밋하지 말아 주세요
- [DISCLAIMER.md](DISCLAIMER.md)를 꼭 읽어 주세요

## 라이선스

MIT — [LICENSE](LICENSE)

실행 파일에 함께 들어가는 오픈소스의 라이선스 전문은
[THIRD-PARTY-NOTICES.txt](THIRD-PARTY-NOTICES.txt) 에 있습니다.

문의는 개발자 포털을 이용해 주세요.
