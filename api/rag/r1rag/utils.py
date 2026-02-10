import os
import time
import base64
from typing import Optional
from openai import AzureOpenAI, OpenAI
import requests
import re
def strip_code_fences(text: str) -> str:
    text = text.strip()
    # Strip leading triple backticks (optionally followed by a language spec)
    text = re.sub(r'^```[a-zA-Z0-9]*\n?', '', text)
    # Strip trailing triple backticks
    text = re.sub(r'\n?```$', '', text)
    return text.strip()

def get_client():
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        KEY = os.getenv("AZURE_OPENAI_API_KEY")
        ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
        client = AzureOpenAI(  
            azure_endpoint=ENDPOINT,  
            api_key=KEY,  
            api_version="2024-05-01-preview",  
        )
        return client, "gpt-4o"
    elif os.getenv("OPENAI_API_KEY"):
        KEY = os.getenv("OPENAI_API_KEY")
        BASE_URL = os.getenv("OPENAI_BASE_URL")
        client = OpenAI(
            api_key=KEY,
            base_url=BASE_URL
        )
        return client, "gpt-4o"
    else:
        raise ValueError("Either (AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT) or OPENAI_API_KEY must be set")

def call_gpt4(prompt: str, system_message: str = "You are an effective first perspective assistant.", temperature=0.9, top_p=0.95,max_tokens=2200) -> Optional[str]:
    """
    Call GPT-4 API with given prompt and system message.
    
    Args:
        prompt (str): The user prompt to send to GPT-4
        system_message (str): System message to set context for GPT-4
        
    Returns:
        Optional[str]: The response content from GPT-4, or None if request fails after retries
    """
    # Configuration
    client, model_name = get_client()

    chat_prompt = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": system_message,
                }
            ]
        },
        {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt,
            }
        ]
    }]
    messages = chat_prompt
    

    retries = 5
    for attempt in range(retries):
        try:
    
            completion = client.chat.completions.create(  
                model=model_name,  
                messages=messages,  
                max_tokens=max_tokens,  
                temperature=temperature,  
                top_p=top_p,  
                frequency_penalty=0,  
                presence_penalty=0,  
                stop=None,  
                stream=False
                )
        
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Attempt {attempt + 1} failed. Error: {e}")
            if attempt < retries - 1:  # No delay needed after the last attempt
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print("All retry attempts failed.")
                return "error"