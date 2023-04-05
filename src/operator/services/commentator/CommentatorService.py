import json
import random
from src.operator.helpers.BaseClass import BaseClass


class CommentatorService(BaseClass):
    """Class for generating comments"""

    def __init__(self):
        super().__init__("commentator")
        self._dice_comments = None
        self._comment_type = {
            "dice_roll": self.comment_on_dice
        }
        self._load_comments()
        self.log.info("Loaded")

    def _load_comments(self) -> None:
        """Loads comment data"""

        with open("src/operator/data/dice_comments.json", "r") as data:
            self._dice_comments = json.load(data)
        self.log.info("Comments loaded")

    def get_comment(self, request_type: str, **kwargs) -> str:
        """Returns a comment"""

        self.log.debug(f"Received:\n"
                       f"\tType: {request_type}\n"
                       f"\tkwargs: {kwargs}")
        output = self._comment_type[request_type](**kwargs)
        self.log.info(f"Final message: {output}")
        return output

    def comment_on_dice(self, name: str, percent: int, rolls: list) -> str:
        """Returns a dice roll comment according to success rate"""

        res = 100
        for key in self._dice_comments["comments"]:
            if percent <= int(key):
                res = key
                break

        if 1 < len(rolls) <= 5:
            output = self._dice_comments["comments"][res]
            output = random.choice(output) + "\n\n"
            output += f"**{name}** rolls: {rolls[0]}"
            for roll in rolls[1::]:
                output += f" + {roll}"
            output += f" = **{sum(rolls)}**"

            return output

        output = self._dice_comments["comments"][res]
        output = random.choice(output) + "\n\n"
        output += f"**{name}** rolls: **{sum(rolls)}**"

        return output
