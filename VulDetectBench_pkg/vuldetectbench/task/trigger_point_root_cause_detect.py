from vuldetectbench.utils import metrics

class trigger_point_root_cause_eval:
    def __init__(self):
        pass
    
    def eval(self,data):
        """
        Evaluates the model's scores on trigger point code snippet detection.
        
        Args:
            data(list):A list of dictionaries containing the model's predictions and labels.
        
        Returns:
            dict: A dictionary containing evaluation metrics.

        """
        union_recs=[]
        simple_recs=[]
        sys_codes=[]
        for data_item in data:
            urs,sys_code=metrics.task45_urs(data_item['sys'],data_item['gold'])
            ors,sys_code=metrics.task45_urs(data_item['sys'],data_item['gold'])
            union_recs.append(urs)
            simple_recs.append(ors)
            sys_codes.append(sys_code)
        
        avg_union_rec=metrics.task45_avg_score(union_recs)
        avg_simple_rec=metrics.task45_avg_score(simple_recs)        
        results={
            'verbose output':sys_codes,
            'verbose_urs':union_recs,
            'verbose_ors':simple_recs,
            'average union recall':avg_union_rec,
            'average simple recall':avg_simple_rec     
        }
        return results