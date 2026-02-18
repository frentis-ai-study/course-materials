# 사내 도서 관리 API

FastAPI 기반의 사내 도서 관리 REST API입니다.

## 프로젝트 구조

```
├── main.py           # FastAPI 애플리케이션 및 엔드포인트
├── models.py         # Pydantic 데이터 모델
└── requirements.txt  # Python 의존성
```

## 실행 방법

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

서버가 `http://localhost:8000`에서 시작됩니다.

## API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/books` | 모든 도서 조회 |
| GET | `/books/{id}` | 특정 도서 조회 |
| POST | `/books` | 새 도서 등록 |
| DELETE | `/books/{id}` | 도서 삭제 |

## 사용 예시

```bash
# 도서 등록
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "클린 코드", "author": "로버트 마틴", "category": "개발"}'

# 전체 조회
curl http://localhost:8000/books
```

## API 문서

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
