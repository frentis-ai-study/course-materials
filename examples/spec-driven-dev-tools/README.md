# 데모: OpenSpec 스펙 생성 시연

> LO: `LO-스펙 주도 개발 도구` | 예상 시간: 2~3분

## 시연 목표

"코드 전에 명세를 먼저 — AI가 실행하기 전에 인간이 방향을 정한다"

## 사전 체크리스트

```bash
# 1. Claude Code 설치 확인
claude --version
# → claude-code x.x.x 이상
# 미설치 시: npm install -g @anthropic-ai/claude-code

# 2. OpenSpec 확장 설치 확인
claude extensions list 2>/dev/null || echo "extensions 명령 확인"
# OpenSpec이 설치되어 있어야 함
# 미설치 시: claude install-extension fission-ai/openspec

# 3. 샘플 프로젝트 디렉토리 준비
# 아무 코드 프로젝트면 됨 (Git 저장소 권장)
# 예: Spring AI 데모 프로젝트 등

# 4. Anthropic API 키 확인 (Claude Code 동작에 필요)
echo $ANTHROPIC_API_KEY | head -c 10
# → sk-ant-api 로 시작해야 함
```

## 시연 순서

### Step 1: 문제 제기 (30초)

- "AI에게 '로그인 기능 만들어줘'라고 바로 시키면 어떻게 될까요?"
- "빠르게 나오지만, 요구사항이 채팅 기록에 흩어집니다"
- "3개월 뒤 이 코드를 왜 이렇게 짰는지 아무도 모릅니다"

### Step 2: OpenSpec으로 명세 먼저 (1분)

```bash
# Claude Code 내에서
/opsx:new add-2fa-authentication
```

- AI가 `openspec/changes/add-2fa-authentication/` 폴더 생성
- proposal.md (왜 이 변경이 필요한지) 자동 생성

```bash
/opsx:continue
```

- specs/ 생성 — Delta 스펙 (ADDED/MODIFIED/REMOVED)
- "변경되는 부분만 기록합니다. 기존 코드는 건드리지 않아요"

```bash
/opsx:continue
```

- design.md 생성 — 기술 설계
- tasks.md 생성 — AI가 실행할 작업 목록

### Step 3: 코드 실행 (30초)

```bash
/opsx:apply add-2fa-authentication
```

- AI가 tasks.md 기반으로 코드 생성
- "명세를 기준으로 코드를 만들었기 때문에, 누가 언제 요청해도 같은 결과"

### Step 4: 핵심 비교 (30초)

| 구분 | 채팅 기반 | 스펙 기반 (OpenSpec) |
|------|----------|---------------------|
| 요구사항 위치 | 채팅 기록 (흩어짐) | proposal.md (구조화) |
| 재현 가능 | 불가 | 가능 |
| 팀 공유 | 어려움 | Git으로 관리 |
| 변경 추적 | 불가 | Delta 스펙으로 추적 |

## 핵심 멘트

- "코드를 짜기 전에, 뭘 만들지 먼저 정합니다"
- "이게 Vibe Coding과 프로페셔널 개발의 차이입니다"
- "교육과정에서 이 방법론을 직접 실습합니다"

## 백업 플랜

| 실패 시나리오 | 대응 |
|-------------|------|
| OpenSpec 설치 안 됨 | LO 슬라이드에서 스크린샷으로 대체 |
| Claude Code 에러 | 폴더 구조만 직접 보여주며 설명 |
| 시간 부족 | Step 2까지만 (proposal + specs) |
