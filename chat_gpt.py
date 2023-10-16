import openai
openai.api_key = "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"
import os

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "what is time!"}
  ]
)

print(completion.choices[0].message["content"])



