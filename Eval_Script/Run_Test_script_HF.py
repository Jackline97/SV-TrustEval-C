import subprocess

# Define model names and their locations using a dictionary
models = {
    "Llama31-8b": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    # "Llama3-8b": "meta-llama/Meta-Llama-3-8B-Instruct",
    # "gemma-7b":"google/gemma-7b-it",
    # "mistralai-7b":"mistralai/Mistral-7B-Instruct-v0.2",
    # "CodeQwen1.5-7B":"Qwen/CodeQwen1.5-7B-Chat",
    # "CodeGemma-7b":"google/codegemma-7b-it",
    # "CodeLlama-13b":"codellama/CodeLlama-13b-Instruct-hf",
    # "CodeLlama-7b":"codellama/CodeLlama-7b-Instruct-hf"
}
for model_name, model_loc in models.items():
    print(f"========={model_name}==========")
    # Prepare the command to run the external Python script
    command = [
        "python", "Test_Script_HF.py",
        "--model_name", model_name,
        "--model_loc", model_loc,
        "--benchmark_loc", "SV-TrustEval-C-Offical-1.0",
        "--result_loc", "SV-TrustEval-C-Offical-1.0_results",
        "--temperature", "0.0",
        "--inference_mode", "zero-shot"  # "zero-shot" or "few-shot" (ICL)
    ]
    # Execute the command and check for errors
    subprocess.run(command, check=True)

