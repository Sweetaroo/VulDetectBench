from vuldetectbench.utils import metrics

class type_cls_eval:
    def __init__(self):
        pass
    
    def eval(self,data):
        """
        Evaluates the model's scores on vulnerability type classification.
        
        Args:
            data(list):A list of dictionaries containing the model's predictions and labels.
        
        Returns:
            dict: A dictionary containing evaluation metrics.

        """
        scs=[]
        mcs=[]
        answers=[]
        for data_item in data:
            strict_score,strict_answer=metrics.task2_se(data_item['sys'],data_item['gold'])
            moderate_score,moderate_answer=metrics.task2_me(data_item['sys'],data_item['gold'])
            scs.append(strict_score)
            mcs.append(moderate_score)
            answers.append([strict_answer,moderate_answer])
        avg_strict_score=metrics.task2_avg_score(scs)
        avg_moderate_score=metrics.task2_avg_score(mcs)
        results={
            'verbose output':answers,
            'strict score':avg_moderate_score,
            'moderate score':avg_moderate_score     
        }
        return results