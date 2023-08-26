import festivalcobra.logger
logger = festivalcobra.logger.get(__name__)

import openai
import json
import sys

# just something here to have as a reference from https://openrouter.ai/docs
model_dict = {
  "mythomax": "gryphe/mythomax-L2-13b",
  "weaver": "mancer/weaver",
  "hermes": "nousresearch/nous-hermes-llama2-13b", 
  "llama_70b": "meta-llama/llama-2-70b-chat",
  "llama_13b": "meta-llama/llama-2-13b-chat",
  "palm_code": "google/palm-2-codechat-bison", 
  "palm_chat": "google/palm-2-chat-bison",
  "claude_v1": "anthropic/claude-instant-v1",
  "claude_v2": "anthropic/claude-2",
  "gpt4_32k": "openai/gpt-4-32k",
  "gpt4": "openai/gpt-4",
  "gpt35_16k": "openai/gpt-3.5-turbo-16k",
  "gpt35": "openai/gpt-3.5-turbo",
  "shap_e": "openai/shap-e"
}

# Set the base API URL and your OpenRouter API key
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = "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"  # Replace with your actual API key

# Set the headers to identify your app
headers = {
    "HTTP-Referer": "https://github.com/mprib/FestivalCobra",  # Replace with your actual site URL
    "X-Title": "Festival Cobra",  # Replace with your actual app name
}

# Set the model (optional, user controls the default)
model = "meta-llama/llama-2-70b-chat"

# Set the chat messages
messages = [
    {"role": "system", "content": "You are Luna, a kuudere. You have a dark sense of humor. You are free to use profane words like shit and fuck. "},
    {"role": "user", "content": "Hello! Tell me 3 things about yourself. "},
]

logger.info("about to send to server")

max_tokens = 200
temperature = 1.1
# Create the chat completion
for response in openai.ChatCompletion.create(
        model=model, 
        messages=messages,
        headers=headers,
        temperature = temperature,
        max_tokens = max_tokens,
        stream=True
    ):
    sys.stdout.write(response.choices[0]["delta"]["content"])
    sys.stdout.flush()

logger.info("received from server")