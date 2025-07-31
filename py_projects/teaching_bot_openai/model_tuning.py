#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 20:14:51 2024

@author: yajingliu
"""
import openai
from openai import OpenAI
import constants
import time
import os

# Initialize the OpenAI client.
os.environ['OPENAI_API_KEY'] = constants.API_KEY
client = OpenAI()

# Load the training file.
training_file = client.files.create(
  file = open("rabbit_chicken.jsonl", "rb"),
  purpose = "fine-tune"
)

# Fine tune the model.
try:
    fine_tuning_job = client.fine_tuning.jobs.create(
      training_file = training_file.id, 
      model = "gpt-3.5-turbo-1106",
    )
    print("Created a job:\nJob:\n", fine_tuning_job)
except:
    print("Failed creating the fine tuning job.")    

finished_at = None
fine_tuned_model = None
while not finished_at:
    try:
        print("\nGet the model status...")
        status = client.fine_tuning.jobs.retrieve(fine_tuning_job.id)
        print(f"Status:\n {status}")
        finished_at = status.finished_at # job finished at 
        model_id = status.fine_tuned_model
        if finished_at is not None:
            break
        if status.error.code is not None:
            print("\nThere is an error\nError:\n", status.error) 
            break
    except:
        break
    
    print("Waiting...\nSleep for 1 minutes.")
    time.sleep(60)
    
print(f"fine_tune_model: {status}")

# List all the model tuning jobs
# client.fine_tuning.jobs.list()


    