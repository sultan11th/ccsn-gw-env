# Common tasks. Run from the repository root.
PY ?= python3

.PHONY: all fetch index graph test queries agent-local agent-deepseek agent-course check-bib lock unlock

all: fetch index graph test queries   ## build the library and verify everything

fetch:            ## download and convert all active papers (about 3 s per request to arXiv)
	$(PY) src/fetch_arxiv.py --all

index:            ## build the search index
	$(PY) src/build_index.py

graph:            ## validate the ontology and regenerate ontology/graph.md
	$(PY) src/ontology.py validate
	$(PY) src/ontology.py graph

test:             ## self-test (offline fixtures + repository consistency)
	$(PY) tests/selftest.py

queries:          ## retrieval check of eval/queries.yaml -> results/queries/RETRIEVAL.md
	$(PY) src/run_queries.py

agent-local:      ## all example queries with Goose + local model (vLLM or Ollama), in a sandbox
	$(PY) src/run_queries.py --agent local

agent-deepseek:   ## all example queries with Goose + DeepSeek API (DEEPSEEK_API_KEY in .env)
	$(PY) src/run_queries.py --agent deepseek

agent-course:     ## all example queries with the course wrapper (Yandex AI Studio, 3M tokens/day)
	$(PY) src/run_queries.py --agent course:qwen

check-bib:        ## compare literature/catalog.yaml with arXiv metadata
	$(PY) src/fetch_arxiv.py --check

LOCKED = data literature/md literature/raw ontology/concepts.yaml literature/catalog.yaml AGENT.md

lock:             ## make data, papers, ontology, catalog and AGENT.md read-only (before an interactive agent session)
	@for p in $(LOCKED); do [ -e $$p ] && find $$p -type f -exec chmod a-w {} + ; done; echo "locked: $(LOCKED)"

unlock:           ## undo `make lock` (needed before make fetch / graph or editing these files)
	@for p in $(LOCKED); do [ -e $$p ] && find $$p -type f -exec chmod u+w {} + ; done; echo "unlocked"
