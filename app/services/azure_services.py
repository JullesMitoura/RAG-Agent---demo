from langchain_openai.chat_models import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
import os
import logging

class AzureServices:
    def __init__(self):
        self.azure_endpoint = os.getenv("OPENAI_URL")
        self.openai_api_key = os.getenv("OPEN_AI_KEY")
        self.llm_model = os.getenv("LLM_MODEL")
        self.embedding_model = os.getenv("EMBEDDING_MODEL")
        self.llm_api_version = "2023-07-01-preview"
        self.embedding_api_version = "2024-02-01"

        if not all([self.azure_endpoint, self.openai_api_key, self.llm_model, self.embedding_model]):
            raise ValueError("One or more required environment variables are not set.")

        logging.basicConfig(level=logging.INFO)

    def define_llm(self, temperature=0.4, max_tokens=1000):
        """Define and return the AzureChatOpenAI language model."""
        try:
            llm_model = AzureChatOpenAI(
                openai_api_version=self.llm_api_version,
                azure_endpoint=self.azure_endpoint,
                openai_api_key=self.openai_api_key,
                azure_deployment=self.llm_model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            logging.info("Language model defined successfully.")
            return llm_model
        except Exception as e:
            logging.error(f"Failed to define language model: {str(e)}")
            raise

    def define_embedding(self):
        """Define and return the AzureOpenAIEmbeddings model."""
        try:
            embedding_model = AzureOpenAIEmbeddings(
                api_key=self.openai_api_key,
                api_version=self.embedding_api_version,
                deployment=self.embedding_model,
                azure_endpoint=self.azure_endpoint
            )
            logging.info("Embedding model defined successfully.")
            return embedding_model
        except Exception as e:
            logging.error(f"Failed to define embedding model: {str(e)}")
            raise