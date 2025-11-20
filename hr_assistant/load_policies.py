from pathlib import Path

def load_policies(policy_dir: str):
    policy_files = Path(policy_dir).glob("*.txt")
    policies = {}

    for file in policy_files:
        name = file.stem
        with open(file, "r") as f:
            policies[name] = f.read()

    return policies
