# AGENT.md — Gravitational waves from core-collapse supernovae + machine learning

This file is the contract between the researcher (Sultan Abylkairov) and the
course agent (Goose, as packaged by AI4Science), whichever open-weight model runs it:
a local model through Ollama, DeepSeek, or the Yandex AI Studio models of `ai4science`.
Its rules refine the agent's general instructions for this project.

## 1. Project goal
Answer research questions about gravitational waves (GWs) from core-collapse
supernovae (CCSNe) and the machine-learning (ML) methods used to analyse them —
the rotating-core bounce signal, the nuclear equation of state (EOS), rotation
(T/|W|), the peak frequency f_peak, detector reach and ML validation — using the
**local library** in this repository, with every claim traceable to a source.

**Language:** work and answer in English (this overrides the agent's default
language). Code and identifiers in English.

## 2. Data and context (what lives where)
| Path | Content | Access |
|---|---|---|
| `data/` | Raw data (e.g. waveform files) | read-only |
| `literature/catalog.yaml` | Bibliographic truth: key, arXiv ID, venue, DOI, own paper or not | edit only when asked |
| `literature/md/<key>.md` | Papers converted from arXiv to Markdown | read-only (regenerate with `src/fetch_arxiv.py`) |
| `literature/raw/` | Original downloads (LaTeX, HTML, PDF) | read-only |
| `ontology/concepts.yaml` | Concepts of the topic and their relations | edit only when asked |
| `index/` | Search index (generated) | do not edit |
| `src/` | Scripts | |
| `results/` | All derived files (answers, tables, figures) | write here |
| `diary.md` | Work journal | append-only |

## 3. Tools for the local context (run them with the shell)
- **Search the library:** `python3 src/search.py "<query>" -k 8`
  - `--own` only my papers; `--file <key>` one paper; `--exact "<string>"` chunks
    containing an exact string (numbers, EOS names); `--json` machine-readable.
  - `python3 src/search.py --papers` lists the indexed papers.
- **Look up a concept:** `python3 src/ontology.py show <concept or synonym>`
  (definition, relations, source papers). `python3 src/ontology.py list` lists all.
- **Read the cited passage:** `sed -n '<start>,<end>p' literature/md/<key>.md`.
- After the library changes: `python3 src/build_index.py`.

## 4. How to work
1. **Search before answering.** For any factual question run `search.py` first.
   Try synonyms (the ontology lists them) before concluding something is absent.
2. **Read before citing.** Open the passage with `sed -n` and check that it really
   says what you claim.
3. **Cite every factual sentence** in the form the search prints:
   `[literature/md/<key>.md:L<start>-L<end> § <section>]`.
   Only cite passages that the search returned in this session.
4. **Quote numbers exactly**, with units and conditions (detector, distance,
   orientation, SNR, accuracy threshold, EOS set).
5. **Separate source from inference:** "Paper X reports …" vs. "I infer …".
6. **If the library has no answer, say so:** "Not found in the local library
   (searched: …)". Then propose a paper to add. Never fill gaps from memory.
7. **Bibliographic details come only from `literature/catalog.yaml`.** Do not copy
   references from other papers' reference lists without checking the catalog.
8. **Computations** are done by Python scripts in `src/`, outputs saved to
   `results/`. Run code before reporting its result.
9. **Terminology:** write T/|W| for the rotation ratio (β only as a search synonym),
   f_peak, EOS; distances in kpc, frequencies in Hz, strain amplitudes as quoted
   by the source (state the reference distance, e.g. "at 10 kpc").
10. **Web and PDF tools** (`web_search`, `pdf_read`, …) only when the user asks
    to add or check a paper. A paper enters the library only through
    `src/fetch_arxiv.py` and a catalog row.

## 5. Verification (every conclusion states how to check it)
Each answer ends with a **Verification** line that lets anyone re-check it
independently, for example:
- `sed -n '210,224p' literature/md/richers2017.md` — the cited passage;
- `python3 src/search.py --exact "772" --file richers2017` — the quoted number;
- the table, figure or equation number in the source;
- the script and command that produced a computed result.

## 6. Journal
After each task append to `diary.md` (never edit earlier entries):

```
## YYYY-MM-DD HH:MM — <short title>
- Request: <user request>
- Model: <model alias>
- Actions: <commands run>
- Result: <answer in one or two sentences, with citations>
- Verification: <how to re-check>
- Open issues: <what remains unclear, or "none">
```

## 7. Forbidden
- Modifying, moving or deleting anything in `data/`, `literature/raw/` or
  `literature/md/` by hand.
- Inventing papers, authors, arXiv IDs, DOIs, numbers, equations or section names.
- Stating a conclusion without a citation and a verification method.
- Citing a passage that `search.py` did not return in this session.
- Committing `.env` or API keys.

## 8. Definition of done
An answer is done when it has: (1) citations for every factual claim,
(2) a Verification line, (3) a saved copy in `results/answers/` when the user
asks for a written result, and (4) a `diary.md` entry.
