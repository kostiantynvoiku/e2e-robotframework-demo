from robot.api import logger
from robot.api.deco import keyword


class BColors:

    def __init__(self):
        self.header = '\033[95m'
        self.okblue = '\033[94m'
        self.okgreen = '\033[92m'
        self.warning = '\033[93m'
        self.fail = '\033[91m'
        self.endc = '\033[0m'

    @keyword
    def log_to_console_header(self, colored_message, message):
        return logger.console(f"{self.header}{colored_message}{self.endc} {message}")

    @keyword
    def log_to_console_blue(self, colored_message, message):
        return logger.console(f"{self.okblue}{colored_message}{self.endc} {message}")

    @keyword
    def log_to_console_green(self, colored_message, message):
        return logger.console(f"{self.okgreen}{colored_message}{self.endc} {message}")

    @keyword
    def log_to_console_orange(self, colored_message, message):
        return logger.console(f"{self.warning}{colored_message}{self.endc} {message}")

    @keyword
    def log_to_console_red(self, colored_message, message):
        return logger.console(f"{self.fail}{colored_message}{self.endc} {message}")
