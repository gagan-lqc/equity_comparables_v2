# models.py
import os

from generate_features import models


def init_model():
    """
    Initialize the Azure OpenAI model.
    """
    deployment = 'gpt4-128'  # gpt 4 turbo
    # deployment = "lqc"  # gpt 4 32k


    os.environ["AZURE_OPENAI_KEY"] = "5e9b35a369e849919d54300222083628"
    os.environ["OPENAI_API_VERSION"] = '2023-07-01-preview'
    api_version_query = f'api-version={os.environ["OPENAI_API_VERSION"]}'
    os.environ["AZURE_OPENAI_ENDPOINT"] = f"https://lqc-gpt.openai.azure.com/openai/deployments/{deployment}/chat/completions?{api_version_query}"

    llm = models.AzureOpenAI(model='gpt-4',
                             api_key=os.environ["AZURE_OPENAI_KEY"],
                             azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                             echo=False)

    return llm