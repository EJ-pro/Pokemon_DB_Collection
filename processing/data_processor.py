import os
import json

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"

def ensure_dir():
    if not os.path.exists(PROCESSED_DATA_DIR):
        os.makedirs(PROCESSED_DATA_DIR)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_json(data, filename):
    filepath = os.path.join(PROCESSED_DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_korean_name(names_list, default_name):
    for n in names_list:
        if n['language']['name'] == 'ko':
            return n['name']
    return default_name

def get_korean_flavor_texts(flavor_text_entries):
    texts = []
    seen = set() # To avoid exact duplicates if any
    for f in flavor_text_entries:
        if f['language']['name'] == 'ko':
            cleaned_text = f['flavor_text'].replace('\n', ' ').replace('\f', ' ').replace('\r', '')
            key = f"{f['version']['name']}:{cleaned_text}"
            if key not in seen:
                seen.add(key)
                texts.append({
                    'version_name': f['version']['name'],
                    'content': cleaned_text
                })
    return texts

def process_types():
    types_data = []
    type_efficacy = []
    
    # 1 to 18 covers normal to fairy
    for i in range(1, 19):
        t_data = load_json(os.path.join(RAW_DATA_DIR, f"type_{i}.json"))
        if not t_data: continue
        
        type_id = t_data['id']
        name_ko = get_korean_name(t_data.get('names', []), t_data['name'])
        types_data.append({'id': type_id, 'name': name_ko})
        
        # Damage relations
        relations = t_data['damage_relations']
        
        def add_efficacy(target_list, factor):
            for t in target_list:
                # API returns URL, extract ID: https://pokeapi.co/api/v2/type/12/
                target_id = int(t['url'].split('/')[-2])
                if target_id <= 18: # Limit to base 18 types
                    type_efficacy.append({
                        'damage_type_id': type_id,
                        'target_type_id': target_id,
                        'damage_factor': factor
                    })
        
        add_efficacy(relations['double_damage_to'], 2.0)
        add_efficacy(relations['half_damage_to'], 0.5)
        add_efficacy(relations['no_damage_to'], 0.0)
        # Normal damage (1.0) is implicit, but could be computed if needed.
        # DB typically expects all relations or we default to 1.0 in queries.
    
    save_json(types_data, "types.json")
    save_json(type_efficacy, "type_efficacy.json")

def process_pokemon():
    pokemon_list = []
    stats_list = []
    pokemon_types_list = []
    species_list = []
    flavor_texts_list = []
    
    for i in range(1, 1026):
        p_data = load_json(os.path.join(RAW_DATA_DIR, f"pokemon_{i}.json"))
        s_data = load_json(os.path.join(RAW_DATA_DIR, f"species_{i}.json"))
        
        if not p_data or not s_data: continue
        
        # Korean name extraction
        name_ko = get_korean_name(s_data.get('names', []), p_data['name'])
        
        # 1. Pokemon
        pokemon_list.append({
            'id': p_data['id'],
            'name': name_ko,
            'height': p_data['height'],
            'weight': p_data['weight'],
            'base_exp': p_data['base_experience']
        })
        
        # 2. Pokemon Stats
        stats = {s['stat']['name']: s['base_stat'] for s in p_data['stats']}
        stats_list.append({
            'pokemon_id': p_data['id'],
            'hp': stats.get('hp', 0),
            'attack': stats.get('attack', 0),
            'defense': stats.get('defense', 0),
            'sp_attack': stats.get('special-attack', 0),
            'sp_defense': stats.get('special-defense', 0),
            'speed': stats.get('speed', 0)
        })
        
        # 3. Pokemon Types
        for t in p_data['types']:
            type_id = int(t['type']['url'].split('/')[-2])
            pokemon_types_list.append({
                'pokemon_id': p_data['id'],
                'type_id': type_id,
                'slot': t['slot']
            })
            
        # 4. Species
        # Generation: https://pokeapi.co/api/v2/generation/1/
        gen_id = int(s_data['generation']['url'].split('/')[-2])
        species_id = s_data['id']
        species_list.append({
            'id': species_id,
            'pokemon_id': p_data['id'],
            'generation': gen_id,
            'capture_rate': s_data['capture_rate']
        })
        
        # 5. Flavor Texts
        ko_flavors = get_korean_flavor_texts(s_data.get('flavor_text_entries', []))
        for f in ko_flavors:
            flavor_texts_list.append({
                'species_id': species_id,
                'version_name': f['version_name'],
                'content': f['content']
            })

    save_json(pokemon_list, "pokemon.json")
    save_json(stats_list, "pokemon_stats.json")
    save_json(pokemon_types_list, "pokemon_types.json")
    save_json(species_list, "species.json")
    save_json(flavor_texts_list, "flavor_text.json")

def process_moves():
    moves_list = []
    for i in range(1, 951):
        m_data = load_json(os.path.join(RAW_DATA_DIR, f"move_{i}.json"))
        if not m_data: continue
        name_ko = get_korean_name(m_data.get('names', []), m_data['name'])
        
        flavor_text = None
        for f in m_data.get('flavor_text_entries', []):
            if f['language']['name'] == 'ko':
                flavor_text = f['flavor_text'].replace('\n', ' ').replace('\f', ' ').replace('\r', '')
                break
        
        type_id = int(m_data['type']['url'].split('/')[-2]) if m_data.get('type') else None
        
        moves_list.append({
            'id': m_data['id'],
            'name': name_ko,
            'type_id': type_id,
            'power': m_data.get('power'),
            'accuracy': m_data.get('accuracy'),
            'effect_text': flavor_text
        })
    save_json(moves_list, "moves.json")

def process_items():
    items_list = []
    for i in range(1, 2251):
        i_data = load_json(os.path.join(RAW_DATA_DIR, f"item_{i}.json"))
        if not i_data: continue
        name_ko = get_korean_name(i_data.get('names', []), i_data['name'])
        
        flavor_text = None
        for f in i_data.get('flavor_text_entries', []):
            if f['language']['name'] == 'ko':
                flavor_text = f['text'].replace('\n', ' ').replace('\f', ' ').replace('\r', '')
                break
        
        category = i_data['category']['name'] if i_data.get('category') else None
        
        items_list.append({
            'id': i_data['id'],
            'name': name_ko,
            'category': category,
            'effect_text': flavor_text
        })
    save_json(items_list, "items.json")

def process_evolutions():
    evolutions_list = []
    for i in range(1, 551):
        e_data = load_json(os.path.join(RAW_DATA_DIR, f"evolution_{i}.json"))
        if not e_data: continue
        
        chain = e_data.get('chain')
        if not chain: continue
        
        queue = [chain]
        while queue:
            current = queue.pop(0)
            from_species_id = int(current['species']['url'].split('/')[-2])
            
            for evolution_to in current.get('evolves_to', []):
                to_species_id = int(evolution_to['species']['url'].split('/')[-2])
                
                details = evolution_to.get('evolution_details', [{}])
                detail = details[0] if details else {}
                min_level = detail.get('min_level')
                
                trigger_item_id = None
                if detail.get('item'):
                    trigger_item_id = int(detail['item']['url'].split('/')[-2])
                
                evolutions_list.append({
                    'from_species_id': from_species_id,
                    'to_species_id': to_species_id,
                    'min_level': min_level,
                    'trigger_item_id': trigger_item_id
                })
                
                queue.append(evolution_to)
                
    save_json(evolutions_list, "evolutions.json")

if __name__ == "__main__":
    ensure_dir()
    print("Processing Types...")
    process_types()
    print("Processing Pokemon...")
    process_pokemon()
    print("Processing Moves...")
    process_moves()
    print("Processing Items...")
    process_items()
    print("Processing Evolutions...")
    process_evolutions()
    print("Processing Complete.")

