import re
import random
from src.operator.helpers.BaseClass import BaseClass


class DiceRollerService(BaseClass):
    """Roller service"""

    def __init__(self):
        super().__init__("dice_service")
        self.log.info("Loaded")

    def roll(self, message: str) -> (list, int):
        """Creates a roll message"""

        dice_num, side_num = self._process_message(message)
        rolls = self._generate_rolls(dice_num, side_num)
        percent = self._calculate_percent(dice_num, side_num, rolls)

        return rolls, percent

    def _process_message(self, message: str) -> (int, int):
        """Processes message"""

        matches = re.match(r"(?P<multiplier>\d+)d(?P<range>\d+)", message)
        if matches is None:
            raise ValueError(
                "Invalid dice specification. "
                "Valid specification looks like: <multiplier>d<range>, e.g. 3d6"
            )

        dice_num = int(matches["multiplier"])
        dice_sides = int(matches["range"])
        self.log.info(f"Received: {message}.\n"
                      f"Processed into:\n"
                      f"\tDice num: {dice_num},\n"
                      f"\tDice sides: {dice_sides}")

        return dice_num, dice_sides

    def _generate_rolls(self, dice_num: int, side_num: int) -> list:
        """Generates list of rolls"""

        output = []
        for _ in range(dice_num):
            output.append(random.randint(1, side_num))

        self.log.info(f"Generated: {output}")

        return output

    def _calculate_percent(self, dice_num: int, side_num: int, rolls: list) -> int:
        """calculates success rate"""

        total = side_num * dice_num
        sum_of_rolls = sum(rolls)
        percent = int((100 * sum_of_rolls) / total)
        self.log.info(f"Success rate: {percent}")

        return percent
