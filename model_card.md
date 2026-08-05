# Model Card: AutoSolverAgent (Applied AI System)

## What This System Is
`agent.py` adds an agentic AI feature to the original Game Glitch Investigator:
an `AutoSolverAgent` that autonomously plays the number-guessing game using a
plan -> act -> check -> guardrail loop, integrated directly with the existing
`logic_utils.py` functions (`check_guess`, `get_range_for_difficulty`). A
supporting pytest suite (`tests/test_agent.py`) provides a reliability/testing
layer on top of the agentic feature, covering both normal solving behavior
and forced failure cases.

## Limitations and Biases
- The agent only handles this specific type of problem: a numeric target with
  clear, binary "higher/lower" feedback. It has no ability to generalize to
  other kinds of games or ambiguous feedback.
- Its "intelligence" is really just binary search — it is not learning or
  adapting, just applying a fixed strategy. It will always converge quickly
  on a 1-100 range (≤7 guesses), but that is a property of the math, not of
  any real reasoning by the agent.
- The guardrail only checks for *logical* consistency (does a hint match the
  established range) — it cannot detect subtler bugs, like a hint that is
  consistent but still wrong for an unrelated reason.

## Potential Misuse
An auto-solver like this could, in a different context, be adapted into a
tool for automatically beating human-facing games or quizzes that use similar
guess-and-hint mechanics — for example, bypassing rate limits or "guess
attempts" restrictions meant to slow down brute-force attacks (like a PIN
code or verification-code guesser). To prevent this kind of misuse, the
guardrail logic here is scoped narrowly to *this specific game's* internal
functions, is not designed to be pointed at external systems or APIs, and is
clearly documented as a demonstration/testing agent rather than a general
brute-forcing tool.

## What Surprised Me During Testing
I expected the agent to sometimes need close to the theoretical maximum
number of guesses, but in most test runs it solved in fewer attempts than I
anticipated — the binary search strategy converged faster than I expected
even on the full 1-100 range. It reinforced for me that a very simple,
well-defined strategy can outperform intuition about how many steps a
problem "should" take.

## AI Collaboration During This Project
**Helpful suggestion:** When I got stuck figuring out how to structure the
agent, the AI suggested reusing my *existing* `check_guess()` and
`get_range_for_difficulty()` functions directly inside the agent, rather than
writing new logic from scratch. This was helpful because it kept the agent
genuinely tied to the real game logic (satisfying the "must be integrated,
not standalone" requirement) instead of being a disconnected script.

**Flawed suggestion:** At one point, the AI told me to `cd` into
`~/Documents/applied-ai-system-project` to edit my README — but that was the
wrong folder entirely; my actual project (with all my git history and
commits) was at `~/applied-ai-system-project`. This caused a confusing
moment where a `git push` was rejected and it looked like my work might be
lost. It wasn't — but it took extra troubleshooting to figure out that two
similarly-named folders existed and I'd been editing the wrong one. This was
a good reminder to double check `git log` and confirm you're in the right
directory before trusting instructions blindly, even when they come from an
AI assistant.
