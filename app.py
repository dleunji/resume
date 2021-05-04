from pydantic import BaseModel, Field
import requests, json
from transformers import AutoTokenizer

autoTokenizer = AutoTokenizer.from_pretrained("gpt2-large")
url = 'https://train-wrrhqlm5konh50zk93l1-gpt2-train-teachable-ainize.endpoint.ainize.ai/predictions/gpt-2-en-medium-finetune'

class TextGenerationInput(BaseModel):
    text_input : str = Field(
        ...,
        title = "Text Input",
        description = "The input text to use as basis to generate resume.",
        max_length = 30,
    )
    length : int = Field(
        10,
        title = "Length",
        description="The length of the sequence to be generated.",
        ge=5,
        le=50,
    )

class TextGenerationOutput(BaseModel):
    output_1 : str
    output_2 : str
    output_3 : str

def generate_resume(input: TextGenerationInput)-> TextGenerationOutput:
    """Generate Résumé based on a given prompt. And choose one of the best sentences. """
    encoded = autoTokenizer.encode(input.text_input)
    data = {
        'text' : encoded,
        'length' : input.length,
        'num_samples' : 3
    }
    response = requests.post(url, data = json.dumps(data) , headers = {"Content-Type":'application/json; charset=utf-8'})
    if response.status_code == 200:
        text = dict()
        res = response.json()
        for idx, output in enumerate(res):
            text[idx] = autoTokenizer.decode(res[idx], skip_special_tokens = True)
        return TextGenerationOutput(output_1 = text[0], output_2 = text[1], output_3 = text[2])
    else:
        return TextGenerationOutput(text_output_1 = response.status_code)