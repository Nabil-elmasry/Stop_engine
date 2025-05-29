# modules/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

# إنشاء مجلد log/ إذا لم يكن موجودًا
os.makedirs("log", exist_ok=True)

# إعداد مسار ملف اللوج
LOG_FILE = "log/app_log.txt"

# إنشاء معالج تدوير الملفات
log_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding='utf-8'
)
log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_format)

# تهيئة اللوجر العام للمشروع
logger = logging.getLogger("StopEngineLogger")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.propagate = False

# ✅ استخدام جاهز: import logger ثم logger.logger.info(...)
