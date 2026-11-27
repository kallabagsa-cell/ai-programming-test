# test_ai_bug.py — ★ 함정: 고장난 find_max 함수만 주고 받은 테스트 (프롬프트 "함정")
# ※ Claude가 find_max 코드만 보고 작성, 수정 없이 저장. (같은 대화라 버그를 이미 알고 있던 상태임)
import pytest

from bug3_logic import find_max


def test_find_max_unsorted():
    assert find_max([70, 85, 60, 95]) == 95


def test_find_max_first_is_largest():
    assert find_max([95, 85, 70, 60]) == 95


def test_find_max_last_is_largest():
    assert find_max([10, 20, 30]) == 30


def test_find_max_single_element():
    assert find_max([5]) == 5


def test_find_max_negative_numbers():
    assert find_max([-3, -1, -2]) == -1


def test_find_max_duplicates():
    assert find_max([50, 50, 50]) == 50


def test_find_max_empty_list_raises():
    with pytest.raises(IndexError):
        find_max([])
