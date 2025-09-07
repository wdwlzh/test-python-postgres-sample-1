from ..models import AdjustedPrice
from typing import List

class Strategy:
    def should_buy(self, prices: List[AdjustedPrice], current_position: int, current_cash: float) -> bool:
        """Decide whether to buy based on current data and state."""
        return False

    def should_sell(self, prices: List[AdjustedPrice], current_position: int, current_cash: float) -> bool:
        """Decide whether to sell based on current data and state."""
        return False

from .buy_and_hold import BuyAndHoldStrategy
from .ema_crossover import EMACrossoverStrategy

# Strategy registry
STRATEGIES = {
    "buy_and_hold": BuyAndHoldStrategy,
    "ema_crossover": EMACrossoverStrategy
}
