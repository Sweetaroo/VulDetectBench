# 代码结构
# 数据集转化为prompt的工具
# prompt输送给模型，模型输出
# 输出的测试
# 要实现的基本工具
from prompt import task_templates,format_dataset
from utils.metrics import *
import json
import os
from abc import ABC, abstractmethod

class TaskItem:
    # implementation of single task curation
    def __init__(self,name,dataset,metric_list):
        self.task_name=name
        self.dataset=dataset
        self.metrics=metric_list
        
    def __len__(self):
        return len(self.dataset)
        
    def __iter__(self):
        self.current_data_index = 0
        return self
    
    def __next__(self):
        if self.current_index >= len(self.dataset):
            raise StopIteration
        
        data_item = self.dataset[self.current_index]
        question={
            'system':data_item['system'],
            'user':data_item['user']
        }
        answer=data_item['answer']
        
        self.current_index += 1
        return question,answer
    

class Tasks:
    def __init__(self,data_dir=None,task_no=None):
        if task_no==None:
            self.task_no=[1,2,3,4,5]
        else:
            self.task_no=[task_no]
        self.data_dir=data_dir
        self.task_names=[f'Task{task_no}'for task_no in self.task_no ]
        self.tasks=self._form_tasks()
        pass
    
    def _get_task_info(self,task_templates=task_templates):
        # self.task_name
        task_info=[task_templates[name] for name in self.task_name]
            
        return task_info
    
    def _load_dataset(self,task_no):
        with open(os.path.join(self.data_dir,'test',f'task{task_no}_code.jsonl'),'r')as f:
            raw_dataset=[json.loads(line) for line in f.readlines()]
            return raw_dataset
    
    def _form_dataset(self,task_no):
        # only a single task
        task_name=f'Task{task_no}'
        raw_dataset=self._load_dataset(task_no)
        dataset=format_dataset(task_name,raw_dataset)
        return dataset 
    
    def _form_tasks(self):
        """
        form a seires of task LLM will work on.
        return:a list of object Task
        """
        all_tasks=[]
        for no in self.task_no           
            dataset=self.form_dataset(no)
            task=TaskItem(name=self.task_info[no]['Name'],dataset=dataset,metric_list=self.task_info[no]['metrics'])
            all_tasks.append(task)
        
        return all_tasks
            
       

class Agent:
    # currently, batch size is fixed to 1.
    def __init__(self,tokenizer_path=None,
                 model_path=None,
                 api_key=None):
        pass
    
    @abstractmethod
    def __call__(self,prompt):
        """
        input:
        {
            "system":str,
            "user":str
        }
        return:answer to the query(str)    
        """
        pass
    
 # preprocessing done.TODO:evaluation code.
 
class VulDetectBench:
    def __init__():
        pass
    def _run_single_task():
        pass
    def run_exist_detect():
        pass
    def run_cls():
        pass
    def run_root_cause_detect():
        pass
    def run_trigger_point_detect():
        pass
    def run_obj_func_detect():
        pass
    def eval():
        pass
    def save_results():
        pass