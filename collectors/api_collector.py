import requests
import json
import os
import time
from tqdm import tqdm

RAW_DATA_DIR = "data/raw"
BASE_URL = "https://pokeapi.co/api/v2"

def ensure_dir():
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR)

def save_json(data, filename):
    filepath = os.path.join(RAW_DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint}: {e}")
        return None

def collect_pokemon(start_id, end_id):
    print("Collecting Pokemon and Species data...")
    for i in tqdm(range(start_id, end_id + 1)):
        # Fetch Pokemon data
        poke_data = fetch_data(f"pokemon/{i}")
        if poke_data:
            save_json(poke_data, f"pokemon_{i}.json")
        
        # Fetch Species data (contains Korean name and flavor text)
        species_data = fetch_data(f"pokemon-species/{i}")
        if species_data:
            save_json(species_data, f"species_{i}.json")
            
        time.sleep(0.1) # Be polite to API

def collect_types(start_id, end_id):
    print("Collecting Types data...")
    for i in tqdm(range(start_id, end_id + 1)):
        type_data = fetch_data(f"type/{i}")
        if type_data:
            save_json(type_data, f"type_{i}.json")
        time.sleep(0.1)

def collect_moves(start_id, end_id):
    print("Collecting Moves data...")
    for i in tqdm(range(start_id, end_id + 1)):
        move_data = fetch_data(f"move/{i}")
        if move_data:
            save_json(move_data, f"move_{i}.json")
        time.sleep(0.1)

def collect_items(start_id, end_id):
    print("Collecting Items data...")
    for i in tqdm(range(start_id, end_id + 1)):
        item_data = fetch_data(f"item/{i}")
        if item_data:
            save_json(item_data, f"item_{i}.json")
        time.sleep(0.1)

def collect_evolutions(start_id, end_id):
    print("Collecting Evolution Chains...")
    for i in tqdm(range(start_id, end_id + 1)):
        evo_data = fetch_data(f"evolution-chain/{i}")
        if evo_data:
            save_json(evo_data, f"evolution_{i}.json")
        time.sleep(0.1)

if __name__ == "__main__":
    ensure_dir()
    # 1세대 151마리 수집 (완료됨)
    # collect_pokemon(1, 151)
    # 18개 기본 속성 수집 (완료됨)
    # collect_types(1, 18)
    # 1세대 기술 165개 수집
    collect_moves(1, 165)
    # 주요 도구 수집 (진화의 돌 등 포함 대략 1~100)
    collect_items(1, 100)
    # 1세대 진화 트리 (약 78개)
    collect_evolutions(1, 78)
    print("Collection Phase 1.5 Complete.")
