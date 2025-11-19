from pathlib import Path
from interface import Interface
import pandas as pd
from dotenv import load_dotenv

def load_policies(policy_dir: str):
    policy_files = Path(policy_dir).glob("*.txt")
    policies = {}

    for file in policy_files:
        name = file.stem
        with open(file, "r") as f:
            policies[name] = f.read()

    return policies


def main():
    policy_path = "./Policies"

    print("Initialising HR assistant...")
    hr = Interface("hr_policies")

    print("Loading policies...")
    policies = load_policies(policy_path)
    for name, text in policies.items():
        hr.add_policy(name, text)

    print("------ HR Chatbot Demo ------")
    print("Q: How many days annual leave do I get?")
    print("A:", hr.ask("How many days annual leave do I get?"), "\n")

    print("Q: Can I work from home?")
    print("A:", hr.ask("Can I work from home?"), "\n")

    print("Exiting...")


if __name__ == "__main__":
    load_dotenv()
    main()
