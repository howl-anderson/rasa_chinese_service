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

### WeChat Service
启动 WeChat Service 分为两步: 第一步启动 WeChat Web Puppet, 第二步(在新的终端中)启动 WeChat Adapter.
#### 启动 WeChat web puppet
```shell
docker pull wechaty/wechaty:latest

export WECHATY_LOG="verbose"
export WECHATY_PUPPET="wechaty-puppet-wechat"
export WECHATY_PUPPET_SERVER_PORT="8080"
export WECHATY_TOKEN="python-wechaty-uos-token"

docker run -ti \
--name wechaty_puppet_service_token_gateway \
--rm \
-e WECHATY_LOG \
-e WECHATY_PUPPET \
-e WECHATY_PUPPET_SERVER_PORT \
-e WECHATY_TOKEN \
-p "$WECHATY_PUPPET_SERVER_PORT:$WECHATY_PUPPET_SERVER_PORT" \
wechaty/wechaty:latest
```
#### 启动 WeChat Adapter
```shell
WECHATY_PUPPET_SERVICE_TOKEN=python-wechaty-uos-token WECHATY_PUPPET_SERVICE_ENDPOINT=127.0.0.1:8080 python -m rasa_chinese_service.core.channels.wechat
```
上面的命令默认Rasa服务地址是 http://localhost:5005 (这是Rasa默认的服务地址).如果你的Rasa服务地址不是这个(比如启动在别的机器上或者使用了不同的端口),那么请你在命令行前添加环境变量`RASA_SERVER`来指明,比如下面这个命令:
```shell
RASA_SERVER=http://192.168.1.2:5050 WECHATY_PUPPET_SERVICE_TOKEN=python-wechaty-uos-token WECHATY_PUPPET_SERVICE_ENDPOINT=127.0.0.1:8080 python -m rasa_chinese_service.core.channels.wechat
```

如果你是第一次访问 WeChat Web Puppet, 那么可能需要按照 WeChat Adapter 的提示,用将要作为机器人的微信(存在被官方封杀的风向)来扫描二维码登录.