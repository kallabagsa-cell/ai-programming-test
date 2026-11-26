"""load_scores 단위 테스트 (11주차 직접 작성).

케이스는 load_scores.py 를 열기 전에, 10주차 명세서 6칸을 보고 설계표에 먼저 적었습니다.
실행:  pytest        (이 폴더 안에서)
"""
import contextlib
import io
import runpy
import sys
from pathlib import Path

import pytest

from load_scores import load_scores

# 어느 폴더에서 pytest 를 돌려도 배포 CSV 를 찾도록 이 파일 기준 경로를 씁니다.
DATA = Path(__file__).parent


def 만들기(tmp_path, 본문, 인코딩="utf-8"):
    """헤더 + 본문으로 임시 CSV 를 만들고 경로를 돌려준다."""
    p = tmp_path / "임시.csv"
    p.write_text("name,score\n" + 본문, encoding=인코딩)
    return p


# ═══════════════════════ 정상 ═══════════════════════
def test_정상_파일을_읽는다():
    kept, skipped = load_scores(DATA / "scores.csv")
    assert kept == [
        ("김하나", 88),
        ("최,네번", 77),
        ("김하나", 91),
        ("윤보람", 64),
        ("서한별", 95),
    ]


def test_건너뛴_줄의_번호가_기록된다():
    kept, skipped = load_scores(DATA / "scores.csv")
    assert [줄번호 for 줄번호, _, _ in skipped] == [3, 4, 7, 8, 9]


def test_빈_줄은_건너뛰고_기록하지_않는다(tmp_path):
    p = 만들기(tmp_path, "가,80\n\n나,90\n")
    kept, skipped = load_scores(p)
    assert kept == [("가", 80), ("나", 90)]
    assert skipped == []


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    p = 만들기(tmp_path, '"김,하나",88\n')
    kept, skipped = load_scores(p)
    assert kept == [("김,하나", 88)]


def test_같은_이름이_두_번_나오면_둘_다_남긴다(tmp_path):
    p = 만들기(tmp_path, "김하나,88\n김하나,91\n")
    kept, skipped = load_scores(p)
    assert kept == [("김하나", 88), ("김하나", 91)]


def test_점수_앞뒤_공백은_무시한다(tmp_path):
    p = 만들기(tmp_path, "한겨울,  77\n")
    kept, skipped = load_scores(p)
    assert kept == [("한겨울", 77)]


def test_BOM이_붙은_파일도_읽는다(tmp_path):
    p = 만들기(tmp_path, "가,80\n", 인코딩="utf-8-sig")
    kept, skipped = load_scores(p)
    assert kept == [("가", 80)]


# ═══════════════════════ 예외 ═══════════════════════
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores(DATA / "empty.csv")
    assert kept == []
    assert skipped == []


@pytest.mark.parametrize("본문", ["가,80,비고\n", "가\n"])
def test_열_개수가_2가_아니면_건너뛰고_기록한다(tmp_path, 본문):
    kept, skipped = load_scores(만들기(tmp_path, 본문))
    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][2] == "열 개수가 2가 아님"


def test_점수가_비어_있으면_건너뛰고_기록한다(tmp_path):
    kept, skipped = load_scores(만들기(tmp_path, "가,\n"))
    assert kept == []
    assert skipped == [(2, "가,", "점수가 비어 있음")]


@pytest.mark.parametrize("점수", ["결석", "88.5", "7 2", "abc"])
def test_점수가_정수가_아니면_건너뛰고_기록한다(tmp_path, 점수):
    kept, skipped = load_scores(만들기(tmp_path, f"가,{점수}\n"))
    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][2] == "점수가 정수가 아님"


@pytest.mark.parametrize("본문", [",90\n", "   ,90\n"])
def test_이름이_비어_있으면_건너뛰고_기록한다(tmp_path, 본문):
    kept, skipped = load_scores(만들기(tmp_path, 본문))
    assert kept == []
    assert len(skipped) == 1
    assert skipped[0][2] == "이름이 비어 있음"


def test_이상한_파일에서도_죽지_않고_유효한_줄만_남긴다():
    kept, skipped = load_scores(DATA / "weird.csv")
    assert kept == [("한겨울", 77), ("윤보람", 88)]
    assert len(skipped) == 7


# ═══════════════════════ 명령줄 실행 ═══════════════════════
def test_명령줄로_직접_실행하면_결과를_출력한다():
    # README 의 실행 명령(python3 load_scores.py scores.csv)과 같은 경로를 시험한다.
    원래_argv = sys.argv
    sys.argv = ["load_scores.py", str(DATA / "scores.csv")]
    출력 = io.StringIO()
    try:
        with contextlib.redirect_stdout(출력):
            runpy.run_path(str(DATA / "load_scores.py"), run_name="__main__")
    finally:
        sys.argv = 원래_argv
    글 = 출력.getvalue()
    assert "읽은 줄 : 5개" in 글
    assert "건너뛴 줄 : 5개" in 글


# ═══════════════════════ 경계값 ═══════════════════════
@pytest.mark.parametrize(
    "점수, 유효한가",
    [
        (-1, False),   # 경계 바로 아래
        (0, True),     # ★ 아래쪽 경계
        (1, True),
        (99, True),
        (100, True),   # ★ 위쪽 경계
        (101, False),  # 경계 바로 위
    ],
)
def test_점수_경계값(tmp_path, 점수, 유효한가):
    kept, skipped = load_scores(만들기(tmp_path, f"가,{점수}\n"))
    assert (len(kept) == 1) == 유효한가
    if not 유효한가:
        assert skipped[0][2] == "점수가 0~100 밖"
