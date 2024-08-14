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
        },
        "cot":"Let's think step by step.First,describe the overall purpose of the program.Then,List the inputs, functions, and variables related to the task and highlight any sensitive operations, such as memory allocation, copying, or assignment.Next,based on your prior knowledge,select the variables and functions that is related to the most risky operations.Please only use \" to wrap code during analysis.only Output your final data objects and functions in the format: `{code}` if your answer contains any.",
        "fewshot":"""output data objects and functions in the format: `{code}` if your answer contains any.## example1:
        code:
        void host_lookup(char *user_supplied_addr){
struct hostent *hp;
in_addr_t *addr;
char hostname[64];
in_addr_t inet_addr(const char *cp);

/*routine that ensures user_supplied_addr is in the right format for conversion */

validate_addr_form(user_supplied_addr);
addr = inet_addr(user_supplied_addr);
hp = gethostbyaddr( addr, sizeof(struct in_addr), AF_INET);
strcpy(hostname, hp->h_name);
}
answer:`hp` `gethostbyaddr` `strcpy`
## example2:
code:
char * copy_input(char user_supplied_string){
int i, dst_index;
char dst_buf = (char)malloc(4sizeof(char) * MAX_SIZE);
if ( MAX_SIZE <= strlen(user_supplied_string) ){
die("user string too long, die evil hacker!");
}
dst_index = 0;
for ( i = 0; i < strlen(user_supplied_string); i++ ){
if( '&' == user_supplied_string[i] ){
dst_buf[dst_index++] = '&';
dst_buf[dst_index++] = 'a';
dst_buf[dst_index++] = 'm';
dst_buf[dst_index++] = 'p';
dst_buf[dst_index++] = ';';
}
else if ('<' == user_supplied_string[i] ){
/* encode to < */
}
else dst_buf[dst_index++] = user_supplied_string[i];
}
return dst_buf;
}
answer:`malloc` `dst_buf` `malloc`
## Test
code:\n
"""
            
    },
    "Task4":{
        "Name":"Root Cause Location",
        "system":"Assuming you are an experienced code vulnerability analyst who can only output code snippets and the following code may have vulnerabilities.",
        "question":"Which line of code is the root cause point of the vulnerability?",
        "restriction":"output your answer code in the format: `{code}`.",
        "metrics":{
            "single":['Union Line Recall','Line Recall'],
            "overall":['Avg Union Line Recall','Avg Line Recall']
        },
        "cot":"Let's think step by step.First,describe the overall purpose of the program.Then,List the inputs, functions, and variables related to the task and highlight any sensitive operations, such as memory allocation, copying, or assignment.Next,based on your prior knowledge,analyze these operation for Root Causes:whether this operation brings a latent vulnerability(such as initialization,read/write,...).Please only use \" to wrap code during analysis.Only output your final answer code in the format: `{code}`.",
        "fewshot":"""output your final answer code in the format: `{code}`.## example1:
        code:
        void host_lookup(char *user_supplied_addr){
struct hostent *hp;
in_addr_t *addr;
char hostname[64];
in_addr_t inet_addr(const char *cp);

/*routine that ensures user_supplied_addr is in the right format for conversion */

validate_addr_form(user_supplied_addr);
addr = inet_addr(user_supplied_addr);
hp = gethostbyaddr( addr, sizeof(struct in_addr), AF_INET);
strcpy(hostname, hp->h_name);
}
answer:`hp = gethostbyaddr( addr, sizeof(struct in_addr), AF_INET);`
## example2:
code:
char * copy_input(char user_supplied_string){
int i, dst_index;
char dst_buf = (char)malloc(4sizeof(char) * MAX_SIZE);
if ( MAX_SIZE <= strlen(user_supplied_string) ){
die("user string too long, die evil hacker!");
}
dst_index = 0;
for ( i = 0; i < strlen(user_supplied_string); i++ ){
if( '&' == user_supplied_string[i] ){
dst_buf[dst_index++] = '&';
dst_buf[dst_index++] = 'a';
dst_buf[dst_index++] = 'm';
dst_buf[dst_index++] = 'p';
dst_buf[dst_index++] = ';';
}
else if ('<' == user_supplied_string[i] ){
/* encode to < */
}
else dst_buf[dst_index++] = user_supplied_string[i];
}e

return dst_buf;
}
answer:`char *dst_buf = (char*)malloc(4*sizeof(char) * MAX_SIZE);`
## Test
code:\n
"""
            
    },
    "Task5":{
        "Name":"Trigger Point Location",
        "system":"Assuming you are an experienced code vulnerability analyst who can only output code snippets and the following code may have vulnerabilities.",
        "question":"Which line of code is the trigger point of the vulnerability?",
        "restriction":"output your answer code in the format: `{code}`.",
        "metrics":{
            "single":['Union Line Recall','Line Recall'],
            "overall":['Avg Union Line Recall','Avg Line Recall']
        },
        "cot":"Let's think step by step.First,describe the overall purpose of the program.Then,List the inputs, functions, and variables related to the task and highlight any sensitive operations, such as memory allocation, copying, or assignment.Next,based on your prior knowledge,analyze for Root Causes:whether these operations raises a vulnerability.Finally,analyze other operations for Trigger Points:whether the code utilizes the latent vulnerability in the likely Root Cause.Please only use \" to wrap code during analysis.Only output your final answer code in the format: `{code}`.",
        "fewshot":"""output your final answer code in the format: `{code}`.## example1:
        code:
        void host_lookup(char *user_supplied_addr){
struct hostent *hp;
in_addr_t *addr;
char hostname[64];
in_addr_t inet_addr(const char *cp);

/*routine that ensures user_supplied_addr is in the right format for conversion */

validate_addr_form(user_supplied_addr);
addr = inet_addr(user_supplied_addr);
hp = gethostbyaddr( addr, sizeof(struct in_addr), AF_INET);
strcpy(hostname, hp->h_name);
}
answer:`strcpy(hostname, hp->h_name);`
## example2:
code:
char * copy_input(char user_supplied_string){
int i, dst_index;
char dst_buf = (char)malloc(4sizeof(char) * MAX_SIZE);
if ( MAX_SIZE <= strlen(user_supplied_string) ){
die("user string too long, die evil hacker!");
}
dst_index = 0;
for ( i = 0; i < strlen(user_supplied_string); i++ ){
if( '&' == user_supplied_string[i] ){
dst_buf[dst_index++] = '&';
dst_buf[dst_index++] = 'a';
dst_buf[dst_index++] = 'm';
dst_buf[dst_index++] = 'p';
dst_buf[dst_index++] = ';';
}
else if ('<' == user_supplied_string[i] ){
/* encode to < */
}
else dst_buf[dst_index++] = user_supplied_string[i];
}e

return dst_buf;
}
answer:`if( '&' == user_supplied_string[i] )`
## Test
code:\n
"""
    }
}

