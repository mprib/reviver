import requests
import reviver.logger
logger = reviver.logger.get(__name__)

from keys import OPEN_ROUTER_API_KEY
import json

headers = {
    'Authorization': f'Bearer {OPEN_ROUTER_API_KEY}',
}

response = requests.get('https://openrouter.ai/api/v1/auth/key', headers=headers)

# to view the response content
print(response.content)

key_data_json = response.content.decode() # comes in as a byte string
key_data = json.loads(key_data_json)

original_key_limit = key_data["data"]["limit"]
key_usage = key_data["data"]["usage"]
limit_remaining = key_data["data"]["limit_remaining"]

logger.info(f"Key Limit: {original_key_limit}")
logger.info(f"Key Usage: {key_usage}")
logger.info(f"Remaining Limit: {limit_remaining}")
