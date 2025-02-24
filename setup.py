from setuptools import setup, find_packages

setup(
    name="mathlearn",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'transformers>=4.36.0',
        'torch>=2.0.0',
        'datasets>=2.14.0',
        'accelerate>=0.24.0',
        'bitsandbytes>=0.41.0',
        'peft>=0.5.0'
    ]
) 