from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from ..services.parser_service import parse_srt_bytes
from ..services.align_service import align_greedy_time
from ..models.schemas import CorpusResponse

router = APIRouter(prefix="/api/corpus", tags=["corpus"])

@router.post("/align", response_model=CorpusResponse)
async def align_corpus(
    en_srt: UploadFile = File(..., description="English .srt"),
    si_srt: UploadFile = File(..., description="Sinhala .srt"),
    window_ms: int = Query(700, ge=0, le=4000, description="Near-miss tolerance in ms")
):
    if not (en_srt.filename.lower().endswith(".srt") and si_srt.filename.lower().endswith(".srt")):
        raise HTTPException(status_code=400, detail="Both uploads must be .srt")

    en_bytes = await en_srt.read()
    si_bytes = await si_srt.read()

    en = parse_srt_bytes(en_bytes)
    si = parse_srt_bytes(si_bytes)
    if not en or not si:
        raise HTTPException(status_code=400, detail="Failed to parse one or both SRT files")

    items = align_greedy_time(en, si, window_ms=window_ms)

    return CorpusResponse(
        count=len(items),
        items=items
    )
