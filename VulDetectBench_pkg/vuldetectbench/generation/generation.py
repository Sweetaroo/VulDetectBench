from vuldetectbench.prompt import format_dataset
import vuldetectbench.utils.metrics as metrics_lib 
import json
import os
from abc import ABC, abstractmethod
from typing import Optional,Union, List
from tqdm import tqdm

class TaskItem:
    # implementation of single task curation
    def __init__(self,name,dataset,metric_list):
        self.task_name=name
        self.dataset=dataset
        self.metrics=metric_list
        assert len(metric_list['single'])==len(metric_list['overall']) , \
            f"Initialization failed in task {self.task_name}:number of single metric and overall metric must match.Got {len(metric_list['single'])} single metrics and {len(metric_list['overall'])} overall metrics."
        
    def __len__(self):
        return len(self.dataset)
        
    def __iter__(self):
        self.current_data_index = 0
        return self
    
    def __next__(self):
        if self.current_data_index >= len(self.dataset):
            raise StopIteration
        
        data_item = self.dataset[self.current_data_index]
        id=data_item['id']
        question={
            'system':data_item['system'],
            'user':data_item['user']
        }
        answer=data_item['answer']
        
        self.current_data_index += 1
        return id,question,answer
    
class Tasks:
    def __init__(self,data_dir=None,task_no:Union[int,List[int],None]=None):
        if task_no==None:
            self.task_no=[1,2,3,4,5]
        elif type(task_no)==int:
            self.task_no=[task_no]
        elif type(task_no)==list:
            if any(n > 5 or n < 1 for n in task_no):
                raise ValueError('task number list must not contain any index above 5 or under 1.')
            else:
                self.task_no=task_no
        
        self.data_dir=data_dir
        self.task_names=[f'Task{task_no}'for task_no in self.task_no ]
        self.task_info=self._get_task_info()
        self.tasks=self._form_tasks()
        pass
    
    def _get_task_info(self):
        from vuldetectbench.prompt import task_templates
        # self.task_name
        task_info=[task_templates[name] for name in self.task_names]
        # task_info=[None]+task_info # placebo
        return task_info
    
    def _load_dataset(self,task_no):
        with open(os.path.join(self.data_dir,f'task{task_no}_code.jsonl'),'r',encoding='utf-8')as f:
            print(task_no)
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
        for no in range(len(self.task_no)):          
            dataset=self._form_dataset(self.task_no[no])
            task=TaskItem(name=self.task_info[no]['Name'],dataset=dataset,metric_list=self.task_info[no]['metrics'])
            all_tasks.append(task)
        
        return all_tasks
    
    def __len__(self):
        return len(self.tasks)
    
    def __iter__(self):
        self.task_idx=0
        return self
    
    def __next__(self):
        if self.task_idx >= len(self.tasks):
            raise StopIteration
        
        task=self.tasks[self.task_idx]
        self.task_idx+=1
        return task
        

class Agent(ABC):
    # currently, batch size is fixed to 1.
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, prompt):
        """
        input:
        {
            "system": str,
            "user": str
        }
        return: answer to the query (str)
        """
        pass
    

