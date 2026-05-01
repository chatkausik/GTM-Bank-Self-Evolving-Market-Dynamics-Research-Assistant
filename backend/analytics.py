from collections import defaultdict


def compute_analytics(memories: list[dict]) -> dict:
    if not memories:
        return {
            "by_category": [], "by_segment": [], "coverage_gaps": [],
            "timeline": [], "total": 0, "wins": 0, "failures": 0, "win_rate": 0,
        }

    cat_stats: dict[str, dict] = defaultdict(lambda: {"wins": 0, "failures": 0})
    seg_stats: dict[str, dict] = defaultdict(lambda: {"wins": 0, "failures": 0})
    timeline_raw: dict[str, dict] = defaultdict(lambda: {"wins": 0, "failures": 0})

    for m in memories:
        cat = m.get("product_category", "Unknown")
        seg = m.get("merchant_segment", "Unknown")
        ts  = m.get("timestamp", "")
        month = ts[:7] if ts else "Unknown"
        key = "wins" if m["outcome_type"] == "success" else "failures"
        cat_stats[cat][key]      += 1
        seg_stats[seg][key]      += 1
        timeline_raw[month][key] += 1

    def to_list(stats, sort_key="total"):
        rows = [
            {"label": k, "wins": v["wins"], "failures": v["failures"],
             "total": v["wins"] + v["failures"]}
            for k, v in stats.items()
        ]
        return sorted(rows, key=lambda x: -x[sort_key])

    by_category = to_list(cat_stats)
    by_segment  = to_list(seg_stats)

    coverage_gaps = [s["label"] for s in by_segment if s["wins"] == 0]
    underrepresented = [s["label"] for s in by_segment if s["total"] == 1]

    timeline = sorted(
        [{"month": k, "wins": v["wins"], "failures": v["failures"]}
         for k, v in timeline_raw.items()],
        key=lambda x: x["month"],
    )

    total    = len(memories)
    wins     = sum(1 for m in memories if m["outcome_type"] == "success")
    failures = total - wins

    return {
        "by_category":     by_category,
        "by_segment":      by_segment,
        "coverage_gaps":   coverage_gaps,
        "underrepresented": underrepresented,
        "timeline":        timeline,
        "total":           total,
        "wins":            wins,
        "failures":        failures,
        "win_rate":        round(wins / total * 100) if total else 0,
    }
