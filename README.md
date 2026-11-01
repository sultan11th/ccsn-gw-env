# CCSN-GW + ML: a personal research environment for an AI agent

A local, citation-grounded working environment in which the
[AI4Science](https://github.com/andkhalov/AI4Science) agent (YSDA course
"AI assistants for researchers") answers questions about **gravitational waves
from core-collapse supernovae and machine learning** from my own library of
papers, cites every claim by file and line range, and logs its work.

| Component | Where | What it does |
|---|---|---|
| Contract | [`AGENT.md`](AGENT.md) | Rules the agent reads at start-up: goal, data, tools, citation and verification rules, journal, forbidden actions |
| Library | [`literature/catalog.yaml`](literature/catalog.yaml), `literature/md/` | 43 papers (12 mine + 31 external) converted from arXiv to Markdown |
| Ontology | [`ontology/concepts.yaml`](ontology/concepts.yaml), [`ontology/graph.md`](ontology/graph.md) | 41 concepts, 6 relation types, rendered as a Mermaid graph |
| Search | [`src/search.py`](src/search.py) | BM25 over paragraph chunks with ontology synonyms; citations `file:Lstart-Lend § section` |
| Journal | [`diary.md`](diary.md) | Append-only work log |
| Agent runtime | [`src/agent.py`](src/agent.py), [`src/llm_proxy.py`](src/llm_proxy.py) | The course agent (Goose) on a local model (vLLM or Ollama) or DeepSeek; `ai4science` also works |
| Evaluation | [`eval/queries.yaml`](eval/queries.yaml), `results/` | Example queries, retrieval check, agent transcripts |
| Report | [`REPORT.md`](REPORT.md) | Course submission |

## Quick start

Requirements: Python 3.10+, [pandoc](https://pandoc.org/installing.html) ≥ 2.19, the
AI4Science agent installed as described in its README (it provides Goose), and
a local model server ([vLLM](https://docs.vllm.ai) on a GPU, or [Ollama](https://ollama.com)).

```bash
pip install -r requirements.txt
make fetch        # download and convert the 43 active papers (arXiv asks for ≥3 s between requests)
make index        # build the search index
make test         # self-test: prints "selftest OK"
make queries      # retrieval check of the example queries -> results/queries/RETRIEVAL.md
```

Use the library directly:

```bash
python3 src/search.py "f_peak dependence on the EOS" -k 5
python3 src/search.py "SHAP" --own                 # only my papers
python3 src/search.py --exact "772" --file richers2017
python3 src/ontology.py show beta                  # concept card for T/|W|
```

### Running the agent

The agent is Goose (the engine of the course's `ai4science`) with this project's
`AGENT.md`. The same agent can run on three model backends; only the model changes:

| Backend | Command | Model (default) | Cost / limit |
|---|---|---|---|
| Local | `python3 src/agent.py --backend local` | Qwen3-Coder-30B-A3B FP8 via vLLM | free, no limit |
| DeepSeek | `python3 src/agent.py --backend deepseek` | `deepseek-flash` via the DeepSeek API | pay per token |
| Course | `ai4science` (`/model deepseek` to switch) | `qwen3.6-35b-a3b` via Yandex AI Studio | 3M tokens/day |

Plan: debug the whole workflow on the local model, then run the final experiments on DeepSeek.

```bash
cp .env.example .env                 # set AI4SCIENCE_HOME and, later, DEEPSEEK_API_KEY
# local model server (GPU): Qwen3-Coder-30B-A3B in FP8 with tool calling
vllm serve Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8 --served-model-name qwen3-coder-30b \
  --max-model-len 65536 --gpu-memory-utilization 0.92 --enable-auto-tool-choice --tool-call-parser qwen3_coder
# (no suitable GPU: Ollama `qwen3-coder:30b`, then LOCAL_URL=http://localhost:11434 in .env)
python3 src/agent.py --backend local --dry-run run "test"           # check the settings
python3 src/agent.py --backend local                                # interactive session
python3 src/agent.py --backend local run "How does f_peak depend on the EOS?"
make agent-local                     # all example queries -> results/agent_runs/local/
make agent-deepseek                  # the same on DeepSeek -> results/agent_runs/deepseek/
```

`src/agent.py` reuses the Goose binary and the course instructions from your AI4Science
clone, adds `AGENT.md` to the system prompt, and gives the agent Goose's shell and file
tools. A small local proxy (`src/llm_proxy.py`) adds the API key, switches DeepSeek's
thinking mode off (with thinking on, DeepSeek rejects tool-using turns unless the client sends
its reasoning back, and Goose is not built for that), and logs token usage to `results/agent_runs/usage.jsonl`.

If arXiv refuses a download, fetch the source or PDF in a browser and convert it with
`python3 src/fetch_arxiv.py <key> --local <file>`.

## Repository layout

```
AGENT.md              contract for the agent
REPORT.md             course report (Appendix A = AGENT.md, kept in sync by the self-test)
diary.md              work journal
data/                 raw data, read-only
literature/
  catalog.yaml        bibliographic truth (45 entries, 43 active)
  md/                 converted papers (only my own papers are committed)
  raw/                downloads (not committed)
ontology/
  concepts.yaml       concepts and relations
  graph.md            generated Mermaid graph
eval/queries.yaml     example queries with expected answers
index/                search index (generated, not committed)
results/              retrieval check, agent transcripts, answers
src/
  fetch_arxiv.py      arXiv -> Markdown (LaTeX, then HTML, then PDF)
  build_index.py      chunking + index
  search.py           library search (standard library only)
  textnorm.py         shared normalisation of physics notation
  ontology.py         validate / graph / show / list
  run_queries.py      retrieval check and agent runs
  agent.py            course agent (Goose) with a local model (vLLM/Ollama) or DeepSeek
  llm_proxy.py        local proxy: API key, request fields, token log
tests/selftest.py     offline self-test on synthetic fixtures + consistency checks
paper/                manuscript drafts
```

## Licensing of the library

Most arXiv papers are distributed under arXiv's non-exclusive licence, which does not
permit redistribution, so converted papers are not committed (see `.gitignore`); anyone can
rebuild them with `make fetch`. Only my own papers are committed. Before committing an
external paper, check that its arXiv licence is CC BY (shown on its abstract page).
