import requests
import sys
import json
import os

JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_FIX_VERSION = sys.argv[1]

headers = {
    "Authorization": f"Bearer {JIRA_API_TOKEN}",
    "Accept": "application/json"
}

def fetch_jira_issues(fix_version):
    url = f"{JIRA_BASE_URL}/rest/api/2/search?jql=fixVersion='{fix_version}'"
    response = requests.get(url, headers=headers)

    # Print response status and JSON for debugging
    print("Response Status Code:", response.status_code)
    print("Response JSON:", response.json())

    # Handle potential errors before accessing "issues"
    if response.status_code != 200:
        raise Exception(f"JIRA API request failed: {response.text}")

    data = response.json()
    
    # Check if "issues" key exists
    if "issues" not in data:
        raise KeyError(f"'issues' key not found in response: {data}")

    return data["issues"]

issues = fetch_jira_issues(JIRA_FIX_VERSION)

with open("jira_issues.json", "w") as f:
    json.dump(issues, f)

print(f"Extracted {len(issues)} JIRA issues.")
