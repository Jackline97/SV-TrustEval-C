# SV‑TrustEval‑C 🚨🔒

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![IEEE S&P 2025](https://img.shields.io/badge/Publication-S%26P2025-blueviolet)](https://ieeexplore.ieee.org/document/) [![Python](https://img.shields.io/badge/Python-3.6%2B-blue.svg)](https://www.python.org)

<img src="Figures/main_intro.png" alt="SV-TrustEval-C Overview" width="800"/>

**Evaluating Structure & Semantic Reasoning in LLMs for C Source Code Vulnerability Analysis**

SV‑TrustEval‑C is an open benchmark to systematically evaluate LLMs’ proficiency in understanding and reasoning about security vulnerabilities in C code. It measures both control/data flow (Structure Reasoning) and semantic vulnerability detection (Semantic Reasoning) across four core tasks.

---

## 📖 Table of Contents
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
  - [Single-Model Evaluation](#single-model-evaluation)
  - [Batch Evaluation](#batch-evaluation)
  - [Performance Analysis](#performance-analysis)
- [Benchmark Tasks](#benchmark-tasks)
- [Metrics](#metrics)
- [Dataset](#dataset)
- [Results](#results)
- [Supported Models](#supported-models)
- [Contributing](#contributing)
- [Citation](#citation)
- [License](#license)

---

## ⭐ Key Features
- ✅ **Dual Reasoning Dimensions:** Structure (ControlFlow/DataFlow) & Semantic (Baseline/Counterfactual/GoalDriven/Predictive)
- 📊 **Rich Evaluation Metrics:** Accuracy, conceptual distance, reasoning consistency
- 🔧 **Plug‑and‑Play Framework:** Compatible with Hugging Face models
- 🌐 **Open Dataset & Scripts:** Easily reproduce and extend

---

## ⚙️ Installation

```bash
git clone https://github.com/your_username/SV-TrustEval-C.git
cd SV-TrustEval-C
pip install -r requirements.txt
```

---

## 🎯 Usage

### Single-Model Evaluation

```bash
python Eval_Script/Test_Script_HF.py \
  --model_name "Llama31-8b" \
  --model_loc "meta-llama/Meta-Llama-3.1-8B-Instruct" \
  --benchmark_loc "./SV-TrustEval-C-Offical-1.0" \
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

---

## 📋 Benchmark Tasks

| Dimension | Task            | Description |
|-----------|-----------------|-------------|
| Structure | ControlFlow     | Program control-flow analysis |
| Structure | DataFlow        | Variable/data relationship comprehension |
| Semantic  | Base_questions  | Baseline vulnerability detection |
| Semantic  | Counterfactual  | Reasoning about “what-if” scenarios |
| Semantic  | GoalDriven      | Task-oriented vulnerability identification |
| Semantic  | Predictive      | Predicting unseen vulnerabilities |

---

## 📈 Metrics

- **Accuracy** across tasks
- **Conceptual Distance Sensitivity**
- **Reasoning Consistency Score**

---

## 💾 Dataset

Download the benchmark:  
👉 [SV-TrustEval-C Official v1.0](./SV-TrustEval-C-Offical-1.0.zip)

---

## 📊 Results

Results directory structure:

```bash
results/
└── LLM_result_[mode]_[temp]/
    └── [model_name]/
        ├── ControlFlow/
        ├── DataFlow/
        ├── Base_questions/
        ├── Counterfactual/
        ├── GoalDriven/
        └── Predictive/
```

<img src="Figures/results.png" alt="Evaluation Results" width="600"/>

---

## 🤖 Supported Models

Llama-3.1-8B-Instruct, Gemma-7B-IT, Mistral-7B-Instruct, CodeQwen1.5-7B, CodeGemma-7B, CodeLlama-13B/7B-Instruct, and more.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📚 Citation

```bibtex
Coming soon
```

---

## 📄 License

Released under the **MIT License**. See [LICENSE](LICENSE) for details.
