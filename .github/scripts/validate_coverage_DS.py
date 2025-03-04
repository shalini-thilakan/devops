import json
import sys
import os
import openai

OPENROUTER_API_KEY = os.getenv("DEEPSEEK_API_KEY")
FEATURE_FILES = sys.argv[2].split("\n")
STEP_DEF_FILES = sys.argv[3].split("\n")

# Define DeepSeek model
MODEL = "deepseek-ai/deepseek-coder-1.3b-instruct"
# Initialize OpenRouter client
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = OPENROUTER_API_KEY

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

print("Model loaded successfully!")

# coverage_report = {}
# for jira_key, criteria in acceptance_criteria.items():
#     coverage_report[jira_key] = search_criteria_in_features(criteria)

def analyze_bdd_coverage(acceptance_criteria, feature_text, step_def_text):
    openai_client = openai.OpenAI(api_key=openai.api_key) 
    validation_prompt = f"""
    Given the following acceptance criteria in JSON format, verify if they are fully covered in the provided BDD automation scripts. 

    Acceptance Criteria:
    {acceptance_criteria}

    Feature File:
    {feature_text}

    Step Definitions:
    {step_def_text}

    Analyze and respond with only this:
    1. Which acceptance criteria are fully covered?
    2. Which acceptance criteria are partially covered or missing?
    3. Suggestions for improving test coverage.
    """

    response = openai_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": validation_prompt}],
        max_tokens=1000
    )

    return response["choices"][0]["message"]["content"]

analysis_result = analyze_bdd_coverage(acceptance_criteria, feature_text, step_def_text)

print("\n🔹 Analysis Result : 🔹")
print(analysis_result)
print("\n----------------------------------\n")

print("Coverage analysis completed.")
