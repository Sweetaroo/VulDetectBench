import openai
from openai import OpenAI
from vuldetectbench.generation import Tasks,Agent,VulDetectBench_Engine
import os
import requests

class OpenAIAgent(Agent):
    def __init__(self):
       pass
        
    def __call__(self, prompt):
        
        if not isinstance(prompt, dict):
            raise ValueError("Prompt must be a dictionary with 'system' and 'user' keys.")
        
        system_message = prompt.get("system", "")
        user_message = prompt.get("user", "")
        
        if not user_message:
            raise ValueError("User message must be provided in the prompt.")
    
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages":[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.3
        }
        # print(user_message)
        response = requests.post(url, headers=headers, json=data)
        # print(response)
        return response.json()['choices'][0]['message']['content']

if __name__=='__main__':
    
    gpt_model=OpenAIAgent()
    tasks=Tasks(data_dir='/home/cihangxie/langgao/VulDetectBench/dataset/test',method='few-shot',task_no=[1,2,3,4,5])
    engine=VulDetectBench_Engine(model=gpt_model,save_path='./',task_and_metrics=tasks)
    engine.run()