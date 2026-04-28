import os
import pandas as pd
from datasets import load_dataset
from src.config import config
from src.phase1_data.data_schema import RestaurantClean
from src.phase5_infra.logger import logger
import re

def clean_mojibake(text: str) -> str:
    if not isinstance(text, str):
        return text
    return re.sub(r'[^\x00-\x7F]+', '', text).strip()

def process_cost(val) -> float:
    if pd.isna(val) or val is None or val == '': return 0.0
    val_str = str(val).replace(',', '').strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def process_rating(val) -> float:
    if pd.isna(val) or val is None or val in ('NEW', '-', ''): return 0.0
    val_str = str(val).split('/')[0].strip()
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def process_votes(val) -> int:
    if pd.isna(val) or val is None or val == '': return 0
    try:
        return int(val)
    except ValueError:
        return 0

def standardize_location(loc: str) -> str:
    loc = str(loc).lower().strip()
    if loc == 'nan' or loc == '':
        return ''
    
    if loc in ['central bangalore', 'east bangalore', 'north bangalore', 'south bangalore', 'west bangalore']:
        return ''
        
    if 'koramangala' in loc:
        return 'koramangala'
        
    if 'whitefield' in loc:
        return 'whitefield'
        
    cbd_roads = [
        'brigade road', 'mg road', 'church street', 'st. marks road', 
        'residency road', 'richmond road', 'lavelle road', 'cunningham road', 
        'commercial street', 'infantry road', 'race course road', 'sankey road'
    ]
    if loc in cbd_roads:
        return 'ashok nagar'
        
    if loc.endswith(' road'):
        return loc[:-5].strip()
        
    if loc.endswith(' street'):
        return loc[:-7].strip()
        
    return loc



def load_and_clean_data():
    dataset_name = config['data']['hf_dataset']
    raw_path = config['data']['raw_path']
    processed_path = config['data']['processed_path']
    
    logger.info(f"Loading dataset {dataset_name} from Hugging Face")
    try:
        dataset = load_dataset(dataset_name, split="train")
        df = dataset.to_pandas()
        os.makedirs(os.path.dirname(raw_path), exist_ok=True)
        df.to_parquet(raw_path)
        logger.info(f"Successfully loaded and cached raw data to {raw_path}")
    except Exception as e:
        logger.error(f"Failed to load dataset from Hugging Face: {e}")
        if os.path.exists(raw_path):
            df = pd.read_parquet(raw_path)
            logger.info("Loaded raw data from fallback local parquet file.")
        else:
            raise e
            
    cleaned_rows = []
    dropped_count = 0
    for _, row in df.iterrows():
        try:
            name = clean_mojibake(row.get('name', 'Unknown'))
            location = standardize_location(row.get('location', ''))
            if not location:
                continue
                
            cuisines_raw = str(row.get('cuisines', ''))
            cost_raw = row.get('approx_cost(for two people)', row.get('cost', '0'))
            rating_raw = row.get('rate', row.get('rating', '0/5'))
            votes_raw = row.get('votes', '0')
            
            cuisines_list = [clean_mojibake(c.strip().lower()) for c in cuisines_raw.split(',') if c.strip()]
            
            # Explicit missing value handling - defaulting to 0.0
            clean_record = RestaurantClean(
                name=name,
                location=location,
                cuisines=cuisines_list,
                cost_for_two=process_cost(cost_raw),
                rating=process_rating(rating_raw),
                votes=process_votes(votes_raw)
            )
            cleaned_rows.append(clean_record.model_dump())
        except Exception as e:
            dropped_count += 1
            
    logger.info(f"Cleaned {len(cleaned_rows)} records, dropped {dropped_count} records")
    clean_df = pd.DataFrame(cleaned_rows).drop_duplicates(subset=['name', 'location'])
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    clean_df.to_parquet(processed_path)
    logger.info(f"Saved processed data to {processed_path}")

if __name__ == '__main__':
    load_and_clean_data()
