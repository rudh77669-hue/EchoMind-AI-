import easyocr
import numpy as np
from dotenv import load_dotenv
import os
import openai as op
import io
from PIL import Image
# from flask import request
# from transformers import pipeline

load_dotenv()

op.api_key=os.getenv("OPEN_ROUTER_API_KEY")
op.api_base="https://openrouter.ai/api/v1"
reader=easyocr.Reader(['hi','en'])

def image(image_file):
        image_path=Image.open(image_file)
        image_np=np.array(image_path)
        results=reader.readtext(image_np)
        ocr_text="\n".join([text for _,text,_ in results])
        generated_text=f"\n Extracted text: {ocr_text}"
        return f"{generated_text}" if generated_text else "No text found in image"

# a=input(":")

# image(a)