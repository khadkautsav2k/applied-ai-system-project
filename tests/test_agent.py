from agent import AutoSolverAgent


def test_agent_solves_easy():
    agent = AutoSolverAgent(secret=10, difficulty="Easy")
    result = agent.run()
    assert result["solved"] is True


def test_agent_solves_normal():
    agent = AutoSolverAgent(secret=77, difficulty="Normal")
    result = agent.run()
    assert result["solved"] is True


def test_agent_solves_within_log2_attempts():
    # Binary search on 1-100 should never need more than 7 guesses.
    agent = AutoSolverAgent(secret=1, difficulty="Normal")
    result = agent.run()
    assert result["solved"] is True
    assert result["attempts"] <= 7


def test_agent_solves_edge_low():
    agent = AutoSolverAgent(secret=1, difficulty="Hard")
    result = agent.run()
    assert result["solved"] is True


def test_agent_solves_edge_high():
    agent = AutoSolverAgent(secret=50, difficulty="Hard")
    result = agent.run()
    assert result["solved"] is True


def test_agent_fails_gracefully_with_low_max_attempts():
    # Force a failure path to prove the guardrail/logging code runs, not just the happy path.
    agent = AutoSolverAgent(secret=99, difficulty="Normal", max_attempts=1)
    result = agent.run()
    assert result["solved"] is False
    assert result["reason"] == "max_attempts_exceeded"
