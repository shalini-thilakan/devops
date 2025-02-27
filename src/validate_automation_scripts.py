import sys
import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def validate_test_cases(acceptance_criteria, test_files):
    with open(test_files, "r") as file:
        test_script = file.read()

    prompt = f"""
    Given the following acceptance criteria from JIRA:

    {acceptance_criteria}

    And the following automation test script:

    {test_script}

    Analyze whether the test script correctly validates all the acceptance criteria. 
    List any missing validations or incorrect implementations.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert test case validator."},
                  {"role": "user", "content": prompt}]
    )

    result = response["choices"][0]["message"]["content"]
    print(result)

    if "missing" in result.lower() or "does not validate" in result.lower():
        sys.exit(1)

if __name__ == "__main__":
    acceptance_criteria = sys.argv[1]
    test_files = sys.argv[2]
    validate_test_cases(acceptance_criteria, test_files)
