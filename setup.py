from __future__ import print_function
from setuptools import setup, find_packages

packages = find_packages(include = 'fastml_engine.**', exclude=['fastml_engine.egg-info'])
packages.append('fastml_engine.docs')
print(packages)



setup(
    name='fastml_engine',
    version='1.0.3',
    author="HaiTao Hou",
    author_email="hou610433155@163.com",
    description='A web server for deploy ml/dl model',
    long_description=open("README.rst",encoding='utf-8').read(),
    long_description_content_type="text/x-rst",
    license='MIT',
    packages=packages,
    package_data={'fastml_engine.docs': ['*.yaml'], },
    install_requires=[
        'Flask',
        'flasgger',
        'numpy',
        'six',
        'gevent',
        'Werkzeug',
        'concurrent_log_handler==0.9.16',
        'portalocker==1.7.0',
        "click>=7.0"
        "gunicorn; platform_system != 'Windows'",
        "waitress; platform_system == 'Windows'",
    ],
    python_requires='>=3.6',
    entry_points="""
            [console_scripts]
            fastml=fastml_engine.cli:cli
        """,
    keyword="ml ai model inference",
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ]
    # project_urls={
    #     "Bug Tracker": "https://github.com/mlflow/mlflow/issues",
    #     "Documentation": "https://mlflow.org/docs/latest/index.html",
    #     "Source Code": "https://github.com/mlflow/mlflow",
    # },
)
