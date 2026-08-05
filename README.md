# Applied AI System: Game Glitch Investigator + Auto-Solver Agent

## Base Project
This project extends my Module 1 submission, **Game Glitch Investigator**
(originally at `ai110-module1show-gameglitchinvestigator-starter`), a Streamlit
number-guessing game with hint logic, scoring, and a small pytest suite.

For this final project, I extended it with an **agentic AI feature**: an
autonomous agent that plays the game on its own, demonstrating a full
plan -> act -> check -> guardrail loop integrated directly with the game's
existing logic (`logic_utils.py`).

## What It Does
- The original game lets a human guess a secret number with hints (Higher/Lower).
- The new `agent.py` module adds an **AutoSolverAgent** that:
  - **Plans** its next guess using binary search over the valid range
  - **Acts** by submitting that guess through the game's real `check_guess()` function
  - **Checks** that each hint is logically consistent with prior guesses (a guardrail
    against buggy/contradictory hints, which was the original bug in this game)
  - **Logs** every step to `agent_log.txt` for auditability
  - Repeats until it wins or a guardrail trips, instead of looping forever

This is not a separate script bolted on the side — the agent calls the same
`check_guess()` and `get_range_for_difficulty()` functions the human-facing
game uses, so it is testing and exercising the real game logic.

## Setup
1. Clone this repo and enter the folder.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the original human-playable game:
   ```
   python -m streamlit run app.py
   ```
4. Run the autonomous agent on its own:
   ```
   python3 agent.py
   ```
5. Run the automated test suite:
   ```
   python3 -m pytest tests/ -v
   ```

## Architecture
See `diagrams/architecture.mmd` for the full Mermaid source diagram, showing
input -> agentic loop -> output, plus where logging and pytest provide
human-checkable oversight.

## Example Runs

**Example 1 — Agent solves a Normal-difficulty game:**
```
$ python3 agent.py
{'solved': True, 'attempts': 6, 'history': [(50, 'Too High'), (25, 'Too Low'), (37, 'Too Low'), (43, 'Too Low'), (46, 'Too High'), (44, 'Win')]}
```

**Example 2 — Automated test suite (reliability evidence):**
```
$ python3 -m pytest tests/test_agent.py -v
tests/test_agent.py::test_agent_solves_easy PASSED
tests/test_agent.py::test_agent_solves_normal PASSED
tests/test_agent.py::test_agent_solves_within_log2_attempts PASSED
tests/test_agent.py::test_agent_solves_edge_low PASSED
tests/test_agent.py::test_agent_solves_edge_high PASSED
tests/test_agent.py::test_agent_fails_gracefully_with_low_max_attempts PASSED
6 passed in 0.01s
```

**Example 3 — Guardrail path (forced failure, proves error handling isn't just theoretical):**
```
$ python3 -c "from agent import AutoSolverAgent; print(AutoSolverAgent(secret=99, max_attempts=1).run())"
{'solved': False, 'reason': 'max_attempts_exceeded', 'attempts': 1, 'history': [...]}
```

## Reliability Summary
6 out of 6 automated tests passed, covering: normal-range solving, easy/hard
difficulty edge cases, an upper bound on attempts (binary search should never
exceed 7 guesses on a 1-100 range), and a forced failure case to confirm the
agent fails gracefully (returns a structured result) rather than crashing or
looping forever when it can't finish in time.

## Reflection
See `model_card.md` for limitations, misuse considerations, and a description
of AI collaboration during this project.
