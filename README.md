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
Download the benchmark (v1.0):
👉 [SV-TrustEval-C Official Dataset](./SV-TrustEval-C-Offical-1.0.zip)



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



## 🤝 Contributing
Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and file issues or pull requests.



## 📚 Citation
```
Accepted by IEEE Symposium on Security and Privacy (S&P) 2025! Paper will come soon
```



## 📄 License
Released under the **MIT License**. See [LICENSE](LICENSE) for details.

