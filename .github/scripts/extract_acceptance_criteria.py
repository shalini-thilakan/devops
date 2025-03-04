import json
import sys

with open(sys.argv[1], "r") as f:
    jira_issues = json.load(f)

#jira_issues=json.load(sys.argv[1])

acceptance_criteria = {}

for issue in jira_issues:
    key = issue["key"]
    description = issue["fields"].get("description", "")
    
    # if "Acceptance Criteria:" in description:
    #     criteria = description.split("Acceptance Criteria:")[1].strip()
    acceptance_criteria[key] = description

with open("criteria.json", "w") as f:
    json.dump(acceptance_criteria, f, indent=4)

print(f"Extracted acceptance criteria for {len(acceptance_criteria)} issues.")
sys.stdout.flush()
