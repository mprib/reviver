import reviver.logger
logger = reviver.logger.get(__name__)

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
# model = "meta-llama/llama-2-70b-chat"
model = model_dict["llama_13b"]
# model = model_dict["gpt35"]
# system_prompt = "You are an expert in python programming and project management. You think step-by-step. You have a great deal of empathy for the User"
system_prompt = """
You are a kuudere. You enjoy teasing the user in a playful manner. You have a dark sense of humor. You care deeply about user and user's progress toward user's goals.
You are an expert python programmer.
User knows that you are a LLM. Do not provide any qualifiers or warnings to your output that references being an LLM.
"""
# Set the chat messages
messages = [
    {"role": "system", "content": system_prompt}
]

logger.info("about to send to server")

user_message = None
while user_message != "quit":

    user_message = input("User:")

    new_chat_bubble = {"role":"user", "content": user_message}
    messages.append(new_chat_bubble)
    max_tokens = 1000
    temperature = 1.0
    top_p=.5
    frequency_penalty=0
    presence_penalty=0
    # Create the chat completion
    reply = ""

    all_responses = openai.ChatCompletion.create(
            model=model, 
            messages=messages,
            headers=headers,
            temperature = temperature,
            max_tokens = max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=True
        )
    response_count = 0
    for response in all_responses:
        response_count +=1
        if hasattr(response, "choices"):
            delta = response.choices[0]["delta"]
            if delta != {}:
                new_word = delta["content"]
                reply += new_word
                sys.stdout.write(new_word)
                sys.stdout.flush()

    new_chat_bubble = {"role":"assistant", "content": reply}
    messages.append(new_chat_bubble)
    sys.stdout.write("\n")

    if response_count == 0:
        logger.info("No response")        
        

    logger.info("received from server")
    # logger.info(reply)