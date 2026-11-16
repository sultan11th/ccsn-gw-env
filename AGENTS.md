# AGENTS.md — Gravitational waves from core-collapse supernovae + machine learning

Contract between the researcher (Sultan Abylkairov) and the agent (Goose with Qwen3 or
DeepSeek). It overrides the agent's general instructions. **Answer in English.**

## 1. Every question: follow these steps
1. **Search:** `python3 src/search.py "<query>" -k 8`. If the hits are weak, try a synonym
   (`python3 src/ontology.py show <term>` lists them) before saying something is missing.
2. **Read:** `sed -n '<start>,<end>p' literature/md/<key>.md` for each passage you will use.
3. **Answer:** short, every factual sentence followed by its citation, copied exactly
   from the search output: `[literature/md/<key>.md:L<start>-L<end> § <section>]`.
4. **Finish** with three lines: `Summary:` (one sentence), `Verification:` (commands that
   re-check the answer), `Open issues:` (or "none").

Questions about the simulation data use `python3 src/data.py` instead of the search (§3).
If nothing relevant is found, answer: "Not found in the local library (searched: <queries>)."

## 2. Example of a finished answer
```
Richers et al. report that in the linear regime the bounce-signal amplitude depends
approximately linearly on T/|W| [literature/md/richers2017.md:L237-L247 § Results > The Bounce Signal].
I infer that faster rotators give proportionally stronger bounce signals at the same distance.

Summary: Bounce amplitude grows about linearly with T/|W| at low rotation (Richers et al. 2017).
Verification: sed -n '237,247p' literature/md/richers2017.md
Open issues: none
```

## 3. Tools (the only commands you need)
| Task | Command |
|---|---|
| Search papers | `python3 src/search.py "<query>" -k 8` (`--own` my papers, `--file <key>`, `--exact "<string>"`, `--papers`) |
| Read a passage | `sed -n '<start>,<end>p' literature/md/<key>.md` (at most 40 lines at a time) |
| Concept, synonyms, evidence, data columns | `python3 src/ontology.py show <term>` |
| Dataset overview | `python3 src/data.py info` and `python3 src/data.py columns` |
| Select simulations | `python3 src/data.py params --where "eos==SFHo" --where "beta_ic_b>=0.05" --cols f_peak,delta_dh` |
| Statistics | `python3 src/data.py stats f_peak --by eos`, `python3 src/data.py corr beta_ic_b delta_dh` |
| One waveform | `python3 src/data.py strain <run_id>` (`--every 10` samples, `--out results/x.csv`) |

**Data:** 7,438 rotating core-collapse simulations (3 progenitors × 18 EOS × 138 rotation
profiles). `data/data/parameters.csv` has `run_id` + 30 parameters (e.g. `beta_ic_b` = T/|W|
of the inner core at bounce, `delta_dh` = bounce amplitude in cm, `f_peak` in Hz);
`data/data/timeseries/strain.csv.gz` has D·h+ in cm from −1.95 to +5.98 ms (t = 0 at bounce).
Row *i* is the same simulation in both files. Derived parameters come from the full-length
data, so do not recompute them from the trimmed strain.

## 4. Rules
- Cite only passages that `search.py` (or `ontology.py show` as evidence) printed in this session; quote numbers exactly, with
  units and conditions (detector, distance e.g. "at 10 kpc", SNR, accuracy threshold, EOS set).
- Write "Paper X reports …" for sources and "I infer …" for your own reasoning.
- Bibliographic details (authors, year, venue, DOI) only from `literature/catalog.yaml`.
- Terms: T/|W| (not β), f_peak, EOS; kpc, Hz.
- Computed results: run the command, then report its output; save files only in `results/`.
- Web and PDF tools only when the user asks to add or check a paper.

## 5. Forbidden
- `cat`, `grep -r`, `find`, `head` or `less` on `literature/` or `data/`, `zcat` or pandas on `data/`:
  outputs are too long. Use `search.py`, `sed -n` on a short range and `data.py`.
- Reading `eval/`, `results/agent_runs/` or `results/answers/` (they contain expected answers).
- Changing `data/`, `literature/`, `ontology/`, `index/` or `AGENTS.md`.
- Inventing papers, authors, arXiv IDs, DOIs, numbers, equations or section names.
- Committing `.env` or API keys.

## 6. Verification of the data and the analysis (HW2)
One command runs the whole verifier (contract C1-C14, mutation tests, physical properties
P1-P7, the EOS-grouped split, the statistics code and `data.py`); see `METHOD.md`:

```
python3 -m unittest discover -s checks -v
```

It uses the full data in `data/data/` when present, otherwise the committed fragment
`checks/fixtures/data/` (810 runs); `CCSN_DATA=<dir>` selects a directory. The experiment of
`METHOD.md` §7 runs step by step: `python3 scripts/amp_experiment.py dry|smoke|sweep|full`.
Do not edit `checks/` or `METHOD.md` (they are locked by `make lock`); if a check fails,
report it instead of changing the check.

## 7. Journal
`src/agent.py run` writes the `diary.md` entry itself: do not edit `diary.md`. In an
interactive session, end the task with one command:
`python3 src/diary.py --request "..." --actions "..." --result "..." --verification "..." --open "none"`.
