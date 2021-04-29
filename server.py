import requests, json
from transformers import AutoTokenizer
from fastapi import FastAPI
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

app = FastAPI()

autoTokenizer = AutoTokenizer.from_pretrained("gpt2-large")

url = 'https://train-an3ugzje9rw5ysaeq3s0-gpt2-train-teachable-ainize.endpoint.ainize.ai/predictions/gpt-2-en-medium-finetune'

@app.post('/generate')
def generateResume(text : str, url : , ):
    item = item.json()
    prefix = item['text']
    length = item['length']
    encoded = autoTokenizer.encode(prefix)
    data = {
        'text' : encoded,
        'length' : length
    }
    response = requests.post(url, data = json.dumps(data) , headers = {"Content-Type":'application/json; charset=utf-8'})
    if response.status_code == 201:
        res = response.json()
        text = autoTokenizer.decode(res[0], skip_special_tokens = True)
        return jsonify({'text': text})
    else:
        return response.status_code

    return res
