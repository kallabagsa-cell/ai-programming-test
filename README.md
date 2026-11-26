# 성적 관리 프로그램 (load_scores)

## ① 무엇을 하나요 (What)

성적 CSV를 읽어 유효한 점수(0~100 정수)만 골라 내고, 건너뛴 줄은 줄 번호·원본·이유와 함께 기록합니다.

## ② 왜 만들었나요 (Why)

실제 성적 파일에는 빈 칸 · 범위 밖 점수 · 정수가 아닌 값 · 중복 이름이 섞여 있어, 그냥 읽으면 프로그램이 죽거나 틀린 평균이 나옵니다.
그래서 "무엇을 남기고 무엇을 건너뛸지"를 명세로 먼저 정하고, 건너뛴 줄도 이유와 함께 남기도록 만들었습니다.
같은 이름은 동명이인일 수 있어 지우지 않고 둘 다 남깁니다. 누구를 쓸지는 쓰는 쪽이 정합니다.

## ③ 어떻게 쓰나요 (How)

Python 3.8 이상이 필요합니다.

```bash
# 설치
git clone https://github.com/kallabagsa-cell/ai-programming-test.git
cd ai-programming-test
pip install pytest pytest-cov

# 실행
python3 load_scores.py scores.csv
```

실행 결과 예시:

```
읽은 줄 : 5개
  김하나 88
  최,네번 77
  김하나 91
  윤보람 64
  서한별 95
건너뛴 줄 : 5개
  3행  이두리,105   ← 점수가 0~100 밖
  4행  박세찬,   ← 점수가 비어 있음
  7행  정오름,-5   ← 점수가 0~100 밖
  8행  한겨울,결석   ← 점수가 정수가 아님
  9행  장미르,72,비고없음   ← 열 개수가 2가 아님
```

## ④ 어떻게 테스트하나요

저장소 폴더 안에서:

```bash
pytest
# 커버리지까지 보려면
pytest --cov=load_scores --cov-report=term-missing
```

통과하면 다음처럼 나옵니다 (개수는 환경에 따라 같아야 하며, 전부 `.` 이어야 합니다).

```
test_ai_A.py .....................                 
test_ai_B.py ...................                   
test_load_scores.py ..........................     
============== 66 passed ==============
```

`bug3_logic.py`(8주차 버그 코드)를 시험하는 파일 두 개는 버그 때문에 일부러 실패하므로 기본 `pytest`에서는 빠져 있습니다(`conftest.py`).
직접 보려면 `pytest bug3_spec_check.py`(4개 실패) 또는 `pytest test_ai_bug.py`(2개 실패)를 실행하세요. 실패가 정상입니다.

## ⑤ 파일 구성

| 파일 | 하는 일 |
| --- | --- |
| `load_scores.py` | 성적 CSV를 읽어 `(유효 목록, 건너뛴 줄 기록)`을 돌려주는 함수 (직접 실행도 가능) |
| `test_load_scores.py` | 직접 작성한 테스트 (정상·예외·경계값, 16개 함수 / 26개 케이스) |
| `test_ai_A.py` | AI에게 **코드를 주고** 받은 테스트 |
| `test_ai_B.py` | AI에게 **명세만 주고** 받은 테스트 |
| `bug3_logic.py` | 8주차 버그 코드 (함정 실험용) |
| `test_ai_bug.py` | 고장난 `find_max`만 AI에게 주고 받은 테스트 (★ 함정 실험, 버그 때문에 2개 실패) |
| `conftest.py` | 일부러 실패하는 위 두 파일을 기본 `pytest`에서 제외 |
| `bug3_spec_check.py` | 위 버그 코드를 명세 기준으로 시험 — 버그를 잡아내는지 확인용 |
| `scores.csv` · `empty.csv` · `weird.csv` | 테스트용 데이터 (보통 / 헤더만 / 엉망인 파일) |
| `prompts.txt` | AI에게 보낸 A/B 프롬프트 원문 |
| `LICENSE` | MIT 라이선스 |

## ⑥ 만든 사람 · AI를 어디에 썼는지

- 만든 사람 : (박찬우) · (2026100008)
- AI를 쓴 곳 : Claude — `test_ai_A.py`, `test_ai_B.py` 작성과 케스트 보조·README 초안 작성 보조. 실험용 파일은 받은 그대로 저장했습니다.
- 내가 직접 판단한 것 : 설계표의 케이스 선정, README의 Why, 실행 결과 확인, 커밋 단위

## 라이선스

MIT License (LICENSE 파일 참고)
