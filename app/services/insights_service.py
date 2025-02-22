from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def chat_with_assistant(messages, dataset_context: str):
    # Create an initial instruction that includes the entire dataset content
    initial_instruction = f"""You are a data visualization expert and data analyst. Below is the complete dataset:
{dataset_context}
Please answer the user's query in a conversational manner, similar to ChatGPT."""

    formatted_messages = [{"role": "user", "content": initial_instruction}] + messages

    try:
        response = client.chat.completions.create(
            model="o1-mini-2024-09-12", messages=formatted_messages
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in chat_with_assistant: {str(e)}")
        raise
