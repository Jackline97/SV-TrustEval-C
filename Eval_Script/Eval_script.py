from tqdm import tqdm
import os
import json
import re
import argparse

def jaccard_similarity(text1, text2):
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    similarity = len(intersection) / len(union)
    return similarity

def target_option(text):
    # Regular expression to match lines with options marked by A, B, C, or D, possibly mixed with text
    pattern = r"\b(?:Option|Variant)?\s*([ABCD])\b"

    # Finding all matches using the regular expression
    matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
    # Iterating through matches to print the line number and matched option
    for match in matches:

        return match.group(1)
    
    
def load_json(file):
    with open(file, 'r') as f:
        file_dict = json.load(f)
    return file_dict

def load_file(root_folder):
    model_dic = {}
    for model in tqdm(os.listdir(root_folder)):
        model_dic[model] = {}
        model_cat = os.path.join(root_folder, model)
        for task in os.listdir(model_cat):
            model_dic[model][task] = {}
            task_cat = os.path.join(model_cat, task)
            for file in os.listdir(task_cat):
                file_id = file.split('.')[0].split('_')[-1]
                file_pth = os.path.join(task_cat, file)
                model_dic[model][task][file_id] = load_json(file_pth)
    return model_dic

def basic_performance_statistic(model_cat):
    performance_QA = {}
    falsepos_QA = {}
    amount_QA = {}
    distance_QA = {}
    for task in model_cat:
        if task == 'Base_questions':
            falsepos_QA['prediction'] = []
            falsepos_QA['answer'] = []
            pos_count = 0
            pos_acc = 0
            neg_count = 0
            neg_acc = 0
            file_performance = model_cat[task]
            for file in file_performance:
                for QA in file_performance[file]:
                    prediction = target_option(QA['prediction'])
                    answer = QA['answer'][-1]
                    falsepos_QA['answer'].append(answer.upper())
                    falsepos_QA['prediction'].append(prediction.upper())
                    if answer == 'B':
                        if prediction == answer:
                            pos_acc += 1
                        pos_count += 1
                    elif answer == 'A':
                        if prediction == answer:
                            neg_acc += 1
                        neg_count += 1

            performance_QA['Pos_'+task] = (pos_acc/pos_count)*100
            amount_QA['Pos_'+task] = (pos_acc, pos_count)
            performance_QA['Neg_'+task] = (neg_acc/neg_count)*100
            amount_QA['Neg_'+task] = (neg_acc, neg_count)
        else:
            distance_QA[task] = {}
            count = 0
            acc = 0
            file_performance = model_cat[task]
            for file in file_performance:
                for QA in file_performance[file]:
                    prediction = target_option(QA['prediction'])
                    answer = QA['answer']
                    distance = str(QA['distance'])
                    if '_' in distance and 'inner' in distance:
                        distance = '_'.join(distance.split('_')[:-1])

                    if not prediction:
                        choices = QA['choices']
                        sim_list = []
                        for key in choices:
                            sim = jaccard_similarity(choices[key], QA['prediction'])
                            sim_list.append(sim)
                        prediction = list(choices.keys())[sim_list.index(max(sim_list))]
                    else:
                        prediction = prediction.upper()
                    
                    if distance not in distance_QA[task]:
                        distance_QA[task][distance] = []
                        
                    if prediction == answer:
                        acc += 1
                        score = 1
                    elif len(answer) > 1:
                        if prediction in answer:
                            acc += 0.5
                            score = 0.5
                    else:
                        score = 0
                    count += 1                        
                    distance_QA[task][distance].append(score)
            performance_QA[task] = acc/count
            amount_QA[task] = (acc, count)
    return performance_QA, falsepos_QA, amount_QA, distance_QA

def round_func(number):
    if number < 1:
        number = number*100
    return "{:.2f}".format(round(number, 2))


