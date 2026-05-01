import pytest
from reports import clickbait_report


@pytest.fixture
def sample_rows():
    return [
        {"title": "Кликбейт А", "ctr": "25.0", "retention_rate": "22"},
        {"title": "Кликбейт Б", "ctr": "18.2", "retention_rate": "35"},
        {"title": "Высокое удержание", "ctr": "16.5", "retention_rate": "42"},
        {"title": "Низкий CTR", "ctr": "14.2", "retention_rate": "30"},
        {"title": "Обычное видео", "ctr": "9.5", "retention_rate": "82"},
    ]


class TestClickbaitReportFiltering:
    def test_includes_matching_videos(self, sample_rows):
        result = clickbait_report(sample_rows)
        titles = [r["title"] for r in result]
        assert "Кликбейт А" in titles
        assert "Кликбейт Б" in titles

    @pytest.mark.parametrize("title", ["Высокое удержание", "Низкий CTR", "Обычное видео"])
    def test_excludes_non_matching(self, sample_rows, title):
        result = clickbait_report(sample_rows)
        assert title not in [r["title"] for r in result]

    def test_empty_input(self):
        assert clickbait_report([]) == []

    def test_no_matches(self):
        rows = [{"title": "Видео", "ctr": "5.0", "retention_rate": "80"}]
        assert clickbait_report(rows) == []


class TestClickbaitReportBoundaries:
    @pytest.mark.parametrize("ctr,retention,expected_count", [
        ("15.0", "30", 0),
        ("15.1", "30", 1),
        ("20.0", "40", 0),
        ("20.0", "39", 1),
    ])
    def test_boundary_values(self, ctr, retention, expected_count):
        rows = [{"title": "Тест", "ctr": ctr, "retention_rate": retention}]
        assert len(clickbait_report(rows)) == expected_count


class TestClickbaitReportOutput:
    def test_sorted_by_ctr_descending(self, sample_rows):
        result = clickbait_report(sample_rows)
        ctrs = [r["ctr"] for r in result]
        assert ctrs == sorted(ctrs, reverse=True)

    def test_output_columns(self, sample_rows):
        result = clickbait_report(sample_rows)
        for row in result:
            assert set(row.keys()) == {"title", "ctr", "retention_rate"}

    def test_values_are_floats(self, sample_rows):
        result = clickbait_report(sample_rows)
        for row in result:
            assert isinstance(row["ctr"], float)
            assert isinstance(row["retention_rate"], float)
            