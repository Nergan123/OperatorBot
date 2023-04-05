import os
import logging
from dotenv import load_dotenv

from src.operator.Operator import Operator
from src.operator.helpers.logging.Formatter import CustomFormatter


def main():
    """Launches the bot"""

    load_dotenv()
    token = os.getenv('TOKEN')
    bot = Operator(command_prefix="!")
    bot.run(token)


if __name__ == '__main__':
    if not os.path.isdir('logs'):
        os.makedirs('logs')

    fmt = '%(asctime)s [%(name)s]: %(levelname)s: %(message)s'

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter(fmt))

    file_handler = logging.FileHandler("logs/logs.log", 'a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt))

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            stdout_handler,
            file_handler
        ]
    )
    main()
