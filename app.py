from pydantic import BaseModel, Field
import requests, json
from transformers import AutoTokenizer

autoTokenizer = AutoTokenizer.from_pretrained("gpt2-large")
url = 'https://train-an3ugzje9rw5ysaeq3s0-gpt2-train-teachable-ainize.endpoint.ainize.ai/predictions/gpt-2-en-medium-finetune'

class TextGenerationInput(BaseModel):
    Text_Input : str
    Length : int = Field(
        10,
        ge=5,
        le=30,
        descrption = "The length of the sequence to be generated"
    )

class TextGenerationOutput(BaseModel):
    Text_Output_1 : str
    Text_Output_2 : str
    Text_Output_3 : str

def generate_resume(input: TextGenerationInput)-> TextGenerationOutput:
    encoded = autoTokenizer.encode(input.Text_Input)
    data = {
        'text' : encoded,
        'length' : input.Length,
        'num_samples' : 3
    }
    response = requests.post(url, data = json.dumps(data) , headers = {"Content-Type":'application/json; charset=utf-8'})
    if response.status_code == 200:
        text = dict()
        res = response.json()
        for idx, output in enumerate(res):
            text[idx] = autoTokenizer.decode(res[idx], skip_special_tokens = True)
        return TextGenerationOutput(Text_Output_1 = text[0], Text_Output_2 = text[1], Text_Output_3 = text[2])
    else:
        return TextGenerationOutput(Text_Output_1 = response.status_code)