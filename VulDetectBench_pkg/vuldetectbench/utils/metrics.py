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
    sys_code=''
    if 'yes' in sys.lower() or 'is vulnerable' in sys.lower():
        sys_token=1
        sys_code='YES'
    else:
        sys_token=0
        sys_code='NO'

    if 'yes' in gold.lower() or 'is vulnerable' in gold.lower():
        gold_token=1
        
    else:
        gold_token=0
    
    tp=fp=tn=fn=0
    if sys_token==1 and gold_token==1:
        tp=1
    elif sys_token==1 and gold_token==0:
        fp=1
    elif sys_token==0 and gold_token==1:
        fn=1
    else:
        tn=1
    return (tp,fp,tn,fn),sys_code
    
def task1_acc(scores):
    """
    Calculating the overall accuracy in task1:vulnerability existence detection.
    
    Args:
        scores(list of integer lists):containing model prediction situation in each sample,in the form of [[tps],[fps],[tns],[fns]]
        
    Returns:
        float:overall accuracy on task1.
    """
    tps=[item[0] for item in scores]
    fps=[item[1] for item in scores]
    tns=[item[2] for item in scores]
    fns=[item[3] for item in scores]
    #[[tps],[fps],[tns],[fns]]
    TP=sum(tps)
    FP=sum(fps)
    TN=sum(tns)
    FN=sum(fns)
    acc=(TP+TN)/(TP+FP+TN+FN)
    return acc

def task1_f1(scores):
    """
    Calculating the overall f1-score in task1:vulnerability existence detection.
    
    Args:
        scores(list of integer lists):containing model prediction situation in each sample,in the form of [[tps],[fps],[tns],[fns]]
        
    Returns:
        float:overall f1-score on task1.
    """
    
    tps=[item[0] for item in scores]
    fps=[item[1] for item in scores]
    tns=[item[2] for item in scores]
    fns=[item[3] for item in scores]
    #[[tps],[fps],[tns],[fns]]
    TP=sum(tps)
    FP=sum(fps)
    TN=sum(tns)
    FN=sum(fns)
    
    try:
        p=TP/(TP+FN)
        r=TP/(TP+FP)
        f1=2*(p*r)/(p+r)
    except ZeroDivisionError:
        f1=0

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
    sys_code=''
    gold = gold.split('|')
    answers = [gold[0][0], gold[1][0]]
    score_a = 0
    if (answers[1] + '.') in sys:
        score_a += 0.5
        sys_code=answers[1]
    if (answers[0] + '.') in sys:
        score_a += 1
        sys_code=answers[0]
    if score_a==1.5:
        score_a=0
        sys_code=''
    score_b = 0
    if task2_hit(sys, gold[0]) > 0:
        score_b += 1
        sys_code=answers[0]
    if task2_hit(sys, gold[1]) > 0:
        score_b += 0.5
        sys_code=answers[1]
    if score_b==1.5:
        score_b=0
        sys_code=''
    return max(score_a, score_b),sys_code

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
    sys_code=''
    if (answers[0] + '.') in sys :
        score_a = 1
        sys_code=answers[0]
    elif (answers[1] + '.') in sys:
        score_a=1
        sys_code=answers[1]
    score_b = 0
    if task2_hit(sys, gold[0]) > 0:
        score_b = 1
        sys_code=answers[0]
    elif task2_hit(sys, gold[1]) > 0:
        score_b=1
        sys_code=answers[1]
            
    return max(score_a, score_b),sys_code

def task2_avg_se(scores):
    """
    Calculating average ME or SE on the entire task2 benchmark.
        
    Args:
        scores(list of floats):A list of scores model gets on each sample of task2.
        
    Returns:
        float:the average score on task2.
    """
    return sum(scores)/len(scores)

def task2_avg_me(scores):
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
    sys_code=' '.join(hit_tokens)
    recall=len(hit_tokens)/len(gold_tokens)
    return (recall,len(hit_tokens),len(gold_tokens)),sys_code


def task3_mar(scores):
    """
    Calculating Macro average Recall(MAR) on the entire task3.
    
    Args:
        scores(list of tuples):(recall,len(hit_tokens),len(gold_tokens))
        
    Returns:
        float:overall MAR of task3.
    """
    recalls=[item[0] for item in scores]
    return sum(recalls)/len(recalls)

def task3_mir(scores):
    """
    Calculating Micro average Recall(MIR) on the entire task3.
    
    Args:
        hit_lens(list of integers):quantity of "hit" tokens on each sample of task3.
        gold_lens(list of integers):quantity of answer tokens on each sample of task3.
        
    Returns:
        float:overall MIR of task3.
    """
    hit_lens=[item[1] for item in scores]
    gold_lens=[item[2] for item in scores]
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
    pattern = re.compile(r"`{3}(.+?)`{3}|`(.+?)`", re.S)
    sys_code=code1 = pattern.findall(sys)
    sys_code=code1=list(filter(lambda x: x, map(lambda match: match[0] if match[0] else match[1], code1)))
    sys_code='\n'.join(sys_code)
    print(sys_code)
    gold_code=code2 = pattern.findall(gold)
    gold_code=code2=list(filter(lambda x: x, map(lambda match: match[0] if match[0] else match[1], code1)))
    gold_code='\n'.join(gold_code)
    if len(code1) == 0 or len(code2) == 0:
        return 0
    code1 = code1[0].split('\n')
    if len(code1) == 0:
        return set(),set(),0
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
    return intersection,union,len(s2),sys_code
       
def task45_urs(sys,gold):
    """
    Calculating Union Recall Score(URS) of task4 and task5.
    
    Args:
        sys(str):model output of task4 or task5:
        gold(str):expected model output for task4/5:code snippets.
        
    Returns:
        float:URS on the specific sample.
    """
    intersection_len,union_len,gold_len,sys_code=task45_eval_code_similarity(sys,gold)
    return intersection_len/union_len,sys_code

def task45_ors(sys,gold):
    """
    Calculating Output-only Recall Score(ORS) of task4 and task5.
    
    Args:
        sys(str):model output of task4 or task5:
        gold(str):expected model output for task4/5:code snippets.
        
    Returns:
        float:ORS on the specific sample.
    """
    intersection_len,union_len,gold_len,sys_code=task45_eval_code_similarity(sys,gold)
    return intersection_len/gold_len,sys_code

def task45_avg_urs(scores):
    """
    Calculating average ORS or URS on the entire task4/5 benchmark
    
    Args:
        scores(list):a list of ORSs or URSs on each specific sample in task5.
        
    Returns:
        float:average ORS or URS
    """
    return sum(scores)/len(scores)

def task45_avg_ors(scores):
    """
    Calculating average ORS or URS on the entire task4/5 benchmark
    
    Args:
        scores(list):a list of ORSs or URSs on each specific sample in task5.
        
    Returns:
        float:average ORS or URS
    """
    return sum(scores)/len(scores)

MetricsMapping={
    'hit':task1_hit,
    'Accuracy':task1_acc,
    'F1-Score':task1_f1,
    'Moderate Evaluation Score':task2_me,
    'Strict Evaluation Score':task2_se,
    'Avg Moderate Evaluation Score':task2_avg_me,
    'Avg Strict Evaluation Score':task2_avg_se,
    'Token Recall':task3_single_metric,
    'Macro Token Recall':task3_mar,
    'Micro Token Recall':task3_mir,
    'Union Line Recall':task45_urs,
    'Line Recall':task45_ors,
    'Avg Union Line Recall':task45_avg_urs,
    'Avg Line Recall':task45_avg_ors
}
