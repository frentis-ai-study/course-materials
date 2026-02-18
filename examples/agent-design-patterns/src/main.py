"""
CrewAI 멀티에이전트 시장 분석 보고서 — 평가 루프 포함 데모

워크플로우:
  Plan → Research(병렬) → Evaluate → (부족하면 재조사) → Strategize → Write Report

사용법:
  uv run main.py                          # 기본 주제
  uv run main.py "클라우드 AI 시장 분석"   # 커스텀 주제
"""

import sys
from flow import MarketReportFlow


def main():
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "2026년 한국 AI 교육 시장"
    print(f"\n{'='*60}")
    print(f"  🚀 시장 분석 보고서 생성 시작")
    print(f"  📋 주제: {topic}")
    print(f"{'='*60}\n")

    flow = MarketReportFlow()
    result = flow.kickoff(inputs={"topic": topic})

    # 최종 보고서 저장
    report = flow.state.final_report
    if report:
        output_path = "output/report.md"
        with open(output_path, "w") as f:
            f.write(report)
        print(f"\n{'='*60}")
        print(f"  ✅ 보고서 저장 완료: {output_path}")
        print(f"  📊 평가 라운드: {flow.state.eval_round}회")
        print(f"{'='*60}\n")
    else:
        print("\n❌ 보고서 생성 실패")


if __name__ == "__main__":
    main()
