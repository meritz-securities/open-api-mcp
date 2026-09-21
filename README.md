# 메리츠증권 Open API MCP 서버

[개발자 포털](https://openapi.imeritz.com) · [API 신청](https://openapi.imeritz.com/api-apply) · [API 문서](https://openapi.imeritz.com/apiservice) · [문의](https://openapi.imeritz.com/qna)

[![test](https://github.com/meritz-securities/open-api-mcp/actions/workflows/test.yml/badge.svg)](https://github.com/meritz-securities/open-api-mcp/actions/workflows/test.yml) [![release](https://img.shields.io/github/v/release/meritz-securities/open-api-mcp?label=%EC%84%A4%EC%B9%98%20%ED%8C%8C%EC%9D%BC)](https://github.com/meritz-securities/open-api-mcp/releases/latest) [![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

MCP 표준을 지원하는 AI 클라이언트에 연결해, 메리츠증권 Open API를
**대화로 다루실 수 있게** 해 주는 MCP 서버입니다.
시세·잔고·주문을 자연어로 요청하시면 됩니다.

## 먼저 설치하세요

최신 고객용 설치파일은 [릴리스 페이지](https://github.com/meritz-securities/open-api-mcp/releases/latest)에서 받으십시오.

| 사용 환경 | 설치파일 |
|---|---|
| Claude Desktop — Mac Apple Silicon | [MCPB 다운로드](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-darwin-arm64.mcpb) |
| Claude Desktop — Mac Intel | [MCPB 다운로드](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-darwin-x64.mcpb) |
| Claude Desktop — Windows | [MCPB 다운로드](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-win32-x64.mcpb) |
| Claude Code·Codex·Gemini·Cursor·VS Code | [OS별 실행파일](https://github.com/meritz-securities/open-api-mcp/releases/latest) |

설치 후 앱키와 시크릿을 입력합니다. 기본값은 조회 전용입니다.

## 저장소가 네 개입니다

| 하고 싶으신 일 | 여기로 |
|---|---|
| AI 클라이언트에 붙이기 | **이 저장소** |
| 파이썬으로 직접 호출해 보기 | [open-api](https://github.com/meritz-securities/open-api) — 실행 예제 |
| 터미널에서 조회·주문하기 | [open-api-studio](https://github.com/meritz-securities/open-api-studio) — `meritz` CLI |
| 호출 코드를 받아 쓰기 | [open-api-codegen-mcp](https://github.com/meritz-securities/open-api-codegen-mcp) |

## 앱키 발급

개발자 포털 <https://openapi.imeritz.com> 에서 앱키(App Key)와 시크릿(App Secret)을 발급받으세요.

1. 포털에 로그인합니다
2. 앱을 등록하고 사용하실 계좌를 연결합니다
3. 앱키와 시크릿을 발급받습니다

앱키에는 계좌가 묶입니다. 계좌번호를 따로 넣지 않아도 그 계좌가 조회되고,
주문도 그 계좌로 나갑니다.

> 앱키에 연결된 계좌는 실계좌입니다. 모의계좌를 전제로 시험하지 말아 주세요.

> **조회 결과는 연결하신 AI 서비스로 전송됩니다.** 해당 서비스의 데이터 처리
> 정책이 적용되며, 당사는 이에 관여하지 않습니다. 자세한 내용은
> [DISCLAIMER.md](DISCLAIMER.md)를 확인해 주세요.

## 설치 — 쓰시는 도구를 고르십시오

**Python이나 uv를 따로 깔지 않으셔도 됩니다.** 서버가 단일 실행 파일로 제공됩니다.
기본값은 조회 전용이고, 앱키는 설치 화면이나 환경변수로 넣습니다. 실행 파일 안에는 앱키가 없습니다.

### Claude Desktop — 설치 파일 더블클릭

| 내 컴퓨터 | 내려받기 |
|---|---|
| Mac — Apple 칩 (M1 이후) | [**meritz-open-api-darwin-arm64.mcpb**](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-darwin-arm64.mcpb) |
| Mac — Intel 칩 | [**meritz-open-api-darwin-x64.mcpb**](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-darwin-x64.mcpb) |
| Windows | [**meritz-open-api-win32-x64.mcpb**](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-open-api-win32-x64.mcpb) |

내려받은 파일을 더블클릭하면 Claude Desktop이 열리고, 앱키와 시크릿을 묻는 화면이 나옵니다.
입력하고 설치를 누르시면 끝입니다. 앱키는 OS 키체인(Mac) 또는 자격 증명 관리자(Windows)에 저장됩니다.

- 어느 칩인지 모르시면 Mac은 Apple 메뉴 → 이 Mac에 관하여에서 "칩" 항목을 보세요. "Apple M…"이면 Apple 칩입니다.
- Mac에서 "확인되지 않은 개발자" 경고가 뜨면 시스템 설정 → 개인정보 보호 및 보안 → **그래도 열기**를 누르세요.
- 새 버전은 파일을 다시 내려받아 설치하십시오. 직접 내려받은 설치 파일은 자동으로 갱신되지 않습니다.
- 파일 하나에 세 실행 파일을 다 넣지 않고 OS별로 나눈 것은, 크기를 30MB 안팎으로 유지하기 위해서입니다.


### 터미널로 설치하기 — `install.py`

포털 안내대로 저장소를 받아 `install.py`를 실행하면 이 PC에 맞는 실행 파일을 릴리스에서 내려받고, 클라이언트별로 붙여 넣을 명령을 보여 줍니다. Python은 이 스크립트를 돌리는 데만 쓰이고 실행 파일은 Python 없이 동작합니다.

```bash
git clone https://github.com/meritz-securities/open-api-mcp.git
cd open-api-mcp
python3 install.py                      # Windows: python install.py
python3 install.py --register claude-code   # Claude Code에 바로 등록 (codex · gemini 도 됩니다)
```

Mac 에서는 실행 권한 부여와 격리 속성(`com.apple.quarantine`) 해제까지 이 스크립트가 대신 해 줍니다. 아래 "실행 파일 + 명령 한 줄"을 손으로 하실 때만 두 단계를 직접 하시면 됩니다.

### Claude Code · Codex CLI · ChatGPT 데스크톱 · Gemini CLI · Cursor · VS Code — 실행 파일 + 명령 한 줄

1. 실행 파일을 내려받아 원하는 곳에 둡니다.

   | 내 컴퓨터 | 내려받기 |
   |---|---|
   | Mac — Apple 칩 | [meritz-mcp-darwin-arm64](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-mcp-darwin-arm64) |
   | Mac — Intel 칩 | [meritz-mcp-darwin-x64](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-mcp-darwin-x64) |
   | Windows | [meritz-mcp-win32-x64.exe](https://github.com/meritz-securities/open-api-mcp/releases/latest/download/meritz-mcp-win32-x64.exe) |

   **Mac 에서는 실행 권한과 격리 속성 해제를 둘 다 해 주셔야 합니다.** 한 번만 하시면 됩니다.

   ```bash
   chmod +x ~/Downloads/meritz-mcp-darwin-arm64
   xattr -d com.apple.quarantine ~/Downloads/meritz-mcp-darwin-arm64
   mkdir -p ~/meritz && mv ~/Downloads/meritz-mcp-darwin-arm64 ~/meritz/meritz-mcp
   ```

   > **격리 해제를 건너뛰면 서버가 뜨지 않습니다.** 브라우저로 내려받은 파일에는 macOS 가
   > `com.apple.quarantine` 속성을 붙입니다. 이 실행 파일은 ad-hoc 서명이라 Apple 개발자
   > 인증서가 없고 공증도 되어 있지 않아, 속성이 붙은 채로 실행되면 **아무 메시지 없이
   > 종료코드 -9(SIGKILL)로 죽습니다.** AI 앱의 도구 목록에 메리츠가 보이지 않는다면 이 속성이
   > 남아 있을 가능성이 큽니다. 같은 파일에서 속성만 지우면 정상 동작합니다.
   > `install.py` 로 설치하시면 실행 권한 부여와 격리 해제를 스크립트가 대신 해 줍니다.
   > (Claude Desktop 용 `.mcpb` 더블클릭은 Claude Desktop 이 직접 압축을 풀기 때문에
   > 이 속성이 붙지 않아, 이 작업이 필요 없습니다.)

   > **Windows** — `.exe` 를 처음 실행할 때 SmartScreen 경고가 뜰 수 있습니다. 서명되지 않은
   > 실행 파일이라 표시되는 경고입니다. 경고 창의 **추가 정보 → 실행**을 누르시면 됩니다.

2. 쓰시는 도구에 한 줄로 등록합니다. `<실행 파일 경로>`는 위에서 둔 위치의 **전체 경로**입니다 (예: `/Users/홍길동/meritz/meritz-mcp`).

   | 도구 | 명령 |
   |---|---|
   | **Claude Code** | `claude mcp add meritz --env MERITZ_APP_KEY=발급받은_앱키 --env MERITZ_APP_SECRET=발급받은_시크릿 -- <실행 파일 경로>` |
   | **Codex CLI** | `codex mcp add meritz --env MERITZ_APP_KEY=발급받은_앱키 --env MERITZ_APP_SECRET=발급받은_시크릿 -- <실행 파일 경로>` |
   | **ChatGPT 데스크톱** | 설정 → MCP servers → Add server → 이름 입력 → **STDIO** 선택 → 실행 파일 경로 입력 → 저장 → 재시작. 터미널을 쓰시면 위 Codex CLI 명령과 같습니다 |
   | **Gemini CLI** | `gemini mcp add -e MERITZ_APP_KEY=발급받은_앱키 -e MERITZ_APP_SECRET=발급받은_시크릿 meritz <실행 파일 경로>` |
   | **Cursor · VS Code** | 연결 도우미 [`docs/connect.html`](docs/connect.html) 파일을 내려받아 브라우저로 여신 뒤 실행 파일 경로와 앱키를 넣으시면 **한 번에 추가** 버튼이 만들어집니다 |

   > **ChatGPT 데스크톱** — ChatGPT 데스크톱 앱·Codex CLI·IDE 확장은 `~/.codex/config.toml` 을 함께 씁니다.
   > 어느 쪽에서 등록하셔도 나머지에 같이 잡힙니다. **ChatGPT 웹은 이 설정 파일을 읽지 못해 지원되지 않습니다**
   > — 웹에서 쓰시려면 아래 터널 방식을 보십시오.

   > **기동 대기는 60초로 늘려 두십시오.** 첫 기동에 8초 남짓 걸립니다(실측 8.2·8.2·8.6초).
   > Codex·ChatGPT 데스크톱의 기본 대기는 10초라 여유가 2초도 되지 않아, 느린 PC 나 백신 검사가
   > 끼면 넘겨 도구가 아예 뜨지 않습니다. `~/.codex/config.toml` 의 `[mcp_servers.meritz]`
   > 테이블에 `startup_timeout_sec = 60` 한 줄을 넣어 주세요 — 아래 "설정을 직접 넣으시려면"의
   > 예시가 그 형태입니다. `codex mcp add` 로 등록하셨다면 그 파일을 열어 해당 테이블에
   > 직접 추가하시면 됩니다.

   > **연결 도우미** — [`docs/connect.html`](docs/connect.html) 파일을 내려받아 브라우저로 여시면 앱키·실행 파일 경로를 넣는 대로
   > 위 명령과 Cursor·VS Code 버튼, JSON 설정을 만들어 드립니다. 입력한 값은 브라우저 밖으로 나가지 않습니다.
   > (GitHub 에서 링크를 누르면 HTML 소스가 그대로 보입니다. **파일을 내려받아 브라우저로 여세요.**)

<details>
<summary>uv와 Python 3.11 이상이 이미 있으시면 — 내려받기 없이 한 번에</summary>

| 도구 | 방법 |
|---|---|
| **Claude Code** | `claude mcp add meritz -- uvx --from git+https://github.com/meritz-securities/open-api-mcp meritz-mcp` |
| **Cursor** | [**한 번에 추가**](cursor://anysphere.cursor-deeplink/mcp/install?name=meritz&config=eyJjb21tYW5kIjoidXZ4IiwiYXJncyI6WyItLWZyb20iLCJnaXQraHR0cHM6Ly9naXRodWIuY29tL21lcml0ei1zZWN1cml0aWVzL29wZW4tYXBpLW1jcCIsIm1lcml0ei1tY3AiXSwiZW52Ijp7Ik1FUklUWl9BUFBfS0VZIjoiXHViYzFjXHVhZTA5XHViYzFiXHVjNzQwX1x1YzU3MVx1ZDBhNCIsIk1FUklUWl9BUFBfU0VDUkVUIjoiXHViYzFjXHVhZTA5XHViYzFiXHVjNzQwX1x1YzJkY1x1ZDA2Y1x1YjliZiIsIk1FUklUWl9SRUFEX09OTFkiOiIxIn19) |
| **VS Code** | [**한 번에 추가**](vscode:mcp/install?%7B%22name%22%3A%22meritz%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--from%22%2C%22git%2Bhttps%3A//github.com/meritz-securities/open-api-mcp%22%2C%22meritz-mcp%22%5D%2C%22env%22%3A%7B%22MERITZ_APP_KEY%22%3A%22%5Cubc1c%5Cuae09%5Cubc1b%5Cuc740_%5Cuc571%5Cud0a4%22%2C%22MERITZ_APP_SECRET%22%3A%22%5Cubc1c%5Cuae09%5Cubc1b%5Cuc740_%5Cuc2dc%5Cud06c%5Cub9bf%22%2C%22MERITZ_READ_ONLY%22%3A%221%22%7D%7D) |
| **Codex CLI** | `codex mcp add meritz -- uvx --from git+https://github.com/meritz-securities/open-api-mcp meritz-mcp` |

</details>

<details>
<summary>설정을 직접 넣으시려면</summary>

실행 파일을 쓰는 설정입니다. Codex CLI 는 `~/.codex/config.toml` 을 씁니다.

```toml
[mcp_servers.meritz]
command = "/Users/홍길동/meritz/meritz-mcp"
startup_timeout_sec = 60

[mcp_servers.meritz.env]
MERITZ_APP_KEY = "발급받은_앱키"
MERITZ_APP_SECRET = "발급받은_시크릿"
MERITZ_READ_ONLY = "1"
```

> `startup_timeout_sec` 는 `[mcp_servers.meritz]` 테이블 안, `[mcp_servers.meritz.env]` 줄보다
> **위**에 두셔야 합니다. 아래에 두면 환경변수로 읽힙니다.

> 환경변수는 반드시 `[mcp_servers.meritz.env]` 테이블로 적으십시오. `env_vars = { … }` 처럼
> 인라인 테이블로 적으면 `invalid type: map, expected a sequence` 로 **`~/.codex/config.toml`
> 전체가 읽히지 않아** Codex CLI 와 ChatGPT 데스크톱이 모두 뜨지 않습니다.
> `codex mcp add` 로 등록하시면 이 형식이 그대로 만들어집니다.

그 밖의 도구는 대개 이 JSON 형식을 받습니다 (Claude Desktop `claude_desktop_config.json`, Cursor `mcp.json`, Gemini CLI `settings.json`).

```json
{
  "mcpServers": {
    "meritz": {
      "command": "/Users/홍길동/meritz/meritz-mcp",
      "env": {
        "MERITZ_APP_KEY": "발급받은_앱키",
        "MERITZ_APP_SECRET": "발급받은_시크릿",
        "MERITZ_READ_ONLY": "1"
      }
    }
  }
}
```

</details>

### 릴리스에 올라온 파일이 무엇인지

[릴리스 페이지](https://github.com/meritz-securities/open-api-mcp/releases/latest)에는 파일이 여덟 개 있습니다. 쓰시는 것 **하나만** 받으시면 됩니다.

| 파일 | 무엇인지 |
|---|---|
| `meritz-open-api-darwin-arm64.mcpb`<br>`meritz-open-api-darwin-x64.mcpb`<br>`meritz-open-api-win32-x64.mcpb` | **Claude Desktop 설치 파일** (OS별 3종, 30MB 안팎). 더블클릭하면 설치됩니다 |
| `meritz-mcp-darwin-arm64`<br>`meritz-mcp-darwin-x64`<br>`meritz-mcp-win32-x64.exe` | **실행 파일** (OS별 3종, 30MB 안팎). Claude Code·Codex CLI·ChatGPT 데스크톱·Gemini CLI·Cursor·VS Code 에 **경로로 등록**해서 씁니다 |
| `SHA256SUMS.txt` | 위 파일들의 체크섬 |
| `meritz-open-api.mcpb` (100KB대) | **예전 방식입니다. 새로 받으실 분은 고르지 마십시오.** 실행 파일이 들어 있지 않고 uvx 로 내려받아 실행하는 형태라, **파이썬과 uv 가 따로 깔려 있어야** 동작합니다. 다음 릴리스부터는 올라오지 않습니다 |

받은 파일이 올라온 그대로인지 확인하시려면 `SHA256SUMS.txt` 를 받은 파일과 같은 폴더에 두고:

```bash
shasum -a 256 -c SHA256SUMS.txt        # 내려받지 않은 파일은 "FAILED open or read" 로 나옵니다
shasum -a 256 meritz-mcp-darwin-arm64  # 값 하나만 뽑아 SHA256SUMS.txt 의 해당 줄과 눈으로 대조하셔도 됩니다
```

Windows(PowerShell)에서는 값을 뽑아 대조하십시오.

```powershell
Get-FileHash .\meritz-mcp-win32-x64.exe -Algorithm SHA256
```

### Claude 웹·모바일, ChatGPT 웹 — 내 PC의 서버를 터널로 연결 (권장하지 않음)

> **권장하지 않는 부가 방법입니다.** 이 방식은 주문까지 가능한 서버를 인터넷에
> 노출합니다. 두 서비스 모두 커넥터 인증이 OAuth 또는 없음뿐이라, 주소의 난수 경로가
> 사실상 유일한 접근 통제입니다. 주소를 알게 된 사람은 누구나 주문할 수 있고,
> 그 주소는 AI 서비스 쪽에 커넥터 설정으로 저장됩니다.
> 가능하면 위의 실행 파일 등록 방식을 쓰시고, 쓰신 뒤에는 터널을 닫아 주십시오.

> ChatGPT **데스크톱 앱**을 쓰신다면 터널이 필요 없습니다. 위의 실행 파일 등록을 쓰십시오.
> 아래는 ChatGPT **웹**과 Claude 웹·모바일용입니다.

Claude 웹·모바일 앱과 ChatGPT 웹은 **인터넷 주소(HTTPS)로 접근되는 MCP 서버만** 받습니다.
이 서버는 내 PC에서 돌지만, 터널 도구로 임시 HTTPS 주소를 만들어 붙일 수 있습니다.
PC를 켜 두어야 하고, 무료 터널은 주소가 매번 바뀌며, 주소를 아는 사람은 누구나 접근할 수 있으므로
아래처럼 **난수 경로**를 꼭 넣으십시오. 두 서비스 모두 커넥터 인증 옵션이 OAuth 또는 없음뿐이라,
접속 토큰을 헤더가 아닌 주소 경로에 넣는 것이 유일한 방법입니다.

1. 서버를 HTTP 모드로 띄웁니다. `<난수>`는 아무도 모르는 긴 문자열로 바꾸세요 (연결 도우미가 만들어 드립니다).

   ```bash
   MERITZ_APP_KEY=발급받은_앱키 MERITZ_APP_SECRET=발급받은_시크릿 \
   MCP_TYPE=streamable-http MCP_PORT=8765 MCP_PATH=/mcp/<난수> ~/meritz/meritz-mcp
   ```

   Windows(PowerShell)에서는 `$env:MERITZ_APP_KEY="…"` 식으로 변수를 먼저 지정하고 실행 파일을 실행합니다.

2. 다른 터미널에서 터널을 엽니다. 둘 중 하나면 됩니다.

   ```bash
   cloudflared tunnel --url http://127.0.0.1:8765     # 계정 없이 임시 주소가 나옵니다
   ngrok http 8765                                     # ngrok 계정이 필요합니다
   ```

   `https://…trycloudflare.com` 또는 `https://….ngrok-free.app` 같은 주소가 표시됩니다.

3. 챗 서비스에 붙입니다. 주소는 `https://<터널 주소>/mcp/<난수>` 입니다.

   | 서비스 | 위치 | 조건 |
   |---|---|---|
   | **Claude** | 설정 → 커넥터 → 커스텀 커넥터 추가 → 주소 입력, 인증은 비워 둠 | 전 요금제. 웹·데스크톱에서 설정하면 휴대폰 앱과 음성 모드에서도 같은 연결을 씁니다 |
   | **ChatGPT 웹** | 설정 → 커넥터 → 고급 → 개발자 모드 켜기 → 만들기 → 주소 입력, 인증 없음 | 유료 요금제. 웹에서 설정. 음성 모드에서는 도구가 호출되지 않습니다 |

PC를 끄거나 터널을 닫으면 연결이 끊깁니다. 다시 열면 주소가 바뀌므로 커넥터의 주소도 고쳐 주셔야 합니다.

## 도구

분류마다 하나씩, 여섯 개입니다. 여기에 서버 정보를 돌려주는 `meritz_info`까지
모두 일곱 개가 뜹니다. `api_type`으로 호출할 API를 고르시면 됩니다.

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

`api_type='describe'`로 부르시면 파라미터와 응답 필드 설명을 돌려드립니다.
`meritz_info`는 서버 설정과 카탈로그 요약을 돌려드립니다. 카탈로그는 개발자 포털 등록 명세에서
만들며, REST 62건 중 60건을 도구로 노출합니다(토큰 발급·폐기 2건은 서버가 내부에서 처리합니다).

실시간(웹소켓)은 이 서버에서 다루지 않습니다. MCP는 요청·응답 모델이라
구독 스트림과 맞지 않기 때문입니다. 실시간 코드가 필요하시면
[open-api-codegen-mcp](https://github.com/meritz-securities/open-api-codegen-mcp)를 써 주세요.

## 주문은 두 단계입니다

주문과 환전은 먼저 내용을 보여드린 뒤 확인을 받아 전송합니다. 기본값은 조회 전용이며,
주문·환전 안전장치와 실제 접수 판정의 자세한 내용은 [DISCLAIMER.md](DISCLAIMER.md)를
확인해 주세요.

## 환경변수

| 변수 | 기본값 | 설명 |
|---|---|---|
| `MERITZ_APP_KEY` / `MERITZ_APP_SECRET` | — | 포털에서 발급 |
| `MERITZ_BASE_URL` | 운영 도메인 | 호출 대상 서버를 직접 지정합니다 (https 만) |
| `MERITZ_WS_URL` | 운영 실시간 도메인 | `MERITZ_BASE_URL`을 운영이 아닌 주소로 두셨다면 함께 지정하셔야 합니다 |
| `MERITZ_READ_ONLY` | `1` | **기본이 조회 전용입니다.** 주문·환전까지 쓰시려면 `0`으로 두세요 |
| `MERITZ_TIMEOUT` | `15` | 요청 제한시간(초) |
| `MCP_TYPE` | `stdio` | `streamable-http`로 두면 HTTP 서버로 뜹니다 (터널 연결용) |
| `MCP_HOST` / `MCP_PORT` / `MCP_PATH` | `127.0.0.1` / `8000` / `/mcp` | HTTP 모드의 주소·포트·경로. 경로에 난수를 넣어 접속 토큰으로 쓰십시오 |

## 응답 판정

HTTP 200이 왔다고 성공으로 넘기지 않습니다.

```
1) HTTP 200 인가 — 초당 호출 한도를 넘기면 500 과 함께 EGW00200 이 옵니다
2) 주문이라면 warn_cls_code 부터 — 경고면 접수되지 않았습니다
3) rsp_cd 를 읽을 수 있는가 → 성공 코드면 성공, 아니면 업무 오류
4) 읽을 수 없다면 알려진 문제인지 확인 (corrections.json)
     알려진 것이 아니면 실패로 처리합니다
     맞으면 데이터가 있을 때만 통과시키되 "검증되지 않음"을 표시합니다
     주문·환전은 여기서도 통과시키지 않습니다
```

성공으로 보는 코드는 `0000`·`0001`·`5762`·`5766`·`5820`·`5822`입니다.
`5762`는 다음 페이지가 있다는 뜻이고, `5820`·`5822`는 보통 조회 결과가 없다는 뜻입니다.

**`5820`으로 자료 유무를 판정하지 마십시오.** 담보 조회·종목별 실현손익·해외
실현손익은 자료를 담은 채로도 `5820`을 보냅니다. `data`가 비었는지로 판정하십시오.
오류 코드표는 open-api 저장소의
[docs/errors.md](https://github.com/meritz-securities/open-api/blob/main/docs/errors.md)에
있습니다 — 오류는 종류와 무관하게 HTTP 500으로 오고, 조치 정보는 `rsp_sub_msg`에 담깁니다.

## 개발

```bash
uv sync
uv run pytest tests/ -q
```

저장소를 내려받아 소스로 실행하실 때는 `.env.example`을 `.env`로 복사해 쓰셔도 됩니다.
단일 실행 파일은 `.env`를 읽지 않으니 환경변수로 넣어 주십시오.

실행 파일과 설치 파일을 직접 만드시려면:

```bash
./build_binary.sh                    # bin/meritz-mcp — PyInstaller 단일 실행 파일, 자기 점검 포함
python3 make_bundle.py darwin-arm64  # dist/meritz-open-api-darwin-arm64.mcpb (darwin-x64 · win32-x64 도 같음)
```

릴리스는 태그를 밀면 GitHub Actions가 세 플랫폼을 빌드해 올립니다: `git tag vX.Y.Z && git push origin vX.Y.Z`.

## 사용 전 확인해 주세요

- 이 서버는 **실제 계좌에 영향을 줍니다.** 모의계좌를 전제로 시험하지 말아 주세요
- 앱키와 시크릿을 저장소에 커밋하지 말아 주세요
- 조회 결과는 연결하신 AI 서비스로 전송되며, 해당 서비스의 데이터 처리 정책이 적용됩니다
- 투자 판단이나 매매 추천을 위한 도구가 아닙니다. [DISCLAIMER.md](DISCLAIMER.md)를 꼭 읽어 주세요

## 라이선스

MIT — [LICENSE](LICENSE)

문의는 개발자 포털을 이용해 주세요.
