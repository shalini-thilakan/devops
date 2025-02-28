import sys
import os
from transformers import pipeline

ACCEPTANCE_CRITERIA = sys.argv[1]
FEATURE_FILES = sys.argv[2].split("\n")
STEP_DEF_FILES = sys.argv[3].split("\n")

EXTRACTION_MODEL = "mistralai/Mistral-7B-v0.1"
VALIDATION_MODEL = "bigcode/starcoder"

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
extract_pipeline = pipeline("text-generation", model=f"{EXTRACTION_MODEL}")

# Extract plain text acceptance criteria from JSON
extraction_prompt = f"Extract and return only the acceptance criteria as plain text from this JSON:\n{ACCEPTANCE_CRITERIA}"
AC_IN_PLAINTEXT = extract_pipeline(extraction_prompt, max_new_tokens=200)[0]['generated_text']

# Print fetched acceptance criteria
print("\n🔹 Extracted ACCEPTANCE CRITERIA 🔹")
print(AC_IN_PLAINTEXT)
print("\n----------------------------------\n")


# Read test automation files
feature_text = read_file_content(FEATURE_FILES)
step_def_text = read_file_content(STEP_DEF_FILES)

# Load a model for validation (e.g., `bigcode/starcoder` for code analysis)
validation_pipeline = pipeline("text-generation", model=f"{VALIDATION_MODEL}")

# AI Validation using Hugging Face model
validation_prompt = f"You are an expert in BDD test automation. Here are the acceptance criteria:\n{AC_IN_PLAINTEXT}\n\nDoes the following test automation fully cover the criteria?\nFeature Files:\n{feature_text}\n\nStep Definitions:\n{step_def_text}"
validation_result = validation_pipeline(validation_prompt, max_new_tokens=200)[0]['generated_text']


print("\n🔹 AI VALIDATION RESULT 🔹")
print(validation_result)
print("\n----------------------------------\n")

if "no" in validation_result.lower():
    print("❌ Automation test coverage is incomplete.")
    sys.exit(1)
else:
    print("✅ Automation test coverage is sufficient.")
    sys.exit(0)
