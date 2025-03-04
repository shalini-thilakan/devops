import json
import sys
import os
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

VALIDATION_MODEL = "codellama/CodeLlama-13b-Instruct-hf"
FEATURE_FILES = sys.argv[2].split("\n")
STEP_DEF_FILES = sys.argv[3].split("\n")

with open(sys.argv[1], "r") as f:
    acceptance_criteria = json.load(f)

def read_file_content(file_paths):
    content = ""
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content += f"\n### {file_path} ###\n" + file.read() + "\n\n"
        except Exception as e:
            print(f"⚠️ Could not read file {file_path}: {e}")
    return content

# Read test automation files
feature_text = read_file_content(FEATURE_FILES)
step_def_text = read_file_content(STEP_DEF_FILES)

# Load tokenizer & model without downloading everything
tokenizer = AutoTokenizer.from_pretrained(VALIDATION_MODEL, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(VALIDATION_MODEL, device_map="auto", trust_remote_code=True)

print("Model loaded successfully!")

# coverage_report = {}
# for jira_key, criteria in acceptance_criteria.items():
#     coverage_report[jira_key] = search_criteria_in_features(criteria)



# AI Validation using Hugging Face model
validation_prompt = f"""Given the following acceptance criteria along with its corresponding JIRA key, check if the provided BDD automation scripts fully cover them.
If any criteria are missing, list them.

Acceptance Criteria in JSON format:
{acceptance_criteria}

Does the following test automation fully cover the criteria?

🔹 Feature Files:
{feature_text}

🔹 Step Definitions:
{step_def_text}

For each JIRA key and its corresponding acceptance criteria, classify the response as "Positive" or "Negative" based on whether the automation script fully covers the acceptance criteria.
Only return the word "Positive" or "Negative". Do not include the prompt in the reponse. Provide the data in tabular format.
"""

# Tokenize input
inputs = tokenizer(validation_prompt, return_tensors="pt", truncation=True, max_length=4096)
# Generate response
with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=500, temperature=0.7, do_sample=True)

validation_result = tokenizer.decode(output[0], skip_special_tokens=True)

print("\n🔹 AI VALIDATION RESULT 🔹")
print(validation_result)
print("\n----------------------------------\n")

# def search_criteria_in_features(criteria):
#     for root, _, files in os.walk(feature_files_dir):
#         for file in files:
#             if file.endswith(".feature"):
#                 with open(os.path.join(root, file), "r") as f:
#                     content = f.read()
#                     if criteria in content:
#                         return True
#     return False

# coverage_report = {}

# for jira_key, criteria in acceptance_criteria.items():
#     coverage_report[jira_key] = search_criteria_in_features(criteria)

with open("coverage_report.json", "w") as f:
    json.dump(coverage_report, f, indent=4)

print("Coverage analysis completed.")
