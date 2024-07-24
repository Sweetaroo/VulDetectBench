from setuptools import setup, find_packages

setup(
    name='vuldetectbench',
    version='0.0.4',
    description='VulDetectBench',  
    author='Lang Gao',
    author_email='vuldetectbench@gmail.com',
    url='https://github.com/Sweetaroo/VulDetectBench',  
    packages=find_packages(), 
    include_package_data=True, 
    install_requires=[
        'transformers',
        'huggingface_hub',
        'datasets',
        'openai>=1.0.0',
        'tqdm',
        'nltk',
        'numpy',
        'pandas',
        'scipy',
        'python-liquid',
        'requests'       
],
    classifiers=[
    ],
)
