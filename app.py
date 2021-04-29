from pydantic import BaseModel
import requests, json
from transformers import AutoTokenizer

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
autoTokenizer = AutoTokenizer.from_pretrained("gpt2-large")
url = 'https://train-an3ugzje9rw5ysaeq3s0-gpt2-train-teachable-ainize.endpoint.ainize.ai/predictions/gpt-2-en-medium-finetune'

class TextGenerationInput(BaseModel):
    text : str
    length : int

class TextGenerationOutput(BaseModel):
    text : str

def gen_resume(input: TextGenerationInput)-> TextGenerationOutput:
    encoded = autoTokenizer.encode(input.text)
    data = {
        'text' : encoded,
        'length' : input.length
    }
    response = requests.post(url, data = json.dumps(data) , headers = {"Content-Type":'application/json; charset=utf-8'})
    if response.status_code == 200:
        res = response.json()
        return TextGenerationOutput(text = autoTokenizer.decode(res[0], skip_special_tokens = True))
    else:
        return TextGenerationOutput(text = response.status_code)


# #Interact with FastAPI endpoint
# backend = 'http://localhost:8501/generate'
# #Encode the prefix and Request
# def process(text: str, backend :str, length : int):
#     res = requests.post(backend,)

# st.title('Résumé for SW Developers 📄')
# st.write("""It is Résumé Generator. """)
# length = st.number_input('Enter a length', min_value = 1, max_value=200, value=5)
# prefix = st.text_input('Enter some text')

# if st.button('Generate Résumé sentence'):
#     generated_text = server.process(text, backend, length)
#     st.write(generated_text)
