from pathlib import Path
import time
from interface import Interface
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
    print("Type: exit to exit")
    while True:
        question = input("Q: ").strip()
        if question.strip().lower() == "exit":
            break

        while True:
            try:
                print("A:", hr.ask(question), end="\n\n")
                break
            except Exception as e:
                time.sleep(1)



    print("Exiting...")


if __name__ == "__main__":
    load_dotenv()
    main()