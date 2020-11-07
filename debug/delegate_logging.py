class DelegateLogging:
    def __init__(self, main_logging):
        self.main_logging = main_logging
        self.log_header = self.__class__.__name__
        self.log_enable = True

    def log(self, text):
        if self.log_enable:
            self.main_logging.delegate_log(self.log_header, text)
