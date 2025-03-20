import os
import json
from pathlib import Path
from typing import Dict, Any
from datasets import load_dataset


def preprocess_data(dataset):
    data_dict = {}
    for question in dataset:
        data_dict[question] = dataset[question]
    return inflate_flat_data(data_dict)

# --- Inflating Function ---
def inflate_flat_data(flat_data):
    inflated = {}
    for category, examples in flat_data.items():
        cat_dict = {}
        for example in examples:
            qid = int(example.get('qid'))
            example_copy = dict(example)
            if 'qid' in example_copy:
                del example_copy['qid']

            if qid not in cat_dict:
                cat_dict[qid] = []
                
            cur_item = clean_feature(example_copy)
            cat_dict[qid].append(cur_item)
        inflated[category] = cat_dict
    return inflated

def flat_choice(QA_dict):
    options = []
    for key in QA_dict:
        curent_choice = f"{key}<-->{QA_dict[key]}"
        options.append(curent_choice)
    return '\n<--->\n'.join(options)

def clean_feature(sample):
    updated_sample = {}
    for key in sample:
        if sample[key] == 'None':
            continue
        elif key == 'choices':
            choice_dic = {}
            choices = sample[key].split('\n<--->\n')
            for option in choices:
                items = option.split('<-->')
                choice_dic[items[0]] = items[1]
            updated_sample[key] = choice_dic
        else:
            updated_sample[key] = sample[key]
    return updated_sample


def store_json(target_dict: Dict[str, Dict[Any, Any]], 
               task_type: str,
               folder_path: str) -> None:
    """
    Store question data in JSON files organized by task type and question name.
    
    Args:
        target_dict: Dictionary containing question data
        task_type: Type of task (e.g. 'Structure_Reasoning')
        folder_path: Base path to store the JSON files
    """
    root_path = Path(folder_path) / task_type
    
    for question_name, questions in target_dict.items():
        sub_folder = root_path / question_name
        sub_folder.mkdir(parents=True, exist_ok=True)
        
        for question_idx, data in questions.items():
            file_path = sub_folder / f"QA_{question_idx}.json"
            if file_path.exists():
                continue
                
            try:
                with file_path.open('w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"Error writing to {file_path}: {e}")
                raise  # Re-raise exception to handle errors properly
                
def prepare_dataset(folder_path="SV-TrustEval-C-1.1"):
    dataset = load_dataset("Jackline/SV-TrustEval-C-1.0")
    data_dict = preprocess_data(dataset)
    structure_reasoning = {}
    vulnerability_reasoning = {}
    for key in data_dict:
        if key in ['ControlFlow', 'DataFlow']:
            structure_reasoning[key] = data_dict[key]
        else:
            vulnerability_reasoning[key] = data_dict[key]
    store_json(structure_reasoning, task_type='Structure_Reasoning', folder_path=folder_path)
    store_json(vulnerability_reasoning, task_type='Semantic_Reasoning', folder_path=folder_path)

if __name__ == "__main__":
    prepare_dataset()
