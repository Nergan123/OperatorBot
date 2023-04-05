from src.operator.helpers.BaseClass import BaseClass
from src.operator.services.commentator.CommentatorService import CommentatorService
from src.operator.services.dice_rolls.DiceRollerService import DiceRollerService


class State(BaseClass):
    """Campaign state"""

    def __init__(self):
        super().__init__("campaign_state")
        self._dice_rolls = DiceRollerService()
        self._commentator = CommentatorService()

    def get_dice_rolls(self):
        """Returns dice roller service"""

        return self._dice_rolls

    def get_commentator(self):
        """Returns a commentator service"""

        return self._commentator
