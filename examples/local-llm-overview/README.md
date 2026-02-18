# 데모: OpenCode + Ollama 프라이빗 코딩

> LO: `LO-로컬 LLM 개요` | 예상 시간: 2~3분

## 시연 목표

"로컬 LLM으로 무료 AI 코딩 에이전트 — 코드가 외부로 안 나가고, Copilot 비용도 없다"

## 사전 요구사항

- Ollama 설치 및 실행 중 (`ollama serve`)
- Qwen2.5-Coder 7B 모델 다운로드 완료
- OpenCode CLI 설치

```bash
# 사전 준비 (시연 전 완료)
ollama pull qwen2.5-coder:7b
```

## 시연 순서

### Step 1: 샘플 프로젝트 보여주기 (30초)

```bash
cd src/sample-project
ls
# main.py  models.py  requirements.txt
```

- 간단한 FastAPI 도서 관리 API (파일 3개)
- "이 프로젝트에 README가 없습니다. AI한테 시켜봅시다"
- main.py를 열어서 코드 간단히 보여주기

### Step 2: OpenCode 실행 (1분)

```bash
opencode .
```

OpenCode TUI가 뜨면:

```
> 이 프로젝트의 README.md를 작성해줘.
  프로젝트 구조, 실행 방법, API 엔드포인트를 포함해.
```

- AI가 파일을 자동으로 읽고 분석
- README.md 생성 → 내용 확인
- "지금 Qwen2.5-Coder 7B이 로컬에서 돌고 있습니다. Ollama 위에서요"

### Step 3: 결과 확인 + 핵심 (30초)

```bash
cat README.md
```

- 생성된 README 내용 확인
- "이 전체 과정에서 코드가 외부 서버로 나간 게 **하나도 없습니다**. 전부 이 컴퓨터 안에서"

### Step 4: 비용 비교 (30초)

| 항목 | GitHub Copilot | OpenCode + Ollama |
|------|---------------|-------------------|
| **월 비용** | $19 (개인) / $39 (비즈니스) | **$0** |
| **코드 전송** | GitHub 서버로 전송 | **로컬 유지** |
| **오프라인** | 불가 | **가능** |
| **모델 선택** | GPT 고정 | **자유 선택** |

- "Copilot 월 $19, 이건 무료입니다"
- "개발자 100명이면 연간 $46,800 절감"

## 핵심 멘트

- "Copilot 월 $19, 이건 무료입니다"
- "코드가 외부 서버로 나가지 않습니다"
- "교육과정에서 이 환경을 직접 구축합니다"

## 백업 플랜

| 실패 시나리오 | 대응 |
|-------------|------|
| Ollama 안 뜸 | `ollama serve` 재시작, 안 되면 `output/` 예시로 진행 |
| 모델 응답 느림 | "실제 환경에서는 GPU가 있으면 훨씬 빠릅니다" |
| OpenCode 에러 | `output/generated-readme.md` 보여주며 "이런 결과가 나옵니다" |
