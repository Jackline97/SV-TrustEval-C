# SV‑TrustEval‑C 🚨🔒

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![IEEE S&P 2025](https://img.shields.io/badge/Publication-S%26P2025-blueviolet)](https://ieeexplore.ieee.org/document/) [![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org) [![Dataset](https://img.shields.io/badge/Dataset-v1.0-blue)](https://anonymous.4open.science/r/TrustEval-1D7B)

<img src="Figures/main_intro.png" alt="SV-TrustEval-C Overview"/>

## 🔍 Overview
SV‑TrustEval‑C is the first reasoning‑based benchmark designed to rigorously evaluate Large Language Models (LLMs) on both **structure** (control/data flow) and **semantic** reasoning for vulnerability analysis in C source code. Unlike existing benchmarks that focus on pattern recognition, SV‑TrustEval‑C measures logical consistency, adaptability to code transformations, and real‑world security reasoning across six core tasks.

Our benchmark reveals that current LLMs predominantly rely on superficial pattern matching, exposing critical gaps in their ability to understand complex code relationships and ensure trustworthy vulnerability analysis.



## ⭐ Key Features
- 🎯 **Dual Reasoning Dimensions:** Structure (ControlFlow/DataFlow) & Semantic (Counterfactual/Goal‑Driven/Predictive)
- 📊 **Comprehensive Metrics:** Accuracy, Conceptual Distance Sensitivity, Reasoning Consistency
- 🔄 **Plug‑and‑Play Framework:** Seamless integration with Hugging Face models
- 🌐 **Open Dataset & Scripts:** Fully reproducible; Reliable label accuracy



## ⚙️ Installation
```bash
git clone https://github.com/Jackline97/SV-TrustEval-C.git
cd SV-TrustEval-C
pip install -r requirements.txt
```



## 🚀 Quick Start

**Before you begin, ensure you have downloaded and preprocessed the dataset from Hugging Face by running:**

```bash
python Eval_Script/data_preprocessing.py
```
This step prepares the necessary data for evaluation.

### Single-Model Evaluation
```bash
python Eval_Script/Test_Script_HF.py \
  --model_name "llama-3.1-8b-instruct" \
  --benchmark_loc "./SV-TrustEval-C-Official-1.0" \
  --result_loc "./results" \
  --temperature 0.0 \
  --inference_mode "zero-shot"
```

### Batch Evaluation
```bash
python Eval_Script/Run_Test_script_HF.py
```

### Performance Analysis
```bash
python Eval_Script/Run_Eval_script.py \
  --root_folder "./results/LLM_result_zero-shot_0.0" \
  --save_path "./results/eval_score.json"
```



## 📋 Benchmark Tasks

| **Dimension**        | **Task**             | **Description**                                                                              | **Statistics**           |
|-------------------------|----------------------|-------------------------------------------------|--------------------------|
| :gear: **Structure** | **Control Flow**     | Analyze program control-flow impacts.                          | *1,345 questions*        |
| :gear: **Structure** | **Data Flow**        | Trace data dependencies and influence.                         | *2,430 questions*        |
| :brain: **Semantic** | **Counterfactual**   | Predict vulnerability under code perturbations.                        | *3,748 questions*        |
| :brain: **Semantic** | **Goal-driven**      | Safely modify code to meet functional goals.                              | *1,159 questions*        |
| :brain: **Semantic** | **Predictive**       | Classify variants by vulnerability impact.                   | *719 questions*          |
| :shield: **Safety**  | **Base Code Files**  | Compare safe vs. unsafe versions of code samples.                                            | *377 Safe, 377 Unsafe*   |
| :warning: **CWEs**   | **Unique CWEs**      | Categorize vulnerabilities according to distinct Common Weakness Enumerations (CWEs).          | *82 unique CWEs*         |



## 📈 Evaluation Metrics
- **Accuracy**: Task-level correctness
- **Conceptual Distance Sensitivity**: Ability to handle increasing structural complexity
- **Reasoning Consistency**: Logical coherence across related queries



## 💾 Dataset

### Official Dataset (v1.0)

Download the official benchmark directly from [Hugging Face](https://huggingface.co/datasets/Jackline/SV-TrustEval-C-1.0):

- **SV-TrustEval-C Official Dataset**  
  👉 [Download Here](https://huggingface.co/datasets/Jackline/SV-TrustEval-C-1.0)

Alternatively, use the following command to automatically download and preprocess the dataset:

```bash
python Eval_Script/data_preprocessing.py
```

### PrimeVul Benchmark

For the PrimeVul version, please download the file:

- **SV-TrustEval_primevul.zip**

**Note:**  
- No preprocessing is required for the PrimeVul benchmark.  
- The PrimeVul code snippet is not validated through a compilable check due to the absence of a dedicated environment.



## 📊 Results Structure
```bash
results/
└── LLM_result_[mode]_[temp]/
    └── [model_name]/
        ├── ControlFlow/
        ├── DataFlow/
        ├── Counterfactual/
        ├── GoalDriven/
        └── Predictive/
```

<img src="Figures/results.png" alt="Evaluation Results"/>



## 🤖 Supported Models
- Meta Llama-3.1-8B-Instruct
- Gemma-7B-IT
- Mistral-7B-Instruct
- CodeQwen1.5-7B
- CodeGemma-7B
- CodeLlama-13B/7B-Instruct
- And more via Hugging Face


## 📚 Citation
```bibtex
@INPROCEEDINGS {,
author = { Li, Yansong and Branco, Paula and Hoole, Alexander M. and Marwah, Manish and Koduvely, Hari Manassery and Jourdan, Guy-Vincent and Jou, Stephan },
booktitle = { 2025 IEEE Symposium on Security and Privacy (SP) },
title = {{ SV-TrustEval-C: Evaluating Structure and Semantic Reasoning in Large Language Models for Source Code Vulnerability Analysis }},
year = {2025},
volume = {},
ISSN = {2375-1207},
pages = {3014-3032},
abstract = { As Large Language Models (LLMs) evolve in understanding and generating code, accurately evaluating their reliability in analyzing source code vulnerabilities becomes increasingly vital. While studies have examined LLM capabilities in tasks like vulnerability detection and repair, they often overlook the importance of both structure and semantic reasoning crucial for trustworthy vulnerability analysis. To address this gap, we introduce \textsc{SV-TrustEval-C}, a benchmark designed to evaluate LLMs' abilities for vulnerability analysis of code written in the C programming language through two key dimensions: structure reasoning—assessing how models identify relationships between code elements under varying data and control flow complexities; and semantic reasoning—examining their logical consistency in scenarios where code is structurally and semantically perturbed. Our results show that current LLMs are far from satisfactory in understanding complex code relationships and that their vulnerability analyses rely more on pattern matching than on robust logical reasoning. These findings underscore the effectiveness of the \textsc{SV-TrustEval-C} benchmark and highlight critical areas for enhancing the reasoning capabilities and trustworthiness of LLMs in real-world vulnerability analysis tasks. Our initial benchmark dataset is available at \textcolor{blue}{\url{https://huggingface.co/datasets/LLMs4CodeSecurity/SV-TrustEval-C-1.0}} },
keywords = {source code vulnerability;large language model},
doi = {10.1109/SP61157.2025.00191},
url = {https://doi.ieeecomputersociety.org/10.1109/SP61157.2025.00191},
publisher = {IEEE Computer Society},
address = {Los Alamitos, CA, USA},
month =May}
```



## 📄 License
Released under the **MIT License**. See [LICENSE](LICENSE) for details.

