from typing import Protocol, TypedDict


class VideoRow(TypedDict):
    title: str
    ctr: str
    retention_rate: str
    views: str
    likes: str
    avg_watch_time: str


class Report(Protocol):
    def __call__(self, rows: list[VideoRow]) -> list[dict]: ...


def clickbait_report(rows: list[VideoRow]) -> list[dict]:
    filtered = [
        {
            "title": row["title"],
            "ctr": float(row["ctr"]),
            "retention_rate": float(row["retention_rate"]),
        }
        for row in rows
        if float(row["ctr"]) > 15 and float(row["retention_rate"]) < 40
    ]
    return sorted(filtered, key=lambda r: r["ctr"], reverse=True)


REPORTS: dict[str, Report] = {
    "clickbait": clickbait_report,
}