# Generate difficulty scale performance
def cal_dis_acc(dis_dic):
    acc_dic = {}
    for task in dis_dic:
        acc_dic[task] = {}
        for dis in dis_dic[task]:
            acc_dic[task][dis] = dis_dic[task][dis].count(1)/len(dis_dic[task][dis])
            acc_dic[task][dis] = round_func(acc_dic[task][dis])
    return acc_dic

def distance_performance_statistic(model_cat):
    performance_QA = {}
    for task in model_cat:
        if task != 'Base_questions':
            performance_QA[task] = {}
            count = 0
            acc = 0
            file_performance = model_cat[task]
            for file in file_performance:
                for QA in file_performance[file]:
                    prediction = target_option(QA['prediction'])
                    answer = QA['answer']
                    distance = str(QA['distance'])
                    if not prediction:
                        choices = QA['choices']
                        sim_list = []
                        for key in choices:
                            sim = jaccard_similarity(choices[key], QA['prediction'])
                            sim_list.append(sim)
                        prediction = list(choices.keys())[sim_list.index(max(sim_list))]
                    else:
                        prediction = prediction.upper()


                    if '_' in distance and distance != 'outer_variant':
                        distance = distance[:-2]

                    if distance not in performance_QA[task]:
                        performance_QA[task][distance] = []

                    if prediction == answer:
                        cur_acc = 1
                    elif len(answer) > 1:
                        if prediction in answer:
                            cur_acc = 0.5
                    else:
                        cur_acc = 0
                    if cur_acc != 0:
                        performance_QA[task][distance].append(1)
                    else:
                        performance_QA[task][distance].append(0)

    acc_dic = cal_dis_acc(performance_QA)
    return acc_dic, performance_QA

def sort_dic(data):
    sorted_data = {k: data[k] for k in sorted(data, key=int)}
    return sorted_data

def base_code_performance_statistic(model_cat):
    performance_QA = {}
    for task in model_cat:
        if task == 'Base_questions':
            file_performance = model_cat[task]
            for file in file_performance:
                for QA in file_performance[file]:
                    prediction = target_option(QA['prediction'])
                    answer = QA['answer'][-1]
                    Case_ID = QA['case_id']
                    if Case_ID not in performance_QA:
                        performance_QA[Case_ID] = {}
                    if prediction == answer:
                        acc = 1
                    else:
                        acc = 0
                    if answer == 'A':
                        performance_QA[Case_ID]['val'] = acc
                    elif answer == 'B':
                        performance_QA[Case_ID]['non_val'] = acc
    return performance_QA

def cal_consistant_acc(dis_dic):
    acc_dic = {}
    for task in dis_dic:
        acc_dic[task] = dis_dic[task].count(1)/len(dis_dic[task])
        acc_dic[task] = round_func(acc_dic[task])
    return acc_dic

def consistant_performance_statistic(model_cat, base_performance_table):
    performance_QA = {}
    for task in model_cat:
        if task == 'Base_questions':
            continue

        performance_QA[task] = []
        if task == 'Counterfactual':
            counterfactual_var = {'good':[], 'bad':[]}

        file_performance = model_cat[task]
        for file in file_performance:
            for QA in file_performance[file]:
                prediction = target_option(QA['prediction'])
                answer = QA['answer']
                case_id = QA['case_id']
                if task == 'GoalDriven':
                    base_performance = base_performance_table[case_id]['non_val']
                elif task == 'Predictive':
                    base_performance = base_performance_table[case_id]['val']
                elif task == 'Counterfactual':
                    if answer == 'C':
                        base_performance = base_performance_table[case_id]['val']
                    elif answer == 'A':
                        base_performance = base_performance_table[case_id]['non_val']
                    elif answer == 'B':
                        base_performance = base_performance_table[case_id]['non_val'] and base_performance_table[case_id]['val']
                else:
                    if case_id in base_performance_table.keys():
                        base_performance = base_performance_table[case_id]['non_val'] or base_performance_table[case_id]['val']
                    else:
                        continue
                if not prediction:
                    choices = QA['choices']
                    sim_list = []
                    for key in choices:
                        sim = jaccard_similarity(choices[key], QA['prediction'])
                        sim_list.append(sim)
                    prediction = list(choices.keys())[sim_list.index(max(sim_list))]
                else:
                    prediction = prediction.upper()
                if prediction == answer:
                    acc = 1
                else:
                    acc = 0

                if acc == base_performance and acc:
                    performance_QA[task].append(1)
                    if task == 'Counterfactual' and answer == 'C':
                        counterfactual_var['bad'].append(1)
                    elif task == 'Counterfactual' and answer != 'C':
                        counterfactual_var['good'].append(1)

                else:
                    performance_QA[task].append(0)
                    if task == 'Counterfactual' and answer == 'C':
                        counterfactual_var['bad'].append(0)
                    elif task == 'Counterfactual' and answer != 'C':
                        counterfactual_var['good'].append(0)

    return cal_consistant_acc(performance_QA),cal_consistant_acc(counterfactual_var)

