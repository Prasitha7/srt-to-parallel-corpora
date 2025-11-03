from typing import List, Dict, Any, Tuple

def _overlap(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    start = max(a[0], b[0])
    end = min(a[1], b[1])
    return max(0.0, end - start)

def align_greedy_time(
    en: List[Dict[str, Any]],
    si: List[Dict[str, Any]],
    window_ms: int = 700
) -> List[Dict[str, Any]]:
    """
    Greedy alignment using time overlap with a near-miss tolerance (window_ms).
    Returns a list of dicts with keys: en, si, start, end, overlap_ms, confidence
    """
    i = j = 0
    tol = window_ms / 1000.0
    pairs = []

    while i < len(en) and j < len(si):
        e, s = en[i], si[j]
        ov = _overlap((e["start"], e["end"]), (s["start"], s["end"]))

        if ov > 0:
            dur = max(e["end"] - e["start"], s["end"] - s["start"])
            conf = min(1.0, ov / max(0.25, dur))
            pairs.append({
                "en": e["text"], "si": s["text"],
                "start": min(e["start"], s["start"]),
                "end":   max(e["end"], s["end"]),
                "overlap_ms": int(ov * 1000),
                "confidence": round(conf, 3),
            })
            i += 1; j += 1
        else:
            # near-miss soft pairing if segments are within tolerance
            gap = min(abs(e["end"] - s["start"]), abs(s["end"] - e["start"]))
            if gap <= tol:
                dur = max(e["end"] - e["start"], s["end"] - s["start"])
                conf = max(0.1, 1.0 - (gap / (tol + 1e-6)))
                pairs.append({
                    "en": e["text"], "si": s["text"],
                    "start": min(e["start"], s["start"]),
                    "end":   max(e["end"], s["end"]),
                    "overlap_ms": 0,
                    "confidence": round(min(0.8, conf * 0.8), 3),
                })
                i += 1; j += 1
            else:
                if e["end"] < s["end"]:
                    i += 1
                else:
                    j += 1

    return pairs
