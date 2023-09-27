import openai
openai.api_key = "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"
import os

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
)

print(completion.choices[0].message["content"])



