import logging
import sys

def setup_logger(name: str):
    """
    Налаштовує стандартний логер.
    Використовує патерн Singleton для уникнення дублювання повідомлень.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger