from openai import OpenAI
import json

with open('../config/XAI.json', 'r') as f:
    xai_config = json.load(f)

client = OpenAI(
  api_key=xai_config['api_key'],
  base_url=xai_config['NORMAL_BASE_URL'],
  #base_url="https://api.x.ai/v1",
)

message = [
    {"role": "system", "content": "You are a PhD-level mathematician."},
    {"role": "user", "content": "What is 2 + 2?"},
]

completion = client.chat.completions.create(
  model="grok-3",
  messages= message,

)

print(completion.choices[0].message)
