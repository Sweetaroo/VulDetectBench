# VulDetectBench
A Novel Benchmark evaluating the Deep Capability of Vulnerability Detection with Large Language Models

# Abstract
Large Language Models (LLMs) have training corpora containing large amounts of program code, greatly improving the model's code comprehension and generation capabilities. However, sound comprehensive research on detecting program vulnerabilities, a more specific task related to code, and evaluating the performance of LLMs in this more specialized scenario is still lacking. To address common challenges in vulnerability analysis, our study introduces a new benchmark, VulDetectBench, specifically designed to assess the vulnerability detection capabilities of LLMs. The benchmark comprehensively evaluates LLM's ability to identify, classify, and locate vulnerabilities through five tasks of increasing difficulty. We evaluate the performance of 17 models (both open- and closed-source) and find that while existing models can achieve over 80\% accuracy on tasks related to vulnerability identification and classification, they still fall short on specific, more detailed vulnerability analysis tasks, with less than 30\% accuracy, making it difficult to provide valuable auxiliary information for professional vulnerability mining. Our benchmark effectively evaluates the capabilities of various LLMs at different levels in the specific task of vulnerability detection, providing a foundation for future research and improvements in this critical area of code security. 

# Overview of VulDetectBench
<img width="1135" alt="image" src="https://github.com/Sweetaroo/VulDetectBench/assets/14751376/95d7d720-cfde-43ea-8110-76ae80dd5ac5">

# Results
Top 8 LLMs' ability on Vulnerability Detections. Our benchmark consisting of five vulnerability analysis related tasks of increasing difficulty. The figure shows that existing LLMs perform well on simple analysis tasks such as vulnerability existence detection and CWE type inference, while on specific vulnerability related tasks, although performance varies from LLM to LLM, the overall performance is not yet satisfactory.
<img width="930" alt="image" src="https://github.com/Sweetaroo/VulDetectBench/assets/14751376/374e9ec8-b466-43a9-963f-9365d30fd6e4">