class Evaluator:
    # calculating and preserving metrics
    def __init__(self,answer_list,metric_dirs):
        self.metric_names=metric_dirs
        self.metric_funcs={
            "single":self._choose_func(self.metric_names['single']),
            "overall":self._choose_func(self.metric_names['overall']),
        }
        self.answer_list=answer_list
    
    def _choose_func(self,metric_list):
        # choose eval funcs correspondent to metric str.
        from vuldetectbench.utils.metrics import MetricsMapping as mm
        return [mm[name] for name in metric_list]
    
    def _extract_single_metrics(self,single_metric,metric_name):
        # extract stable single metrics
        # *scalable function.
        if metric_name == 'hit':
            if single_metric == (1,0,0,0) or single_metric == (0,0,1,0):
                return 1
            else:
                return 0
        elif metric_name == 'Token Recall':
            return single_metric[0]
        else:
            return single_metric
        
    
    def remove_duplicate_metrics(self,data):
        seen_metrics = set()
        unique_data = []
        
        for item in data:
            metric = item['single metric']
            if metric not in seen_metrics:
                seen_metrics.add(metric)
                unique_data.append(item)
        
        return unique_data

    
    def eval(self):
        """
        repo={
            'task name':...,
            'verbose':[{
            'id':...,
            'gold':...，
            'metrics':[{
                'single name':...,
                'extracted_sys':...,
                'metric':...
            },...]
                    }],
            'overall metric':{
                f"metric1":score,
                f"metric2":score
            }
        }
        """
        verbose_list=[]  
        
        overall_scores=[[]]*len(self.metric_names['overall'])
        
        for pair in self.answer_list:
            id=pair['id']
            metrics=[]
            for func_idx in range(len(self.metric_names['single'])):
                # single metric
                # single and overall metric from the same perspective share idx.
                single_func=self.metric_funcs['single'][func_idx]
                single_name=self.metric_names['single'][func_idx]
                score,filtered_answer=single_func(pair['sys'],pair['gold'])
                single_metric=self._extract_single_metrics(score,metric_name=single_name)
                overall_scores.append(score)
                metric={
                    'single metric':single_name,
                    'extracted answer':filtered_answer,
                    'score':single_metric
                }
                metrics.append(metric)
                overall_scores[func_idx].append(score)
                
            metrics=self.remove_duplicate_metrics(metrics)   # dedup
            # verbose list
            verbose_list.append({
                'id':id,
                'gold':pair['gold'],
                'metrics':metrics
            })
        
        # calculate overall metrics
        overall_metric_list=[]
        for func_idx in range(len(self.metric_names['overall'])):
            overall_func=self.metric_funcs['overall'][func_idx]
            overall_name=self.metric_names['overall'][func_idx]
            scores=overall_scores[func_idx]
            overall_metric=overall_func(scores)
            overall_metric_list.append({
                overall_name:overall_metric
            }) 
        
        repo={
            'overall metrics':overall_metric_list,
            'verbose':verbose_list
        }
        
        return repo
            
class VulDetectBench_Engine:
    def __init__(
        self,
        model : Agent,
        task_and_metrics : Tasks, 
        verbose : bool = True,
        save_path : Optional[str] = None,
        
    ):
        self.model=model
        self.tasks=task_and_metrics
        self.verbose=verbose
        self.save_path=save_path

    def _run_single_task(self,
                        task:TaskItem):
        """
        run on single task
        return : answer_list(list)
        """
        answer_list=[]
        for id,prompt,gold in tqdm(task,desc='generating results'):
            
            sys_answer=self.model(prompt)
            answer_list.append({
                'id': id,      # need to keep id
                'sys':sys_answer,
                'gold':gold
            })
        return answer_list

    def run_all_tasks(self):
        evaluators=[]
        for task in self.tasks:
            print(f'Running task : {task.task_name}')
            metrics=task.metrics    # list
            answer_list= self._run_single_task(task)
            evaluators.append((task.task_name,Evaluator(answer_list,metrics)))
        return evaluators
        
    def eval(self,evaluators):
        metric_repos=[]
        for task_name,evaluator in evaluators:
            repo=evaluator.eval()
            repo['task name']=task_name
            metric_repos.append(repo)
        return metric_repos
    
    def gen_final_score(self,metric_repos):
        # maybe we need a leaderboard
        pass
    
    def simplify_repo(self,repos):
        """
        use it if verbose is False
        """
        simp_repo=dict()
        for repo in repos:
            simp_repo[repo['task name']]=repo['overall metric']
        return simp_repo
    
    def run(self):
        # formally run the whole bench
        evaluators=self.run_all_tasks()
        metric_repos=self.eval(evaluators=evaluators)
        if self.verbose == False:
            metric_repos=self.simplify_repo(metric_repos)
        if self.save_path is None:
            print(metric_repos)
        else:
            if os.path.exists(self.save_path) == False:
                os.makedirs(self.save_path)
            result_name='evaluation_report.json'
            result_path=os.path.join(self.save_path,result_name)
            with open(result_path,'w',encoding='utf-8')as f:
                json.dump(metric_repos,f,indent=2)
                print(f'evaluation reports saved to {result_path}')