def format_dataset(task_name,raw_dataset,method=None):
    general_prompt=Template("{{ question }}\n{{example_with_restriction}}\n{{ code }}\n{{ restriction }}\n{{cot_with_restriction}}")
    dataset=[]
    
    template=task_templates[task_name]
    for raw_sample in raw_dataset:
        if task_name=='Task2':
            user_prompt=general_prompt.render(question=template['question'],
                                              code=raw_sample['selection']+raw_sample['code'],restriction=template['restriction'],
                                              cot_with_restriction='',
                                              example_with_restriction='')   
        elif task_name in ['Task3','Task4','Task5'] and method=='cot':
            
            user_prompt=general_prompt.render(question=template['question'],
                                              code=raw_sample['code'],
                                              restriction='',
                                              cot_with_restriction=template['cot'],
                                              example_with_restriction='')
        elif task_name in ['Task3','Task4','Task5'] and method=='few-shot':
            
            user_prompt=general_prompt.render(question=template['question'],
                                              code=raw_sample['code'],
                                              example_with_restriction=template['fewshot'],
                                              cot_with_restriction='',
                                              restriction='answer:')
        else:
            
            user_prompt=general_prompt.render(question=template['question'],
                                              code=raw_sample['code'],
                                              example_with_restriction='',
                                              cot_with_restriction='',
                                              restriction=template['restriction'])
               
        
        dataset.append({
            'id':raw_sample['idx'],
            'system':template['system'],
            'user':user_prompt,
            'answer':raw_sample['answer']
        })# TODO
    return dataset