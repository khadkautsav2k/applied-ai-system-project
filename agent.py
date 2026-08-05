import logging
from logic_utils import check_guess, get_range_for_difficulty

logging.basicConfig(
    filename="agent_log.txt",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


class AutoSolverAgent:
    """
    Agentic loop that plays the number-guessing game on its own:
      PLAN  -> pick next guess (binary search midpoint)
      ACT   -> submit the guess via check_guess()
      CHECK -> verify the outcome is consistent with prior guesses (guardrail)
      LOOP  -> repeat until it wins or a guardrail trips
    """

    def __init__(self, secret: int, difficulty: str = "Normal", max_attempts: int = 20):
        self.secret = secret
        self.low, self.high = get_range_for_difficulty(difficulty)
        self.max_attempts = max_attempts
        self.history = []  # list of (guess, outcome)

    def plan_next_guess(self):
        return (self.low + self.high) // 2

    def check_consistency(self, guess, outcome):
        """Guardrail: outcome must match what we'd expect given prior bounds."""
        if outcome == "Too High" and guess <= self.low:
            return False
        if outcome == "Too Low" and guess >= self.high:
            return False
        return True

    def apply_outcome(self, guess, outcome):
        if outcome == "Too High":
            self.high = guess - 1
        elif outcome == "Too Low":
            self.low = guess + 1

    def run(self):
        for attempt in range(1, self.max_attempts + 1):
            guess = self.plan_next_guess()
            outcome = check_guess(guess, self.secret)

            if not self.check_consistency(guess, outcome):
                logging.error(
                    f"GUARDRAIL TRIPPED: guess={guess} outcome={outcome} "
                    f"range=({self.low},{self.high}) — inconsistent hint detected."
                )
                return {
                    "solved": False,
                    "reason": "guardrail_tripped",
                    "attempts": attempt,
                    "history": self.history,
                }

            self.history.append((guess, outcome))
            logging.info(f"Attempt {attempt}: guess={guess} outcome={outcome} range=({self.low},{self.high})")

            if outcome == "Win":
                logging.info(f"SOLVED in {attempt} attempts. Secret was {self.secret}.")
                return {
                    "solved": True,
                    "attempts": attempt,
                    "history": self.history,
                }

            self.apply_outcome(guess, outcome)

        logging.error(f"FAILED to solve within {self.max_attempts} attempts. History: {self.history}")
        return {
            "solved": False,
            "reason": "max_attempts_exceeded",
            "attempts": self.max_attempts,
            "history": self.history,
        }


if __name__ == "__main__":
    import random
    secret = random.randint(1, 100)
    agent = AutoSolverAgent(secret=secret, difficulty="Normal")
    result = agent.run()
    print(result)
