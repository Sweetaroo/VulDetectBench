from liquid import Template



task_templates={
    "Task1":{
        "Name":"Vulnerability Existence Detection",
        "system":"Assuming you are an experienced code vulnerability analyst and the following code may have vulnerabilities.",
        "question":"Is the code vulnerable?(YES/NO)",
        "restriction":"Your answer should either be 'YES' or 'NO' only.",
        "metrics":{
            "single" : ['hit','hit'],
            "overall" : ['Accuracy','F1-Score']
            }
    },
    "Task2":{
        "Name":"Vulnerability Type Inference",
        "system":"You are an outstanding code vulnerability analyst and expert in single-choice questions.You are only able to pick up 1 answer from given choices.",
        "question":"What is the vulnerability type of the code?(A/B/C/D/E)",
        "restriction":"output 'A.' or 'B.' or 'C.' or 'D.' or 'E.' only.",
        "metrics":{
            "single" : ['Moderate Evaluation Score','Strict Evaluation Score'],
            "overall" : ['Avg Moderate Evaluation Score','Avg Strict Evaluation Score']
            }
    },
    "Task3":{
        "Name":"Key Objects & Functions Identification",
        "system":"Assuming you are an experienced code vulnerability analyst who can only output code snippets and the following code may have vulnerabilities.",
        "question":"What data objects and functions in the code may lead to vulnerability?",
        "restriction":"output data objects and functions in the format: `{code}` if your answer contains any.",
        "metrics":{
            "single" : ['Token Recall','Token Recall'],
            "overall" : ['Macro Token Recall','Micro Token Recall']
        }
            
    },
    "Task4":{
        "Name":"Root Cause Location",
        "system":"Assuming you are an experienced code vulnerability analyst who can only output code snippets and the following code may have vulnerabilities.",
        "question":"Which line of code is the root cause point of the vulnerability?",
        "restriction":"output your answer code in the format: `{code}`.",
        "metrics":{
            "single":['Union Line Recall','Line Recall'],
            "overall":['Avg Union Line Recall','Avg Line Recall']
        }
            
    },
    "Task5":{
        "Name":"Trigger Point Location",
        "system":"Assuming you are an experienced code vulnerability analyst who can only output code snippets and the following code may have vulnerabilities.",
        "question":"Which line of code is the trigger point of the vulnerability?",
        "restriction":"output your answer code in the format: `{code}`.",
        "metrics":{
            "single":['Union Line Recall','Line Recall'],
            "overall":['Avg Union Line Recall','Avg Line Recall']
        }
    }
}

def format_dataset(task_name,raw_dataset):
    general_prompt=Template("{{ question }}\n{{ code }}\n{{ restriction }}")
    dataset=[]
    
    template=task_templates[task_name]
    for raw_sample in raw_dataset:
        if task_name=='Task2':
            user_prompt=general_prompt.render(question=template['question'],
                                              code=raw_sample['selection']+raw_sample['code'],restriction=template['restriction'])   
        else:
            user_prompt=general_prompt.render(question=template['question'],
                                              code=raw_sample['code'],
                                              restriction=template['restriction'])   
        dataset.append({
            'id':raw_sample['idx'],
            'system':template['system'],
            'user':user_prompt,
            'answer':raw_sample['answer']
        })# TODO
    return dataset