FROM python:3.7-slim

RUN pip install pipenv

ADD . /opt/rasa-chinese-service

RUN mkdir -p /tmp/cache

EXPOSE 8000
VOLUME [ "/tmp/cache" ]

WORKDIR /opt/rasa-chinese-service

RUN pipenv install --system

ENTRYPOINT ["python", "-m", "rasa_chinese_service.nlu.tokenizers.lm_tokenizer", "--cache_dir=/tmp/cache"]
