import os
from transformers import pipeline
from tqdm import tqdm
import json
import re
import logging
import argparse
import re
from io import StringIO
import tokenize
import random
import torch
from pathlib import Path
def remove_comments_and_docstrings(source,lang):
    if lang in ['python']:
        """
        Returns 'source' minus comments and docstrings.
        """
        io_obj = StringIO(source)
        out = ""
        prev_toktype = tokenize.INDENT
        last_lineno = -1
        last_col = 0
        for tok in tokenize.generate_tokens(io_obj.readline):
            token_type = tok[0]
            token_string = tok[1]
            start_line, start_col = tok[2]
            end_line, end_col = tok[3]
            ltext = tok[4]
            if start_line > last_lineno:
                last_col = 0
            if start_col > last_col:
                out += (" " * (start_col - last_col))
            # Remove comments:
            if token_type == tokenize.COMMENT:
                pass
            # This series of conditionals removes docstrings:
            elif token_type == tokenize.STRING:
                if prev_toktype != tokenize.INDENT:
            # This is likely a docstring; double-check we're not inside an operator:
                    if prev_toktype != tokenize.NEWLINE:
                        if start_col > 0:
                            out += token_string
            else:
                out += token_string
            prev_toktype = token_type
            last_col = end_col
            last_lineno = end_line
        temp=[]
        for x in out.split('\n'):
            if x.strip()!="":
                temp.append(x)
        return '\n'.join(temp)
    elif lang in ['ruby']:
        return source
    else:
        def replacer(match):
            s = match.group(0)
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        temp=[]
        for x in re.sub(pattern, replacer, source).split('\n'):
            if x.strip()!="":
                temp.append(x)
        return '\n'.join(temp)


def list_files_by_subfolder(directory):
    """
    Organizes files by subfolders into separate lists.

    Args:
    directory (str): The path to the directory containing subfolders.

    Returns:
    dict: A dictionary with subfolder names as keys and lists of file paths as values.
    """
    files_by_subfolder = {}
    for subdir, dirs, files in os.walk(directory):
        subfolder_name = os.path.basename(subdir)
        if subfolder_name not in files_by_subfolder and subfolder_name !='':
            files_by_subfolder[subfolder_name] = []
        
        for file in files:
            file_path = os.path.join(subdir, file)
            files_by_subfolder[subfolder_name].append(file_path)
    
    return files_by_subfolder

def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as result_file:
        question_dic = json.load(result_file)
    return question_dic

def replace_func_name(code, replace=False):
    if replace:
        code = remove_comments_and_docstrings(code, lang='C')
        func_name = code.split('\n')[0]
        LLM_version_func_name = f"{func_name.split()[0]} Sample_Func()"
        code = code.replace(func_name, LLM_version_func_name)
    return code

def flat_choice(QA_dict):
    options = []
    for key in QA_dict:
        curent_choice = f"{key}:{QA_dict[key]}"
        options.append(curent_choice)
    return '\n'.join(options)

def load_content_SR(files):
    cur_set = {}
    for key in files:
        cur_set[key] = {}
        contents = files[key]
        for idx, content in enumerate(contents):
            file_content = read_file(content)
            for QA in file_content:
                code = replace_func_name(QA['code'])
                question = QA['question']
                choices = flat_choice(QA['choices'])
                content = f"Code:{code}\n\nQuestion:{question}\n\n{choices}"
                QA['Question_final'] = content
            cur_set[key][idx]=file_content
    return cur_set

def load_content_VR(files):
    random.seed(42)
    cur_set = {}
    for key in files:
        cur_set[key] = {}
        contents = files[key]
        if key == 'Base_questions':
            for idx, content in enumerate(contents):
                file_content = read_file(content)
                for QA in file_content:
                    code = QA['code']
                    question = QA['question']
                    choices = flat_choice(QA['choices'])
                    content = f"Code:{code}\n\nQuestion:{question}\n\n{choices}"
                    QA['Question_final'] = content
                cur_set[key][idx]=file_content

        elif key == 'Counterfactual':
            for idx, content in enumerate(contents):
                file_content = read_file(content)
                for QA in file_content:
                    org_code = QA['org_code']
                    new_code = QA['new_code']
                    question = QA['question']
                    choices = flat_choice(QA['choices'])
                    content = f"{org_code}\n\n{new_code}\n\n{question}\n\n{choices}"
                    QA['Question_final'] = content
                cur_set[key][idx]=file_content

        # add shuffle here
        elif key == 'GoalDriven':
            for idx, content in enumerate(contents):
                file_content = read_file(content)
                for QA in file_content:
                    org_code = QA['org_code']
                    question = QA['question']
                    # add shuffle here
                    choices_str, answer_str = shuffle_answers_and_format(QA)
                    QA['choices'] = choices_str
                    QA['answer'] = answer_str
                    choices = flat_choice(QA['choices'])
                    content = f"{question}\n\ncode snippet:\n{org_code}\n\n{choices}"
                    QA['Question_final'] = content
                cur_set[key][idx]=file_content                
        
         
        elif key == 'Predictive':
            for idx, content in enumerate(contents):
                file_content = read_file(content)
                for QA in file_content:
                    question = QA['question']
                    # add shuffle here
                    choices_str, answer_str = shuffle_answers_and_format(QA)
                    QA['choices'] = choices_str
                    QA['answer'] = answer_str
                    choices = flat_choice(QA['choices'])
                    content = f"{question}\n\n{choices}"
                    QA['Question_final'] = content
                cur_set[key][idx]=file_content            
    return cur_set

