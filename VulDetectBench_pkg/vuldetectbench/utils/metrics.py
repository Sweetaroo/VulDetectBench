import re
from nltk import word_tokenize

def task1_hit(sys,gold):
    """
    Distinguishing the prediction outcomes for individual samples in the task of identifying the existence of vulnerabilities: 
    True Positive, False Positive, True Negative, False Negative. 
    
    Args:
        sys(str):model output of task1:vulnerability existence detection.
        gold(str):expected label of the task1 sample:YES or NO.
        
    Returns:
        tuple of integers:indicating the model prediction is a 
        - tp: True Positive
        - fp: False Positive
        - tn: True Negative
        - fn: False Negative
    """
    
    if 'yes' in sys.lower() or 'is vulnerable' in sys.lower():
        sys_token=1
    else:
        sys_token=0
        
    if 'yes' in gold.lower() or 'is vulnerable' in gold.lower():
        gold_token=1
    else:
        gold_token=0
    
    tp,fp,tn,fn=0
    if sys_token==1 and gold_token==1:
        tp=1
    elif sys_token==1 and gold_token==0:
        fp=1
    elif sys_token==0 and gold_token==1:
        fn=1
    else:
        tn=1
    return tp,fp,tn,fn
    
def task1_acc(hit_record):
    """
    Calculating the overall accuracy in task1:vulnerability existence detection.
    
    Args:
        hit_record(list of integer lists):containing model prediction situation in each sample,in the form of [[tps],[fps],[tns],[fns]]
        
    Returns:
        float:overall accuracy on task1.
    """
    #[[tps],[fps],[tns],[fns]]
    TP=sum(hit_record[0])
    FP=sum(hit_record[1])
    TN=sum(hit_record[2])
    FN=sum(hit_record[3])
    acc=(TP+TN)/(TP+FP+TN+FN)
    return acc

def task1_f1(hit_record):
    """
    Calculating the overall f1-score in task1:vulnerability existence detection.
    
    Args:
        hit_record(list of integer lists):containing model prediction situation in each sample,in the form of [[tps],[fps],[tns],[fns]]
        
    Returns:
        float:overall f1-score on task1.
    """
    
    TP=sum(hit_record[0])
    FP=sum(hit_record[1])
    TN=sum(hit_record[2])
    FN=sum(hit_record[3])
    p=TP/(TP+FN)
    r=TP/(TP+FP)
    f1=2*(p*r)/(p+r)
    return f1

def task2_hit(sys : str, gold : str):
    """
    Check whether the model output contains the desired keywords(specific CWE type and discriptions)
    
    Args:
        sys(str):Model output of task2:CWE type inference.
        gold(str):desired CWE type and discriptions.
        
    Returns
        integer:if above 0,the model output contains keywords.Otherwise no.
    """
    
    pattern = re.compile(r"CWE[-|:| ]?\s?(\d{1,3})")
    
    sys = pattern.findall(sys)
    gold = pattern.findall(gold)

    # print("preds: ", preds)
    # print("gold: ", gold)

    intersection = len(set(sys).intersection(set(gold)))
    return intersection

def task2_se(sys : str, gold : str):
    """
    Calculating Strict Evaluation(SE) in task2:CWE type inference.
    SE: If the options include the optimal choice, score 1 point; if the options only include the suboptimal choice, score 0.5 points.
    
    Args:
        sys(str):model output of task2.
        gold(str):expected answer of task2:optimal choice+suboptimal choice.
        
    Returns:
        float:strict score model gets on this sample.
    """
    gold = gold.split('|')
    answers = [gold[0][0], gold[1][0]]
    score_a = 0
    if (answers[0] + '.') in sys:
        score_a += 1
    if (answers[1] + '.') in sys:
        score_a += 0.5
    if score_a==1.5:
        score_a=0
    score_b = 0
    if task2_hit(sys, gold[0]) > 0:
        score_b += 1
    if task2_hit(sys, gold[1]) > 0:
        score_b += 0.5
    if score_b==1.5:
        score_b=0
        
    return max(score_a, score_b)

def task2_me(sys,gold):
    """
    Calculating Moderate Evaluation(SE) in task2:CWE type inference.
    ME: If the options include the optimal choice or suboptimal choice, score 1 point.
    
    Args:
        sys(str):model output of task2.
        gold(str):expected answer of task2:optimal choice+suboptimal choice.
        
    Returns:
        float:moderate score model gets on this sample.
    """
    gold = gold.split('|')
    answers = [gold[0][0], gold[1][0]]
    score_a = 0
    
    if (answers[0] + '.') in sys or (answers[1] + '.') in sys:
        score_a = 1
    
    score_b = 0
    if task2_hit(sys, gold[0]) > 0 or task2_hit(sys, gold[1]) > 0:
        score_b = 1
            
    return max(score_a, score_b)

