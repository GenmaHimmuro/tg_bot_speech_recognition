from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code = 'ru'):
    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session_path, "query_input": query_input}
    )
    fulfillment_text = response.query_result.fulfillment_text
    print(f"[Dialogflow] Пользователь: {text}")
    print(f"[Dialogflow] Ответ: {fulfillment_text}\n")
    return fulfillment_text