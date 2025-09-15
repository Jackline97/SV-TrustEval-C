import subprocess

command = [
    "python", "Eval_script.py",
    "--root_folder", "SV-TrustEval-C-Official-1.0_results/LLM_result_zero-shot_0.0",
    "--save_path", "SV-TrustEval-C-Official-1.0_results/eval_score",
]
# Execute the command and check for errors

subprocess.run(command, check=True)
