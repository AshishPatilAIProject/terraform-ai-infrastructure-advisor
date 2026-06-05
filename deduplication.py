def deduplicate_findings(findings):
    seen = set()
    unique = []

    for finding in findings:

        title = finding["title"].lower()

        if title not in seen:
            seen.add(title)
            unique.append(finding)

    return unique