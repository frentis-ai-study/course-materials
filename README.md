# course-materials

프렌티스 교육 모노레포 — 시연/실습용 소스 코드

## 구조

```
examples/          ← 시연용 (브리핑, 세미나)
└── {LO slug}/     ← LO의 영문 slug 기준
    ├── README.md  ← 실행 가이드
    ├── src/       ← 소스 코드
    └── output/    ← 예상 결과물

labs/              ← 실습용 (실습 CU)
└── {LO slug}/
    ├── README.md
    ├── starter/   ← 수강생 시작 코드
    └── solution/  ← 정답 코드
```

## 규칙

- 폴더명은 LO frontmatter의 `slug` 값 사용 (한글 금지)
- 각 폴더에 `README.md` 필수
- GitHub: `frentis-ai-study/course-materials`
