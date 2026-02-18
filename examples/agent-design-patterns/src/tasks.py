"""태스크 정의 — 각 에이전트에게 할당되는 구체적인 작업"""

from crewai import Task, Agent


def create_plan_task(agent: Agent, topic: str) -> Task:
    return Task(
        description=(
            f"'{topic}'에 대한 시장 분석 조사 계획을 수립하세요.\n\n"
            "포함할 내용:\n"
            "1. 조사 범위 정의 (무엇을 조사할 것인가)\n"
            "2. 필요한 데이터 목록 (시장 규모, 성장률, 주요 플레이어 등)\n"
            "3. 각 조사 영역의 우선순위\n"
            "4. 예상되는 핵심 질문 3~5개"
        ),
        expected_output="구조화된 조사 계획서 (마크다운)",
        agent=agent,
    )


def create_research_task(agent: Agent, topic: str, plan: str) -> Task:
    return Task(
        description=(
            f"'{topic}'에 대해 시장 트렌드와 정량 데이터를 조사하세요.\n\n"
            f"조사 계획:\n{plan}\n\n"
            "반드시 포함할 내용:\n"
            "- 시장 규모 (금액, 단위 명시)\n"
            "- 연평균 성장률 (CAGR)\n"
            "- 주요 트렌드 3가지 이상\n"
            "- 데이터 출처 명시"
        ),
        expected_output="시장 트렌드 및 정량 데이터 보고서 (수치 포함)",
        agent=agent,
    )


def create_analysis_task(agent: Agent, topic: str, plan: str) -> Task:
    return Task(
        description=(
            f"'{topic}' 시장의 경쟁 환경을 분석하세요.\n\n"
            f"조사 계획:\n{plan}\n\n"
            "반드시 포함할 내용:\n"
            "- 주요 경쟁사 3곳 이상 (이름, 제품, 특징)\n"
            "- 시장 포지셔닝 비교\n"
            "- 각 플레이어의 강점/약점\n"
            "- 비교 표"
        ),
        expected_output="경쟁 환경 분석 보고서 (비교 표 포함)",
        agent=agent,
    )


def create_evaluation_task(
    agent: Agent, research_result: str, analysis_result: str
) -> Task:
    return Task(
        description=(
            "아래 두 조사 결과의 품질을 평가하세요.\n\n"
            f"## 시장 조사 결과\n{research_result}\n\n"
            f"## 경쟁 분석 결과\n{analysis_result}\n\n"
            "평가 기준:\n"
            "1. 구체적 수치(시장 규모, 성장률)가 있는가?\n"
            "2. 경쟁사가 3곳 이상 언급되었는가?\n"
            "3. 최신 트렌드가 포함되었는가?\n"
            "4. 논리적 근거가 있는가?\n\n"
            "**첫 줄에 반드시 PASS 또는 FAIL을 작성하세요.**\n"
            "FAIL인 경우 구체적으로 무엇이 부족한지 나열하세요."
        ),
        expected_output="PASS 또는 FAIL + 평가 상세 (첫 줄에 판정)",
        agent=agent,
    )


def create_supplementary_research_task(
    agent: Agent, topic: str, feedback: str
) -> Task:
    return Task(
        description=(
            f"'{topic}'에 대한 추가 조사를 수행하세요.\n\n"
            f"평가자 피드백:\n{feedback}\n\n"
            "위 피드백에서 지적된 부족한 부분을 보완하세요.\n"
            "구체적인 수치와 출처를 반드시 포함하세요."
        ),
        expected_output="보완된 조사 결과 (피드백 반영)",
        agent=agent,
    )


def create_strategy_task(
    agent: Agent, research_result: str, analysis_result: str
) -> Task:
    return Task(
        description=(
            "아래 조사 결과를 종합하여 전략적 인사이트를 도출하세요.\n\n"
            f"## 시장 조사\n{research_result}\n\n"
            f"## 경쟁 분석\n{analysis_result}\n\n"
            "포함할 내용:\n"
            "- 핵심 기회 영역 3가지\n"
            "- 주요 리스크 2가지\n"
            "- 추천 전략 (단기/중기/장기)\n"
            "- 우선순위 액션 아이템"
        ),
        expected_output="전략 인사이트 보고서 (기회, 리스크, 추천 전략)",
        agent=agent,
    )


def create_report_task(
    agent: Agent,
    topic: str,
    research_result: str,
    analysis_result: str,
    strategy_result: str,
) -> Task:
    return Task(
        description=(
            f"'{topic}'에 대한 최종 시장 분석 보고서를 마크다운으로 작성하세요.\n\n"
            f"## 시장 조사 데이터\n{research_result}\n\n"
            f"## 경쟁 분석\n{analysis_result}\n\n"
            f"## 전략 인사이트\n{strategy_result}\n\n"
            "보고서 구조:\n"
            "1. Executive Summary (3문장 이내)\n"
            "2. 시장 현황 (규모, 성장률, 트렌드)\n"
            "3. 경쟁 환경 (비교 표 포함)\n"
            "4. 전략 제언 (기회, 리스크, 액션)\n"
            "5. 부록 (출처, 용어 정의)\n\n"
            "경영진이 5분 안에 읽을 수 있는 분량으로 작성하세요."
        ),
        expected_output="완성된 시장 분석 보고서 (마크다운)",
        agent=agent,
    )
