import os
import logging
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("GITHUB_TOKEN")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG")

# loggger confiq
logging.basicConfig(level=logging.INFO, format='%(levelname)s [%(asctime)s] - %(message)s')

logger = logging.getLogger(__name__)
logger.error("App started %s", "Bulus")