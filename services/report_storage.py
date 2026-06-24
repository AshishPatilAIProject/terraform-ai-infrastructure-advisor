import os


def save_report(
    html: str
):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    report_path = os.path.join(
        "reports",
        "report.html"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as f:
        f.write(html)

    return report_path