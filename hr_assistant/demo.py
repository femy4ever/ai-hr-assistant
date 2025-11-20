from pathlib import Path
import time
from interface import Interface
from dotenv import load_dotenv

def load_policies(policy_dir: str):
    policy_files = Path(policy_dir).glob("*.txt")

    for file in policy_files:
        name = file.stem
        yield name, file.read_text()

def initialise()
    policy_path = Path(__file__).parent.parent.join_path("Policies")

    print("Initialising HR assistant...")
    hr = Interface("hr_policies")

    print("Loading policies...")
    for name, text in load_policies(policy_path):
        hr.add_policy(name, text)
    return hr

def main():

    hr = initialise()

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