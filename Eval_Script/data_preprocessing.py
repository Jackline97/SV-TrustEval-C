import os
import json
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from datasets import load_dataset
import logging
from dataclasses import dataclass
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class QuestionData:
    """Data structure for a single question."""
    qid: int
    choices: Dict[str, str]
    code: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    explanation: Optional[str] = None

class DataPreprocessor:
    """Handles preprocessing of the SV-TrustEval-C dataset."""
    
    def __init__(self, dataset_name: str = "Jackline/SV-TrustEval-C-1.0"):
        """
        Initialize the data preprocessor.
        
        Args:
            dataset_name: Name of the dataset to load from Hugging Face
        """
        self.dataset_name = dataset_name
        self.dataset = None
        
    def load_dataset(self) -> None:
        """Load the dataset from Hugging Face."""
        try:
            logger.info(f"Loading dataset from {self.dataset_name}")
            self.dataset = load_dataset(self.dataset_name)
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            raise

    def preprocess_data(self) -> Dict[str, Dict[int, List[Dict[str, Any]]]]:
        """
        Preprocess the raw dataset into a structured format.
        
        Returns:
            Dictionary containing preprocessed data organized by category and question ID
        """
        if self.dataset is None:
            self.load_dataset()
            
        data_dict = {}
        for question in self.dataset:
            data_dict[question] = self.dataset[question]
        return self._inflate_flat_data(data_dict)

    def _inflate_flat_data(self, flat_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Dict[int, List[Dict[str, Any]]]]:
        """
        Transform flat data structure into a hierarchical one.
        
        Args:
            flat_data: Dictionary containing flat data structure
            
        Returns:
            Dictionary with hierarchical structure organized by category and question ID
        """
        inflated = {}
        for category, examples in tqdm(flat_data.items(), desc="Processing categories"):
            cat_dict = {}
            for example in examples:
                try:
                    qid = int(example.get('qid'))
                    example_copy = dict(example)
                    example_copy.pop('qid', None)  # Safely remove qid if present
                    
                    if qid not in cat_dict:
                        cat_dict[qid] = []
                    
                    cur_item = self._clean_feature(example_copy)
                    cat_dict[qid].append(cur_item)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Error processing example in category {category}: {e}")
                    continue
                    
            inflated[category] = cat_dict
        return inflated

    @staticmethod
    def _flat_choice(qa_dict: Dict[str, str]) -> str:
        """
        Convert choices dictionary to formatted string.
        
        Args:
            qa_dict: Dictionary containing choices
            
        Returns:
            Formatted string of choices
        """
        options = [f"{key}<-->{value}" for key, value in qa_dict.items()]
        return '\n<--->\n'.join(options)

    @staticmethod
    def _clean_feature(sample: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and format sample features.
        
        Args:
            sample: Dictionary containing sample features
            
        Returns:
            Cleaned and formatted sample dictionary
        """
        updated_sample = {}
        for key, value in sample.items():
            if value == 'None':
                continue
            elif key == 'choices':
                try:
                    choice_dic = {}
                    choices = value.split('\n<--->\n')
                    for option in choices:
                        items = option.split('<-->')
                        if len(items) == 2:
                            choice_dic[items[0]] = items[1]
                    updated_sample[key] = choice_dic
                except Exception as e:
                    logger.warning(f"Error processing choices: {e}")
                    continue
            else:
                updated_sample[key] = value
        return updated_sample

    def store_json(self, target_dict: Dict[str, Dict[int, List[Dict[str, Any]]]], 
                  task_type: str,
                  folder_path: Union[str, Path]) -> None:
        """
        Store preprocessed data in JSON files.
        
        Args:
            target_dict: Dictionary containing preprocessed data
            task_type: Type of task (e.g., 'Structure_Reasoning')
            folder_path: Base path to store the JSON files
        """
        root_path = Path(folder_path) / task_type
        root_path.mkdir(parents=True, exist_ok=True)
        
        for question_name, questions in tqdm(target_dict.items(), desc=f"Storing {task_type}"):
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
                    logger.error(f"Error writing to {file_path}: {e}")
                    raise

    def prepare_dataset(self, folder_path: Union[str, Path] = "SV-TrustEval-C-Offical-1.0") -> None:
        """
        Prepare and store the complete dataset.
        
        Args:
            folder_path: Path to store the processed dataset
        """
        try:
            data_dict = self.preprocess_data()
            
            # Separate structure and vulnerability reasoning
            structure_reasoning = {
                k: v for k, v in data_dict.items() 
                if k in ['ControlFlow', 'DataFlow']
            }
            vulnerability_reasoning = {
                k: v for k, v in data_dict.items() 
                if k not in ['ControlFlow', 'DataFlow']
            }
            
            # Store processed data
            self.store_json(structure_reasoning, 'Structure_Reasoning', folder_path)
            self.store_json(vulnerability_reasoning, 'Semantic_Reasoning', folder_path)
            
            logger.info(f"Dataset successfully prepared and stored in {folder_path}")
            
        except Exception as e:
            logger.error(f"Failed to prepare dataset: {e}")
            raise

def main():
    """Main function to run the data preprocessing pipeline."""
    try:
        preprocessor = DataPreprocessor()
        preprocessor.prepare_dataset()
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