def shuffle_answers_and_format(QA):
    choices = QA['choices']
    answer = QA['answer']
    keys = list(choices.keys())
    random.shuffle(keys)
    shuffled_choices = {new_key: choices[old_key] for new_key, old_key in zip(['A', 'B', 'C', 'D'], keys)}
    for new_key, old_key in zip(['A', 'B', 'C', 'D'], keys):
        if old_key == answer:
            new_answer = new_key
            break
    return shuffled_choices, new_answer

def target_option(text):
    # Regular expression to match lines with options marked by A, B, C, or D, possibly mixed with text
    pattern = r"\b(?:Option|Variant)?\s*([ABCD])\b"

    # Finding all matches using the regular expression
    matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
    
    # Iterating through matches to print the line number and matched option
    for match in matches:
        return match.group(1)
    
def load_fewshot_case_SR(key):
    with open(f'fewshot_examples/{key}.json', 'r') as file:
        data = json.load(file)
    final_output = ''
    for example in data:
        code_snippet = example["code"]
        final_output += f"Sample Code:\n{code_snippet}\n"
        for question in example["questions"]:
            q = question["question"]
            final_output += f"{q}\n"
            for choice, text in question["choices"].items():
                final_output += f"{choice}:{text}\n"
            a = question["answer"]
            e = question["explanation"]
            final_output += f"Answer: {a}\n"
            final_output += f"Explanation: {e}\n\n\n"
    return final_output.strip()

def load_fewshot_case_VR(key):
    with open(f'fewshot_examples/{key}.json', 'r') as file:
        data = json.load(file)
    final_output = ''
    for example in data:
        if 'code' in example:
            code = example["code"]
            code_snippet = code
            final_output += f"Sample Code:\n{code_snippet}\n"
        elif 'org_code' in example:
            org_code = example["org_code"]
            new_code = example["new_code"]
            code_snippet = f"{org_code}\n\n{new_code}"
            final_output += f"Sample Code:\n{code_snippet}\n"
        else:
            final_output += ''
        q = example["question"]
        final_output += f"{q}\n"
        for choice, text in example["choices"].items():
            final_output += f"{choice}:{text}\n\n"
        a = example["answer"]
        e = example["explain"]
        final_output += f"Answer: {a}\n"
        final_output += f"Explanation: {e}\n\n\n"
        
    return final_output.strip()

def LLM_testing(dic_target, model_name, chatbot, inference_mode, temperature, root_path="LLM_result_fewshot_updated"):
    key_list = list(dic_target.keys())
    for q_type in key_list:
        # breakpoint
        if inference_mode == 'few-shot':
            if q_type in ['Structurewise', 'Variablewise']:
                fewshot_prompt = load_fewshot_case_SR(key=q_type)
            elif q_type in ['Counterfactual', 'GoalDriven', 'Predictive']:
                fewshot_prompt = load_fewshot_case_VR(key=q_type)
            else:
                fewshot_prompt = None

        directory = f"{root_path}/{model_name}/{q_type}"
        os.makedirs(directory, exist_ok=True)
        count = 0
        acc = 0
        QA_set = dic_target[q_type]
        QA_list = list(QA_set.keys())
        pbar = tqdm(QA_list, desc=f"Initial setup on {q_type}")
        for case in pbar:
            # in case of server down
            file_path = os.path.join(directory, f"QA_{case}.json")
            if os.path.exists(file_path):
                continue
            else:
                QA = QA_set[case]
                final_res = []
                for idx, qa_info in enumerate(QA):
                    content = qa_info['Question_final']
                    if q_type == 'Base_questions':
                        final_content = content
                    else:
                        if inference_mode == 'few-shot':
                            final_content = f"Here are some examples:{fewshot_prompt}\n\nNow please answer the following question:{content}"
                        else:
                            final_content = content
                    
                    prediction = agent_answer(final_content,chatbot=chatbot, temperature=temperature)
                    qa_info['prediction'] = prediction
                    qa_info['wholecontent'] = final_content
                    final_res.append(qa_info)
                    if 'Answer' in qa_info:
                        qa_info['answer'] = qa_info['Answer']
                    if target_option(prediction) == qa_info['answer'][-1]:
                        acc += 1
                    count += 1
                    pbar.set_description(f"Running Case: {q_type}, {model_name} {idx + 1}/{len(QA)}-Prediction:{target_option(prediction)}-Answer:{qa_info['answer'][-1]}, ACC: {acc/count}")
                with open(file_path, "w", encoding='utf-8') as result_file:
                    json.dump(final_res, result_file,indent=4)

