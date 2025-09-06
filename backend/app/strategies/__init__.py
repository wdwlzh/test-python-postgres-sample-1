from ..models import Price
from typing import List

class Strategy:
    def should_buy(self, prices: List[Price], current_position: int, current_cash: float) -> bool:
        """Decide whether to buy based on current data and state."""
        return False

    def should_sell(self, prices: List[Price], current_position: int, current_cash: float) -> bool:
        """Decide whether to sell based on current data and state."""
        return False

from .buy_and_hold import BuyAndHoldStrategy
from .ema_crossover import EMACrossoverStrategy

# Strategy registry
STRATEGIES = {
    "buy_and_hold": BuyAndHoldStrategy,
    "ema_crossover": EMACrossoverStrategy
}
