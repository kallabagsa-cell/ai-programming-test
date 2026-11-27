# test_ai_B.py — 프롬프트 B (명세 6칸만 줌, 코드는 주지 않음)
# ※ 이 파일은 load_scores.py 헤더의 명세 요약만 근거로 작성한 것입니다 (수정 없이 저장).
#   명세에 없는 것(이유 문구의 정확한 글자, 헤더 이름)은 단정하지 않습니다.
import pytest

from load_scores import load_scores


def make_csv(tmp_path, body):
    p = tmp_path / "data.csv"
    p.write_text("name,score\n" + body, encoding="utf-8")
    return str(p)


# ---------- 정상 ----------
def test_returns_valid_rows_in_order(tmp_path):
    kept, skipped = load_scores(make_csv(tmp_path, "가,80\n나,90\n"))
    assert kept == [("가", 80), ("나", 90)]
    assert skipped == []


def test_score_is_int(tmp_path):
    kept, _ = load_scores(make_csv(tmp_path, "가,80\n"))
    assert isinstance(kept[0][1], int)


def test_blank_line_is_skipped_silently(tmp_path):
    kept, skipped = load_scores(make_csv(tmp_path, "가,80\n\n나,90\n"))
    assert len(kept) == 2
    assert skipped == []


def test_duplicate_names_are_not_removed(tmp_path):
    # 명세 ★: 같은 이름이 두 번 나와도 지우지 않고 둘 다 남긴다
    kept, _ = load_scores(make_csv(tmp_path, "가,80\n가,90\n"))
    assert kept == [("가", 80), ("가", 90)]


# ---------- 예외 ----------
def test_missing_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(str(tmp_path / "nope.csv"))


def test_header_only_returns_two_empty_lists(tmp_path):
    assert load_scores(make_csv(tmp_path, "")) == ([], [])


@pytest.mark.parametrize("body", ["가,80,90\n", "가\n"])
def test_wrong_column_count_is_skipped_and_recorded(tmp_path, body):
    kept, skipped = load_scores(make_csv(tmp_path, body))
    assert kept == []
    assert len(skipped) == 1
    line_no, original, reason = skipped[0]
    assert line_no == 2
    assert reason


@pytest.mark.parametrize("score", ["", "abc", "88.5"])
def test_empty_or_non_integer_score_is_skipped_and_recorded(tmp_path, score):
    kept, skipped = load_scores(make_csv(tmp_path, f"가,{score}\n"))
    assert kept == []
    assert len(skipped) == 1


def test_empty_name_is_skipped_and_recorded(tmp_path):
    kept, skipped = load_scores(make_csv(tmp_path, ",80\n"))
    assert kept == []
    assert len(skipped) == 1


def test_one_bad_line_does_not_stop_the_rest(tmp_path):
    kept, skipped = load_scores(make_csv(tmp_path, "가,80\n나,abc\n다,90\n"))
    assert [n for n, _ in kept] == ["가", "다"]
    assert [ln for ln, _, _ in skipped] == [3]


# ---------- 경계값 ----------
@pytest.mark.parametrize(
    "score, valid",
    [(-1, False), (0, True), (1, True), (99, True), (100, True), (101, False)],
)
def test_score_range_boundaries(tmp_path, score, valid):
    kept, skipped = load_scores(make_csv(tmp_path, f"가,{score}\n"))
    assert len(kept) == (1 if valid else 0)
    assert len(skipped) == (0 if valid else 1)
