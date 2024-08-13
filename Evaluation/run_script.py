import subprocess

# Define model names and their locations using a dictionary
models = {
    "GPT35":"gpt-3.5-turbo",
    "GPT4": "gpt-4-turbo-2024-04-09"
}
# Loop over each model and run the Python script with model name and location
for model_name, model_loc in models.items():
    print(f"========={model_name}==========")
    # Prepare the command to run the external Python script
    command = [
        "python", "GPT_Test_Script.py",
        "--model_name", model_name,
        "--model_loc", model_loc
    ]
    # Execute the command
    subprocess.run(command)
