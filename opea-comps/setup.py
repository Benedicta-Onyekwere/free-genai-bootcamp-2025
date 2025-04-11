from setuptools import setup, find_packages

setup(
    name='opea-comps',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'fastapi>=0.109.2',
        'uvicorn>=0.27.1'
    ],
) 