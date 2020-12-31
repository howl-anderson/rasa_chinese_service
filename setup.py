from setuptools import setup, find_packages

setup(
    name='rasa_chinese_service',
    version='2.2.0',
    packages=find_packages(),
    url='https://github.com/howl-anderson/rasa_chinese_service',
    license='Apache 2.0',
    author='Xiaoquan Kong',
    author_email='u1mail2me@gmail.com',
    description='Service package for rasa_chinese',
    install_requires=["transformers>3.0,<4.0", "sanic"],
    tests_requires=["pytest"]
)
