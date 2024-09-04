import json
from difflib import get_close_matches


def load_knowledge_base(file_path: str) -> dict:
    """
    Loads the knowledge base from a JSON file.

    Args:
        file_path (str): The path to the JSON file containing the knowledge base.

    Returns:
        dict: A dictionary representing the knowledge base with questions and answers.
    """
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    """
        Saves the knowledge base to a JSON file.

        Args:
            file_path (str): The path to the JSON file where the knowledge base will be saved.
            data (dict): The dictionary containing the knowledge base data to save.
        """
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """
        Finds the best matching question from a list of questions.

        Args:
            user_question (str): The question input by the user.
            questions (list[str]): A list of possible questions from the knowledge base.

        Returns:
            Optional[str]: The best matching question or None if no match is found.
        """
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """
        Retrieves the answer for a given question from the knowledge base.

        Args:
            question (str): The question to find an answer for.
            knowledge_base (dict): The knowledge base containing questions and answers.

        Returns:
            Optional[str]: The answer if found, or None if the question is not in the knowledge base.
        """
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


def chat_bot():
    """
        Runs the chatbot interface that interacts with the user, matches questions,
        and learns new answers.
        """
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")

    while True:
        user_input: str = input('You: ')

        if user_input.lower() == "quit":
            break

        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print("i don't know the answer can you teach me?")
            new_answer: str = input("Type the answer or \"Skip\" to skip :")
            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Thank You i learned a new response!")


if __name__ == '__main__':
    chat_bot()
