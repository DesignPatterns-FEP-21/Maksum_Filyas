# smart_day_planner/app/core/logger.py
#
import logging
import sys

# Визначаємо ім'я файлу логів.
# У Docker-контейнері цей файл буде створено в директорії /app
LOG_FILE = "smart_planner.log" 

# Налаштовуємо глобальний логер
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(message)s",
    # force=True дозволяє 'basicConfig' перевизначити 
    # будь-які попередні налаштування (корисно при перезапусках)
    force=True, 
    handlers=[
        # --- Обробник 1: Запис у файл ---
        # 'mode="a"' означає 'append' - дозапис у кінець файлу
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
        
        # --- Обробник 2: Вивід у консоль (stdout) ---
        # Це важливо, щоб бачити логи в 'docker logs'
        logging.StreamHandler(sys.stdout) 
    ]
)

logger = logging.getLogger("smart_day_planner")

# Це повідомлення тепер потрапить і в консоль, і в smart_planner.log
logger.info("Logger configured. Outputting to console and file.")