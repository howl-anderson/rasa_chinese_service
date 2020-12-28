# rasa_chinese_service

服务于 [rasa_chinese](https://github.com/howl-anderson/rasa_chinese) 的 Service 包，通过 RPC 的方式提供 rasa_chinese 所需的服务。

## 安装

```shell
pip install rasa_chinese_service
```

## 使用
### lm_tokenizer
```shell
python -m rasa_chinese_service.nlu.tokenizers.lm_tokenizer bert-base-chinese
```