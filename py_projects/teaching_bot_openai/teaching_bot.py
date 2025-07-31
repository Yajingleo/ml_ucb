#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 20:14:51 2024

@author: yajingliu
"""
import openai
from openai import OpenAI
import constants
import os
import sys

# Initialize the OpenAI client
os.environ['OPENAI_API_KEY'] = constants.API_KEY
GPT_MODEL_ID = 'ft:gpt-3.5-turbo-0125:personal::9b0IDMy4'

client = OpenAI()        

if __name__ == "__main__":
    args = sys.argv[1:]
    
    questions = args[0]
    
    completion = client.chat.completions.create(
      model=GPT_MODEL_ID,
      messages=[
        {"role": "system", "content": "我们在给小学生讲数学题。"},
        {"role": "user", "content": questions}
      ]
    )

    print(completion.choices[0].message.content)