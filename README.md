# srt-to-parallel-corpora
# Parallel Corpus API (EN↔SI)
a simple python system that takes in two parallel srt subtitle files in different languages and and responses with a parelle-corpora. hehehehehehe

## Run
docker build -t parallel-corpus-api .
docker run -p 8000:8000 parallel-corpus-api

Open http://localhost:8000/docs

## Test (curl)
curl -X POST "http://localhost:8000/api/corpus/align?window_ms=700" \
  -F "en_srt=@/path/to/english.srt" \
  -F "si_srt=@/path/to/sinhala.srt"
