from vuldetectbench.utils import metrics

class obj_func_eval:
    def __init__(self):
        pass
    
    def eval(self,data):
        """
        Evaluates the model's scores on key objections and functions detection.
        
        Args:
            data(list):A list of dictionaries containing the model's predictions and labels.
        
        Returns:
            dict: A dictionary containing evaluation metrics.

        """
        hit_tokens=[]
        hit_lens=[]
        gold_lens=[]
        recalls=[]
        for data_item in data:
            hit_token,recall,hit_len,gold_len=metrics.task3_single_metric(data_item['sys'],data_item['gold'])
            hit_tokens.append(hit_token)
            recalls.append(recall)
            hit_lens.append(hit_len)
            gold_lens.append(gold_len)
        
        macro_avg_recall=metrics.task3_mar(recalls)
        micro_avg_recall=metrics.task3_mir(hit_lens,gold_lens)
        results={
            'verbose_output':hit_tokens,
            'macro avg recall':macro_avg_recall,
            'micro avg recall':micro_avg_recall     
        }
        return results