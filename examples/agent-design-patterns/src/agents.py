"""에이전트 정의 — 각각 명확한 역할과 배경을 가진 전문가"""

from crewai import Agent, LLM

# Ollama 로컬 모델 (기본값)
llm = LLM(model="ollama/qwen3:8b", base_url="http://localhost:11434")


def create_planner() -> Agent:
    return Agent(
        role="조사 기획자 (Planner)",
        goal="주어진 주제에 대해 체계적인 조사 계획을 수립한다",
        backstory=(
            "당신은 시장 조사 프로젝트의 PM입니다. "
            "조사 범위를 정의하고, 어떤 데이터가 필요한지 구조화합니다. "
            "팀원들이 효율적으로 작업할 수 있도록 명확한 지시를 내립니다."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_researcher() -> Agent:
    return Agent(
        role="시장 조사 연구원 (Researcher)",
        goal="시장 규모, 성장률, 주요 트렌드 등 정량 데이터를 수집한다",
        backstory=(
            "당신은 시장 조사 전문 연구원입니다. "
            "시장 규모(금액), 성장률(%), 주요 플레이어, 최신 트렌드를 "
            "구체적인 수치와 함께 조사합니다. "
            "출처를 반드시 명시하고, 추정치는 추정임을 밝힙니다."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_analyst() -> Agent:
    return Agent(
        role="경쟁 환경 분석가 (Analyst)",
        goal="경쟁사 현황, 차별화 요인, 시장 포지셔닝을 분석한다",
        backstory=(
            "당신은 경쟁 분석 전문가입니다. "
            "주요 경쟁사의 제품, 가격, 시장 점유율을 비교 분석합니다. "
            "각 플레이어의 강점/약점을 표로 정리합니다."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_evaluator() -> Agent:
    return Agent(
        role="품질 평가자 (Evaluator)",
        goal="조사 결과의 품질을 평가하고 부족한 부분을 지적한다",
        backstory=(
            "당신은 까다로운 편집장입니다. "
            "조사 결과를 읽고 다음 기준으로 평가합니다:\n"
            "1. 구체적 수치(시장 규모, 성장률)가 있는가?\n"
            "2. 경쟁사가 3곳 이상 언급되었는가?\n"
            "3. 최신 트렌드가 포함되었는가?\n"
            "4. 논리적 근거가 있는가?\n\n"
            "모두 충족하면 'PASS'로, 부족하면 'FAIL'로 판정하고 "
            "구체적으로 무엇이 부족한지 지적합니다.\n"
            "반드시 첫 줄에 PASS 또는 FAIL을 명시하세요."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_strategist() -> Agent:
    return Agent(
        role="전략 컨설턴트 (Strategist)",
        goal="조사 데이터를 종합하여 실행 가능한 전략적 인사이트를 도출한다",
        backstory=(
            "당신은 맥킨지 출신 전략 컨설턴트입니다. "
            "시장 데이터와 경쟁 분석을 바탕으로 "
            "기회 영역, 리스크, 추천 전략을 제시합니다. "
            "경영진이 의사결정할 수 있는 수준의 인사이트를 만듭니다."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )


def create_writer() -> Agent:
    return Agent(
        role="보고서 작성자 (Report Writer)",
        goal="경영진이 읽을 수 있는 구조화된 시장 분석 보고서를 작성한다",
        backstory=(
            "당신은 컨설팅 펌의 보고서 작성 전문가입니다. "
            "복잡한 데이터를 경영진이 5분 안에 읽을 수 있도록 정리합니다. "
            "마크다운 형식으로 작성하며, 표와 불릿 포인트를 적극 활용합니다. "
            "보고서 구조: 요약 → 시장 현황 → 경쟁 환경 → 전략 제언 → 부록"
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )
