import sys
import os
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

ACCEPTANCE_CRITERIA = sys.argv[1]
FEATURE_FILES = sys.argv[2].split("\n")
STEP_DEF_FILES = sys.argv[3].split("\n")

EXTRACTION_MODEL = "mistralai/Mistral-7B-v0.1"
VALIDATION_MODEL = "codellama/CodeLlama-13b-Instruct-hf"

def read_file_content(file_paths):
    content = ""
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content += f"\n### {file_path} ###\n" + file.read() + "\n\n"
        except Exception as e:
            print(f"⚠️ Could not read file {file_path}: {e}")
    return content

# Print fetched acceptance criteria
print("\n🔹 ACCEPTANCE CRITERIA FROM JIRA 🔹")
print(ACCEPTANCE_CRITERIA)
print("\n----------------------------------\n")


# Load a Hugging Face LLM for text generation (e.g., `mistralai/Mistral-7B-Instruct`)
# extract_pipeline = pipeline("text-generation", model=f"{EXTRACTION_MODEL}")

# # Extract plain text acceptance criteria from JSON
# extraction_prompt = f"Extract and return only the acceptance criteria as plain text from this JSON:\n{ACCEPTANCE_CRITERIA}"
# AC_IN_PLAINTEXT = extract_pipeline(extraction_prompt, max_new_tokens=200)[0]['generated_text']

# # Print fetched acceptance criteria
# print("\n🔹 Extracted ACCEPTANCE CRITERIA 🔹")
# print(AC_IN_PLAINTEXT)
# print("\n----------------------------------\n")


# Read test automation files
feature_text = read_file_content(FEATURE_FILES)
step_def_text = read_file_content(STEP_DEF_FILES)

# Load tokenizer & model without downloading everything
tokenizer = AutoTokenizer.from_pretrained(VALIDATION_MODEL, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(VALIDATION_MODEL, device_map="auto", trust_remote_code=True)

print("Model loaded successfully!")

# Load a model for validation (e.g., `bigcode/starcoder` for code analysis)
#validation_pipeline = pipeline("text-generation", model)

# AI Validation using Hugging Face model
validation_prompt = f"""Given the following acceptance criteria, check if the provided BDD automation scripts fully cover them.
If any criteria are missing, list them.

Acceptance Criteria in JSON format:
{ACCEPTANCE_CRITERIA}

Does the following test automation fully cover the criteria?

🔹 Feature Files:
{feature_text}

🔹 Step Definitions:
{step_def_text}

Classify the response as "Positive" or "Negative" based on whether the automation script fully covers the acceptance criteria.
Only return "Positive" or "Negative".
"""

#validation_result = validation_pipeline(validation_prompt, max_new_tokens=200)[0]['generated_text']

# Tokenize input
inputs = tokenizer(validation_prompt, return_tensors="pt", truncation=True, max_length=4096)
# Generate response
with torch.no_grad():
    output = model.generate(**inputs, max_new_tokens=500, temperature=0.7, do_sample=True)

validation_result = tokenizer.decode(output[0], skip_special_tokens=True)

print("\n🔹 AI VALIDATION RESULT 🔹")
print(validation_result)
print("\n----------------------------------\n")

# RESULT_CLASSIFICATION_PROMPT = f"""
# Classify the following response as "Positive" or "Negative" based on whether the automation script fully covers the acceptance criteria:

# Response:
# {validation_result}

# Only return "Positive" or "Negative".
# """

# clsfn_inputs = tokenizer(RESULT_CLASSIFICATION_PROMPT, return_tensors="pt")
# clsfn_outputs = model.generate(**clsfn_inputs, max_new_tokens=100)
# classification = tokenizer.decode(clsfn_outputs[0], skip_special_tokens=True)

# print("\n🔹 CLASSIFICATION 🔹")
# print(classification)
# print("\n----------------------------------\n")

if "negative" in validation_result.lower():
    print("❌ Automation test coverage is incomplete.")
    sys.exit(1)
else:
    print("✅ Automation test coverage is sufficient.")
    sys.exit(0)
