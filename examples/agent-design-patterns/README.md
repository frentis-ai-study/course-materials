# 데모: CrewAI 멀티에이전트 시장 분석

> LO: `LO-Agent 설계 패턴과 운영` | 예상 시간: 3~5분

## 시연 목표

"6명의 AI Agent가 각자 역할을 나눠 조사하고, 품질이 부족하면 스스로 재조사한다"

## 워크플로우

```
[사용자] "2026년 AI 교육 시장 분석해줘"

     ┌─────────────┐
     │  Planner    │  ← 조사 계획 수립
     └──────┬──────┘
            │
     ┌──────┴──────┐
     │             │
┌────▼────┐  ┌────▼────┐
│Researcher│  │Analyst  │  ← 시장 데이터 + 경쟁사 분석
└────┬────┘  └────┬────┘
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Evaluator  │  ← ★ 품질 평가
     └──────┬──────┘
        ┌───┴───┐
     FAIL      PASS
        │        │
   ┌────▼────┐   │
   │Researcher│   │  ← 추가 조사 루프 (최대 2회)
   │추가 조사  │   │
   └────┬────┘   │
        └───┬────┘
     ┌──────▼──────┐
     │  Strategist │  ← 전략 인사이트 도출
     └──────┬──────┘
     ┌──────▼──────┐
     │Report Writer│  ← 경영진용 보고서 생성
     └─────────────┘
```

## 사전 체크리스트

```bash
# 1. Python 버전 확인 (3.11 이상, 3.14 미만)
python3 --version
# → Python 3.11.x ~ 3.13.x (3.14는 호환 불가)

# 2. uv 설치 확인
uv --version
# → uv 0.x.x 이상
# 미설치 시: curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Ollama 실행 확인
curl -s http://localhost:11434/api/tags | head -1
# → {"models":[...]} 응답이 와야 함
# 미실행 시: ollama serve

# 4. 모델 다운로드 확인
ollama list | grep qwen3:8b
# → qwen3:8b 보여야 함
# 미다운로드 시: ollama pull qwen3:8b

# 5. 의존성 사전 설치 (첫 실행 시 2~3분)
cd src
uv sync
# → Resolved X packages 확인
```

## 주요 파일 경로

```
src/
├── main.py              ← 진입점 (CLI 인자로 주제 입력)
├── agents.py            ← 6명의 Agent 정의
├── tasks.py             ← Agent별 Task 정의
├── flow.py              ← 워크플로우 + 평가 루프
├── pyproject.toml       ← 의존성 (crewai, litellm)
└── output/
    ├── report.md            ← 실행 결과 보고서
    └── sample-report.md     ← 사전 생성 샘플
```

## 시연 순서

### Step 1: 프로젝트 구조 보여주기 (30초)

```bash
cd src
ls
# agents.py  flow.py  main.py  tasks.py  pyproject.toml
```

- "6명의 Agent가 각각 파일로 정의되어 있습니다"
- "flow.py에 워크플로우가 있습니다 — 평가 루프 포함"

### Step 2: 코드 핵심 설명 (1분)

**agents.py 열고:**

- "Planner, Researcher, Analyst, Evaluator, Strategist, Writer — 6명의 전문가"
- "각각 역할(role), 목표(goal), 배경(backstory)이 있습니다"

**flow.py 열고:**

- "Plan → Research → **Evaluate** → (FAIL이면 재조사) → Strategy → Report"
- "Evaluator가 PASS/FAIL을 판단합니다. 사람이 개입하지 않아도요"

### Step 3: 실행 (2~3분)

```bash
uv run main.py "2026년 한국 AI 교육 시장"
```

- 터미널에 Agent들의 대화가 실시간 출력
- **Evaluator가 "FAIL — 시장 규모 수치 없음" 판정 → Researcher 재조사** 장면 주목
- "사람이 중간에 끼어들지 않아도, Agent가 스스로 품질을 관리합니다"

### Step 4: 결과 확인 (30초)

```bash
cat output/report.md
```

- 구조화된 보고서 확인 (요약 → 시장 현황 → 경쟁 환경 → 전략 제언)
- "6명의 Agent가 각자 역할을 수행하고, 품질까지 자체 검증한 결과입니다"

## 핵심 멘트

- "AI Agent는 챗봇이 아닙니다. 스스로 판단하고, 부족하면 재조사합니다"
- "6명의 전문가를 고용한 것과 같은 효과, 비용은 전기세뿐"
- "교육과정에서 이런 멀티에이전트를 직접 설계하고 구축합니다"

## 백업 플랜

| 실패 시나리오 | 대응 |
|-------------|------|
| Ollama 느림/에러 | `output/sample-report.md` 보여주며 "이런 결과가 나옵니다" |
| CrewAI 설치 실패 | 사전에 `uv sync` 완료 확인 |
| 평가 루프 미발동 | "실제로는 데이터가 부족하면 재조사가 발동됩니다" 설명 후 샘플 보여주기 |
