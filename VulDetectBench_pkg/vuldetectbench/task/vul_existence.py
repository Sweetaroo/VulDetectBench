from vuldetectbench.utils import metrics

class ExistenceEval:
    def __init__(self):
        pass
    
    def eval(self,data):
        """
        Evaluates the model's accuracy on vulnerability existence detection.
        
        Args:
            data(list):A list of dictionaries containing the model's predictions and labels.
        
        Returns:
            dict: A dictionary containing evaluation metrics.

        """
        hit_record=[]
        for data_item in data:
            metric=metrics.task1_hit(data_item['sys'],data_item['gold'])
            hit_record.append(list(metric))
        results_acc=metrics.task1_acc(hit_record)
        results_f1=metrics.task1_f1(hit_record)
        results={
            'verbose output':hit_record,
            'accuracy':results_acc,
            'f1':results_f1            
        }
        return results