def agent_answer(content, chatbot, temperature):
    cur_len = len(chatbot.tokenizer(content)['input_ids'])
    if cur_len > 10000:
        extracted_messages = "Exceed Limit"
    else:
        Starter_Sentence = f"As a code security expert, I will present you with a selection of code snippets. Your task is to answer the accompanying multiple-choice questions, which may require either single or multiple answers. Please respond with the letter(s) of the correct answer(s) only; do not include any explanations! (example: Answer: A (single) or Answer: A, C (multiple))"
        chat = [
            {"role": "user", "content": f"{Starter_Sentence}\n\n\n{content}"}
        ]
        with torch.no_grad():
            if temperature == 0:
                do_sample = False
            else:
                do_sample = True
            response = chatbot(chat, max_new_tokens=100, pad_token_id=chatbot.tokenizer.eos_token_id, do_sample=do_sample, temperature=temperature)
        extracted_messages = response[0]['generated_text'][-1]['content']
        torch.cuda.empty_cache()
    return extracted_messages

if __name__ == '__main__':
    # Set up argument parser with clear help messages
    parser = argparse.ArgumentParser(
        description="Process input parameters for model training and testing."
    ) 
    parser.add_argument("--model_name", type=str, required=True,
                        help="Name identifier for the model.")
    parser.add_argument("--model_loc", type=str, required=True,
                        help="Path or URL to the model location.")
    parser.add_argument("--benchmark_loc", type=str, default="SV-TrustEval-C-Offical-1.0",
                        help="benchmark folder location")
    parser.add_argument("--result_loc", type=str, default="SV-TrustEval-C-Offical-1.0_results",
                        help="result folder location")        
    parser.add_argument("--temperature", type=float, default=0.0,
                        help="Temperature setting for text generation.")
    parser.add_argument("--inference_mode", type=str, choices=["zero-shot", "few-shot"], default="few-shot",
                        help="Inference mode, e.g. 'zero-shot' or 'few-shot' (ICL).")

    args = parser.parse_args()

    # Extract arguments
    model_name = args.model_name
    model_loc = args.model_loc
    temperature = args.temperature
    benchmark_loc = args.benchmark_loc
    result_loc = args.result_loc
    inference_mode = args.inference_mode
    
    # Set device and initialize the text-generation pipeline
    device = "cuda"
    chatbot = pipeline("text-generation", model=model_loc, device=device, torch_dtype='auto', trust_remote_code=True)

    # Ensure tokenizer has a pad token
    if chatbot.tokenizer.pad_token is None:
        chatbot.tokenizer.pad_token = chatbot.tokenizer.eos_token

    print(f'Launch LLM with temperature={temperature}')

    # Define directories for reasoning files
    structure_reasoning = f'{benchmark_loc}/Structure_Reasoning/'
    vulnerability_reasoning = f'{benchmark_loc}/Semantic_Reasoning/'

    # Construct the output directory path
    root_path = str(Path(result_loc) / f"LLM_result_{inference_mode}_{temperature}")

    # Get files for each reasoning category
    SR_files = list_files_by_subfolder(structure_reasoning)
    VR_files = list_files_by_subfolder(vulnerability_reasoning)

    # Load content for each category
    SR_QA = load_content_SR(SR_files)
    VR_QA = load_content_VR(VR_files)

    # Run testing for both reasoning categories
    LLM_testing(SR_QA, model_name=model_name, chatbot=chatbot,
                inference_mode=inference_mode, root_path=root_path, temperature=temperature)
    LLM_testing(VR_QA, model_name=model_name, chatbot=chatbot,
                inference_mode=inference_mode, root_path=root_path, temperature=temperature)