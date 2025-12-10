import logging
import logging.config
import yaml
from pathlib import Path
import os

def setup_logging(
    default_path='logging_config.yaml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """
    Настройка логирования для FastAPI проекта с RotatingFileHandler.
    Работает на Windows и Linux, создаёт logs/ в корне проекта.
    """

    # Абсолютный путь до корня проекта
    BASE_DIR = Path(__file__).resolve().parents[3]  # project/

    # Папка для логов
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    # Абсолютный путь до YAML конфига
    config_file = BASE_DIR / "src" / "infrastructure" / "logging_config" / default_path

    if config_file.exists():
        with open(config_file, 'rt', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # Подставляем абсолютные пути к файлам логов
        config["handlers"]["file"]["filename"] = str(log_dir / "app.log")
        config["handlers"]["error_file"]["filename"] = str(log_dir / "error.log")

        # Применяем конфигурацию
        try:
            logging.config.dictConfig(config)
        except Exception as e:
            print("Ошибка конфигурации логирования:", e)
            logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)