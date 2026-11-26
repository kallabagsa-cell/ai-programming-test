"""bug3_logic.py 를 '명세' 기준으로 시험한 것 (함정 실험 대조용).
find_max 는 가장 큰 점수, count_pass 는 cutoff '이상'을 센다 — 이것이 명세다.
실행: pytest bug3_spec_check.py  (일반 pytest 에서는 수집되지 않음)
버그 있는 원본에서는 아래 일부가 실패해야 정상이다(= 테스트가 버그를 잡는다).
"""
import pytest

from bug3_logic import find_max, count_pass


@pytest.mark.parametrize("data, 정답", [
    ([70, 85, 60, 95], 95),   # 8주차 그 데이터
    ([95, 85, 70, 60], 95),
    ([10, 20, 30], 30),
    ([5], 5),
])
def test_find_max는_가장_큰_점수를_돌려준다(data, 정답):
    assert find_max(data) == 정답


@pytest.mark.parametrize("data, 정답", [
    ([70, 85, 60, 95], 4),    # 60점도 합격
    ([60, 60, 59], 2),        # 경계값 60 자체
    ([70, 85, 95], 3),
])
def test_count_pass는_cutoff_이상을_센다(data, 정답):
    assert count_pass(data) == 정답
