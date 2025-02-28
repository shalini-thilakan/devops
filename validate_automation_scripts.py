import sys
import os
import openai

ACCEPTANCE_CRITERIA = sys.argv[1]
FEATURE_FILES = sys.argv[2].split("\n")
STEP_DEF_FILES = sys.argv[3].split("\n")

openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Read test automation files
feature_text = read_file_content(FEATURE_FILES)
step_def_text = read_file_content(STEP_DEF_FILES)

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

AC_IN_PLAINTEXT_RESPONSE = openai_client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "Extract and return only the acceptance criteria as plain text from this JSON."},
        {"role": "user", "content": f"{ACCEPTANCE_CRITERIA}"}
    ]
)

AC_IN_PLAINTEXT = AC_IN_PLAINTEXT_RESPONSE["choices"][0]["message"]["content"]


# AI Validation using OpenAI
response = openai_client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": "You are an expert in BDD test automation."},
        {"role": "user", "content": f"Here are the acceptance criteria:\n{AC_IN_PLAINTEXT}\n\nDoes the following test automation fully cover the criteria?\nFeature Files:\n{feature_text}\n\nStep Definitions:\n{step_def_text}"}
    ]
)

validation_result = response["choices"][0]["message"]["content"]

print("\n🔹 AI VALIDATION RESULT 🔹")
print(validation_result)
print("\n----------------------------------\n")

if "no" in validation_result.lower():
    print("❌ Automation test coverage is incomplete.")
    sys.exit(1)
else:
    print("✅ Automation test coverage is sufficient.")
    sys.exit(0)