if __name__ == '__main__':
    # Add argument parsing
    parser = argparse.ArgumentParser(description='Evaluate LLM performance')
    parser.add_argument('--root_folder', type=str, default='results/LLM_result_zero-shot_0.0',
                      help='Root folder containing LLM results')
    parser.add_argument('--save_path', type=str, default='eval_score',
                      help='Output path for the results')
    args = parser.parse_args()

    # Load model results
    model_dic = load_file(root_folder=args.root_folder)
    
    # Initialize results dictionary
    result_dic = {
        'basic_performance': {},
        'distance_performance': {},
        'consistant_performance': {}
    }

    # Generate basic performance metrics
    for model_name in model_dic:
        # Calculate basic performance statistics
        performance_GPT, falsepos_QA, amount_QA, distance_QA = basic_performance_statistic(model_dic[model_name])
        
        # Store results for this model
        result_dic['basic_performance'][model_name] = {
            'DataFlow': round_func(performance_GPT['DataFlow']),
            'ControlFlow': round_func(performance_GPT['ControlFlow']),
            'Structure AVG': round_func((performance_GPT['ControlFlow'] + performance_GPT['DataFlow'])/2),
            'Counterfactual': round_func(performance_GPT['Counterfactual']),
            'GoalDriven': round_func(performance_GPT['GoalDriven']), 
            'Predictive': round_func(performance_GPT['Predictive']),
            'Semantic AVG': round_func((performance_GPT['Counterfactual'] + performance_GPT['GoalDriven'] + performance_GPT['Predictive'])/3),
            'Pos_Base_questions': round_func(performance_GPT['Pos_Base_questions']),
            'Neg_Base_questions': round_func(performance_GPT['Neg_Base_questions']),
            'Total_Base_questions': round_func((performance_GPT['Pos_Base_questions'] + performance_GPT['Neg_Base_questions'])/2)
        }

        # Calculate distance-based performance
        performance_distance, performance_statistic = distance_performance_statistic(model_dic[model_name])
        result_dic['distance_performance'][model_name] = {
            'ControlFlow': sort_dic(performance_distance['ControlFlow']),
            'DataFlow': sort_dic(performance_distance['DataFlow']),
            'Counterfactual': performance_distance['Counterfactual'],
            'GoalDriven': performance_distance['GoalDriven'],
            'Predictive': performance_distance['Predictive']
        }

    # Calculate consistency scores
    base_code_dic = {
        model_name: base_code_performance_statistic(model_dic[model_name])
        for model_name in model_dic
    }

    for model_name in model_dic:
        performance_GPT, _ = consistant_performance_statistic(model_dic[model_name], base_code_dic[model_name])
        result_dic['consistant_performance'][model_name] = performance_GPT


    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)
    model_name_from_path = os.path.basename(args.root_folder)
    output_path = f'{args.save_path}/result_dic_{model_name_from_path}.json'
    with open(output_path, 'w') as f:
        json.dump(result_dic, f, indent=4)
    print(f"Results saved to {output_path}")