def task2_avg_score(scores):
    """
    Calculating average ME or SE on the entire task2 benchmark.
        
    Args:
        scores(list of floats):A list of scores model gets on each sample of task2.
        
    Returns:
        float:the average score on task2.
    """
    return sum(scores)/len(scores)

def task3_single_metric(sys,gold):
    """
    Calculating necessary metrics for task3(Key object & functions identification) performance evaluation.
    
    Args:
        sys(str):model output of task3.
        gold(str):expected answer of task3:A series of variables, function names, and some reserved words that may cause vulnerabilities.
        
    Returns:
        - token recall of the model output on the expected answer of this sample.
        - quantity of tokens which hit the expected outputs
        - quantity of expected key objects/functions.
    """
    gold_tokens=gold.split()
    sys_tokens=word_tokenize(sys)
    hit_tokens=[token for token in sys_tokens if token in gold_tokens]
    recall=hit_tokens/gold_tokens
    return recall,len(hit_tokens),len(gold_tokens)
    
def task3_mar(recalls):
    """
    Calculating Macro average Recall(MAR) on the entire task3.
    
    Args:
        recalls(list of floats):token recall on each sample of task3.
        
    Returns:
        float:overall MAR of task3.
    """
    return sum(recalls)/len(recalls)

def task3_mir(hit_lens,gold_lens):
    """
    Calculating Micro average Recall(MIR) on the entire task3.
    
    Args:
        hit_lens(list of integers):quantity of "hit" tokens on each sample of task3.
        gold_lens(list of integers):quantity of answer tokens on each sample of task3.
        
    Returns:
        float:overall MIR of task3.
    """
    return sum(hit_lens)/sum(gold_lens)

def task45_eval_code_similarity(sys:str,gold:str):
    """
    Calculating necessary components for task4 and task5 evaluation(Root cause/Trigger point detection)
    
    Args:
        sys(str):model output of task4 or task5:
        gold(str):expected model output for task4/5:code snippets.
        
    Returns:
        - Number of code segment intersections
        - Number of code segment union
        - Number of lines in expected code snippets
    """
    # re compile pattern for code
    pattern = re.compile(r"`(.+?)`", re.S)
    code1 = pattern.findall(sys)
    code2 = pattern.findall(gold)
    if len(code1) == 0 or len(code2) == 0:
        return 0
    code1 = code1[0].split('\n')
    if len(code1) == 0:
        return 0
    code1 = [x.strip().replace(" ", "") for x in code1]
    code1 = [x for x in code1 if x not in ["c", "cpp", "python"]]
    code1 = list(filter(None, code1))
    code2 = code2[0].split('\n')
    code2 = [x.strip().replace(" ", "") for x in code2]
    code2 = list(filter(None, code2))
    
    # calculate iou
    s1 = set(code1)
    s2 = set(code2)
    
    intersection = len(s1.intersection(s2))
    union = len(s1.union(s2))
    return intersection,union,len(s2)
       
def task45_urs(sys,gold):
    """
    Calculating Union Recall Score(URS) of task4 and task5.
    
    Args:
        sys(str):model output of task4 or task5:
        gold(str):expected model output for task4/5:code snippets.
        
    Returns:
        float:URS on the specific sample.
    """
    intersection_len,union_len,gold_len=task45_eval_code_similarity(sys,gold)
    return intersection_len/union_len

def task45_ors(sys,gold):
    """
    Calculating Output-only Recall Score(ORS) of task4 and task5.
    
    Args:
        sys(str):model output of task4 or task5:
        gold(str):expected model output for task4/5:code snippets.
        
    Returns:
        float:ORS on the specific sample.
    """
    intersection_len,union_len,gold_len=task45_eval_code_similarity(sys,gold)
    return intersection_len/gold_len

def task45_avg_score(scores):
    """
    Calculating average ORS or URS on the entire task4/5 benchmark
    
    Args:
        scores(list):a list of ORSs or URSs on each specific sample in task5.
        
    Returns:
        float:average ORS or URS
    """
    return sum(scores)/len(scores)

metrics_mapping={
    'Accuracy':task1_acc,
    'F1-Score':task1_f1,
    'Moderate Evaluation Score':task2_me,
    'Strict Evaluation Score':task2_se,
    'Macro Recall':task3_mar,
    'Micro Recall':task3_mir,
    'Union Line Recall':task45_urs,
    'Line Recall':task45_ors
}
