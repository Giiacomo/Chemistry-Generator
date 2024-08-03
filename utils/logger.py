import logging
import colorlog

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, debug_mode=False):
        if self._initialized:
            return
        self._initialized = True
        self.debug_mode = debug_mode
        self.logger = colorlog.getLogger()
        self._configure_logger()

    def _configure_logger(self):
        # Clear existing handlers to avoid duplicate logs
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # Create a formatter that colors only the time and level name
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(message)s',
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'purple',
            }
        )

        handler = colorlog.StreamHandler()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG if self.debug_mode else logging.INFO)

    @staticmethod
    def get_logger():
        if Logger._instance is None:
            Logger()
        return Logger._instance.logger

    @staticmethod
    def set_debug_mode(debug_mode):
        if Logger._instance is None:
            Logger()
        if Logger._instance.debug_mode != debug_mode:
            Logger._instance.debug_mode = debug_mode
            Logger._instance._configure_logger()

    @staticmethod
    def debug(message):
        Logger.get_logger().debug(message)

    @staticmethod
    def info(message):
        Logger.get_logger().info(message)

    @staticmethod
    def warning(message):
        Logger.get_logger().warning(message)

    @staticmethod
    def error(message):
        Logger.get_logger().error(message)

    @staticmethod
    def critical(message):
        Logger.get_logger().critical(message)
