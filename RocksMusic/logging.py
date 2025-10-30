import logging
from logging import Logger as _Logger

logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    level=logging.INFO
)
LOGGER = logging.getLogger("RocksMusic")
# Provide convenience callables for compatibility with previous code
def get_logger(name: str = "RocksMusic") -> _Logger:
    return logging.getLogger(name)
