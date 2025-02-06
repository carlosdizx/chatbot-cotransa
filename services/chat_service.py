from langchain_openai import ChatOpenAI


class ChatService:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", temperature: float = 0) -> None:
        self.llm = ChatOpenAI(model=model, temperature=temperature, api_key=api_key)

    def generate_response(self, messages: list) -> str:
        try:
            response = self.llm.invoke(messages).content
            return response
        except Exception as e:
            raise RuntimeError(f"Error al generar la respuesta: {e}") from e
