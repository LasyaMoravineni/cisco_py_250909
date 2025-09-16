import logging

logging.basicConfig(
    filename="hospital_app_logs.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)
