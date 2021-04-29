# from pydantic import BaseModel

# class Input(BaseModel):
#     message: str

# class Output(BaseModel):
#     message: str

# def hello_world(input: Input) -> Output:
#     """Returns the `message` of the input data."""
#     return Output(message=input.message)
import streamlit as st
import pandas as pd
import numpy as np

st.title('Résumé for SW Developers 📄')
st.write("""It is Résumé Generator. """)
prefix = st.text_input('Enter some text')
st.write(prefix)
