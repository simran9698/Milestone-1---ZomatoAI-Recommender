import sys
import os

# Add src to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.phase1_data.dataset_loader import load_and_clean_data
from src.phase5_infra.logger import logger

def main():
    logger.info("Starting Restaurant Recommender Pipeline")
    try:
        logger.info("Running Phase 1: Data Processing...")
        load_and_clean_data()
        logger.info("Pipeline completed successfully.")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
