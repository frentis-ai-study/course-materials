"""
시장 분석 Flow — 평가 루프 포함

Plan → Research & Analyze (병렬) → Evaluate → (FAIL이면 재조사) → Strategy → Report
"""

from crewai import Crew, Process
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

from agents import (
    create_analyst,
    create_evaluator,
    create_planner,
    create_researcher,
    create_strategist,
    create_writer,
)
from tasks import (
    create_analysis_task,
    create_evaluation_task,
    create_plan_task,
    create_report_task,
    create_research_task,
    create_strategy_task,
    create_supplementary_research_task,
)

MAX_EVAL_ROUNDS = 2  # 최대 재조사 횟수


class ReportState(BaseModel):
    topic: str = ""
    plan: str = ""
    research_result: str = ""
    analysis_result: str = ""
    eval_feedback: str = ""
    eval_round: int = 0
    strategy_result: str = ""
    final_report: str = ""


class MarketReportFlow(Flow[ReportState]):
    """시장 분석 보고서 생성 Flow — 평가 루프 포함"""

    @start()
    def plan(self):
        """1단계: 조사 계획 수립"""
        self.state.topic = self.state.topic or "2026년 한국 AI 교육 시장"
        print(f"\n📋 [Planner] 조사 계획 수립 중... 주제: {self.state.topic}")

        planner = create_planner()
        task = create_plan_task(planner, self.state.topic)
        crew = Crew(agents=[planner], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state.plan = str(result)
        print(f"\n✅ [Planner] 계획 수립 완료")

    @listen(plan)
    def research_and_analyze(self):
        """2단계: 시장 조사 + 경쟁 분석 (병렬 실행)"""
        print(f"\n🔍 [Researcher + Analyst] 조사 시작...")

        researcher = create_researcher()
        analyst = create_analyst()

        research_task = create_research_task(
            researcher, self.state.topic, self.state.plan
        )
        analysis_task = create_analysis_task(
            analyst, self.state.topic, self.state.plan
        )

        crew = Crew(
            agents=[researcher, analyst],
            tasks=[research_task, analysis_task],
            verbose=True,
            process=Process.sequential,  # 안정성을 위해 순차 실행
        )
        crew.kickoff()

        self.state.research_result = str(research_task.output)
        self.state.analysis_result = str(analysis_task.output)
        print(f"\n✅ [Researcher + Analyst] 조사 완료")

    @listen(research_and_analyze)
    def evaluate(self):
        """3단계: 조사 결과 품질 평가"""
        self.state.eval_round += 1
        print(
            f"\n🔎 [Evaluator] 평가 라운드 {self.state.eval_round}/{MAX_EVAL_ROUNDS + 1}..."
        )

        evaluator = create_evaluator()
        task = create_evaluation_task(
            evaluator, self.state.research_result, self.state.analysis_result
        )
        crew = Crew(agents=[evaluator], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state.eval_feedback = str(result)
        print(f"\n📝 [Evaluator] 평가 결과: {self.state.eval_feedback[:100]}...")

    @router(evaluate)
    def check_quality(self):
        """평가 결과에 따라 라우팅: PASS → 전략 수립, FAIL → 재조사"""
        feedback = self.state.eval_feedback.strip().upper()

        if feedback.startswith("PASS") or self.state.eval_round > MAX_EVAL_ROUNDS:
            if self.state.eval_round > MAX_EVAL_ROUNDS:
                print(f"\n⚠️  최대 재조사 횟수 도달. 현재 결과로 진행합니다.")
            else:
                print(f"\n✅ [Evaluator] PASS — 품질 충분. 다음 단계로 진행합니다.")
            return "passed"
        else:
            print(f"\n🔄 [Evaluator] FAIL — 추가 조사가 필요합니다.")
            return "needs_more_research"

    @listen("needs_more_research")
    def supplementary_research(self):
        """재조사: 평가자 피드백 기반으로 추가 데이터 수집"""
        print(f"\n🔍 [Researcher] 추가 조사 수행 중...")

        researcher = create_researcher()
        task = create_supplementary_research_task(
            researcher, self.state.topic, self.state.eval_feedback
        )
        crew = Crew(agents=[researcher], tasks=[task], verbose=True)
        result = crew.kickoff()

        # 기존 결과에 추가 결과를 병합
        self.state.research_result += f"\n\n## 추가 조사 (라운드 {self.state.eval_round})\n{result}"
        print(f"\n✅ [Researcher] 추가 조사 완료. 재평가로 이동합니다.")

    @listen(supplementary_research)
    def re_evaluate(self):
        """재평가 — evaluate와 동일 로직"""
        self.evaluate()

    @router(re_evaluate)
    def re_check_quality(self):
        """재평가 후 라우팅 — check_quality와 동일 로직"""
        return self.check_quality()

    @listen("passed")
    def strategize(self):
        """4단계: 전략 인사이트 도출"""
        print(f"\n💡 [Strategist] 전략 수립 중...")

        strategist = create_strategist()
        task = create_strategy_task(
            strategist, self.state.research_result, self.state.analysis_result
        )
        crew = Crew(agents=[strategist], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state.strategy_result = str(result)
        print(f"\n✅ [Strategist] 전략 수립 완료")

    @listen(strategize)
    def write_report(self):
        """5단계: 최종 보고서 작성"""
        print(f"\n📝 [Writer] 최종 보고서 작성 중...")

        writer = create_writer()
        task = create_report_task(
            writer,
            self.state.topic,
            self.state.research_result,
            self.state.analysis_result,
            self.state.strategy_result,
        )
        crew = Crew(agents=[writer], tasks=[task], verbose=True)
        result = crew.kickoff()
        self.state.final_report = str(result)
        print(f"\n✅ [Writer] 보고서 작성 완료")
