# test_ai_A.py — 프롬프트 A (load_scores.py 코드 전체를 줌)
# ※ 이 파일은 같은 대화에서 코드를 본 상태로 Claude가 작성한 것입니다 (수정 없이 저장).
import pytest

from load_scores import load_scores, MIN_SCORE, MAX_SCORE


def write_csv(tmp_path, text, name="scores.csv"):
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return str(p)


# ---------- 정상 ----------
def test_valid_rows(tmp_path):
    path = write_csv(tmp_path, "name,score\n김하나,88\n이두리,70\n")
    kept, skipped = load_scores(path)
    assert kept == [("김하나", 88), ("이두리", 70)]
    assert skipped == []


def test_blank_lines_ignored_without_record(tmp_path):
    path = write_csv(tmp_path, "name,score\n김하나,88\n\n이두리,70\n")
    kept, skipped = load_scores(path)
    assert len(kept) == 2
    assert skipped == []


def test_duplicate_names_are_both_kept(tmp_path):
    path = write_csv(tmp_path, "name,score\n김하나,88\n김하나,91\n")
    kept, skipped = load_scores(path)
    assert kept == [("김하나", 88), ("김하나", 91)]


def test_whitespace_is_stripped(tmp_path):
    path = write_csv(tmp_path, "name,score\n  김하나  ,  88  \n")
    kept, skipped = load_scores(path)
    assert kept == [("김하나", 88)]


def test_utf8_bom_header(tmp_path):
    p = tmp_path / "bom.csv"
    p.write_text("name,score\n김하나,88\n", encoding="utf-8-sig")
    kept, skipped = load_scores(str(p))
    assert kept == [("김하나", 88)]


def test_quoted_name_with_comma(tmp_path):
    path = write_csv(tmp_path, 'name,score\n"최,네번",77\n')
    kept, skipped = load_scores(path)
    assert kept == [("최,네번", 77)]


# ---------- 예외 ----------
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_scores("does_not_exist.csv")


def test_header_only(tmp_path):
    path = write_csv(tmp_path, "name,score\n")
    assert load_scores(path) == ([], [])


def test_wrong_column_count(tmp_path):
    path = write_csv(tmp_path, "name,score\n장미르,72,비고없음\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped == [(2, "장미르,72,비고없음", "열 개수가 2가 아님")]


def test_empty_name(tmp_path):
    path = write_csv(tmp_path, "name,score\n,90\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "이름이 비어 있음"


def test_empty_score(tmp_path):
    path = write_csv(tmp_path, "name,score\n박세찬,\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "점수가 비어 있음"


@pytest.mark.parametrize("raw", ["결석", "88.5", "7 2", "abc"])
def test_non_integer_score(tmp_path, raw):
    path = write_csv(tmp_path, f"name,score\n한겨울,{raw}\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "점수가 정수가 아님"


# ---------- 경계값 ----------
@pytest.mark.parametrize(
    "score, valid",
    [
        (MIN_SCORE - 1, False),
        (MIN_SCORE, True),
        (MIN_SCORE + 1, True),
        (MAX_SCORE - 1, True),
        (MAX_SCORE, True),
        (MAX_SCORE + 1, False),
    ],
)
def test_score_boundaries(tmp_path, score, valid):
    path = write_csv(tmp_path, f"name,score\n김하나,{score}\n")
    kept, skipped = load_scores(path)
    assert (len(kept) == 1) is valid
    assert (len(skipped) == 1) is (not valid)
