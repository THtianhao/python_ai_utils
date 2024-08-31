import base64

import requests
import json

api_base = 'https://linkv-aigc-gpt4turbo.openai.azure.com/'
deployment_name = 'gpt-4-vision'
API_KEY = ''

base_url = f"{api_base}openai/deployments/{deployment_name}"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Prepare endpoint, headers, and request body
base64_image = encode_image("/Users/toto/Desktop/0a7e935da9de58c150262e9ea6e1df60e4064d35.jpg")
endpoint = f"{base_url}/chat/completions?api-version=2023-12-01-preview"
data = {
    "messages": [
        {"role": "system", "content": "用中文描述一下这张图片"},
        {"role": "user", "content": [
            {
                "type": "text",
                "text": "Describe this picture:"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]}
    ],
    "max_tokens": 2000
}

# Make the API call
response = requests.post(endpoint, headers=headers, data=json.dumps(data))

print(f"Status Code: {response.status_code}")
print(response.text)
