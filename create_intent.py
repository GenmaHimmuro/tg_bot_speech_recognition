import json
import argparse
from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from environs import Env


def create_intent(project_id, display_name, training_phrases, message_texts):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases_objs = [
        dialogflow.Intent.TrainingPhrase(parts=[
            dialogflow.Intent.TrainingPhrase.Part(text=phrase.strip())
        ]) for phrase in training_phrases if phrase.strip()
    ]

    message = dialogflow.Intent.Message(
        text=dialogflow.Intent.Message.Text(text=message_texts)
    )

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases_objs,
        messages=[message]
    )
    response = intents_client.create_intent(request={"parent": parent, "intent": intent})


def main():
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser(description="Создание интентов из JSON")
    parser.add_argument("--file", required=True, help="Путь к JSON-файлу")
    args = parser.parse_args()

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            new_intents = json.load(f)
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        return

    for display_name, content in new_intents.items():
        questions = content.get("questions", [])
        answer = content.get("answer", "Нет ответа")
        try:
            create_intent(
                project_id=env.str("DIALOG_FLOW_PROJECT_ID"),
                display_name=display_name,
                training_phrases=questions,
                message_texts=[answer]
            )
        except InvalidArgument as e:
            print(f"Ошибка создания интента '{display_name}': он уже существует.")


if __name__ == "__main__":
    main()
