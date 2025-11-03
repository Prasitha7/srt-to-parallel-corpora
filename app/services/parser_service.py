import srt
from datetime import timedelta
from typing import List, Dict, Any

def _seconds(td: timedelta) -> float:
    return td.total_seconds()

def parse_srt_bytes(content: bytes) -> List[Dict[str, Any]]:
    """
    Return list of {text, start, end} from SRT bytes.
    """
    text = content.decode(errors="ignore")
    subs = list(srt.parse(text))
    return [{
        "text": " ".join(s.content.replace("\n", " ").split()),
        "start": _seconds(s.start),
        "end": _seconds(s.end),
    } for s in subs]
