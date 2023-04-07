import os
import json
from src.operator.helpers.logging.LoggerBase import LoggingHandler


class BaseClass(LoggingHandler):
    """Base class to save, log, load states"""

    SERIALIZABLE_FIELDS = []

    def __init__(self, name):
        super().__init__()
        self.log.info(f"Base Class for {name} activated")
        self.json_name = name
        self.state_bucket = "nergan-bot"
        if not os.path.isdir("operator_data"):
            os.mkdir("operator_data")

    def save_state(self) -> None:
        """Saves the current state to .json object"""

        self.log.info(
            f"{self.json_name} saving state to 'operator_data/{self.json_name}_data.json'"
        )

        state = {}
        for property_name in self.SERIALIZABLE_FIELDS:
            state[property_name] = self.__getattribute__(property_name)

        with open(f"operator_data/{self.json_name}_data.json", "w") as file:
            json.dump(state, file)

    def load_state(self) -> None:
        """Loads the current state from .json object"""

        self.log.info(
            f"{self.json_name} loading state from '{self.json_name}_data.json'"
        )

        try:
            with open(f"operator_data/{self.json_name}_data.json", "r") as file:
                state = json.load(file)

            for property_name in self.SERIALIZABLE_FIELDS:
                self.__setattr__(property_name, state[property_name])
                self.log.info(
                    f"{self.json_name} loaded {property_name} from "
                    f"'operator_data/{self.json_name}_data.json'"
                )

        except FileNotFoundError as error:
            self.log.error(f"Can't Load operator/{self.json_name}: {error}")
            self.log.info(
                f"Solving {error}. Attempting to "
                f"save state to 'operator_data/{self.json_name}_data.json'"
            )
            self.save_state()

        except KeyError as error:
            self.log.error(
                f"File corrupted. error: {error}. 'operator_data/{self.json_name}_data.json'"
            )
            self.log.info("Attempting to solve")
            self.save_state()
