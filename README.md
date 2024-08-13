# SV-TrustEval: Evaluating Semantic and Structural Trustworthiness of Source Code Vulnerability Analysis

Welcome to the official repository for the SV-TrustEval benchmark, introduced in our latest research to critically assess the semantic and structural analysis capabilities of Large Language Models (LLMs) on source code vulnerabilities. This benchmark is specifically designed to address significant gaps in evaluating the reliability of LLMs' vulnerability analysis, which is crucial for their trustworthy application in real-world cybersecurity tasks.

## About SV-TrustEval
![Overview of SV-TrustEval](Figures/combine_QA.png)
SV-TrustEval provides a comprehensive framework to evaluate how well LLMs can understand and reason about code, particularly focusing on identifying and predicting vulnerabilities within the C programming language. The benchmark comprises two main components:
- **Structure Reasoning:** Assesses the ability of LLMs to accurately discern the relationships between code elements and predict how changes can propagate errors or vulnerabilities.
- **Semantic Reasoning:** Tests the LLMs' ability to maintain analysis accuracy across various coding scenarios, including counterfactuals, goal-driven modifications, and predictive assessments.

## Key Contributions

- **Novel Benchmarking Approach:** Introduces new methods to measure the analytical depth of LLMs concerning code structure and semantics.
- **Insightful Evaluations:** Offers in-depth insights into the current limitations and capabilities of state-of-the-art LLMs in handling complex code analysis tasks.
- **Open Resource:** Provides a valuable dataset and evaluation metrics for the community to engage with and improve upon the robustness of code vulnerability analysis tools.

## Dataset Access

The benchmark dataset, detailed evaluation protocols, and additional resources are available at: [SV-TrustEval Dataset](https://tinyurl.com/5xmzyerk)

## How to Use This Repository

This repository contains scripts to run the benchmarks, evaluate model performance, and replicate the study findings:
- `scripts/`: Directory containing scripts to execute benchmark tests.
- `data/`: Folder with sample data and links to the full benchmark dataset.
- `docs/`: Documentation on benchmark methodology and usage instructions.

## Contributing

We welcome contributions from the community to extend and refine this benchmark. Please read the [CONTRIBUTING.md](./CONTRIBUTING.md) file for guidelines on how to contribute.

## License

This project is licensed under the terms of the MIT license.

---

Feel free to adapt the README to include more specific links, installation guides, or usage examples as per the actual contents of your repository and research requirements!
