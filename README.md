# 简介

动态DNS更新脚本，目前支持DnsPod和CloudFlare

* [DNSPod API](https://www.dnspod.cn/docs/records.html#dns)
* [CloudFlare API](https://api.cloudflare.com/)

# 功能模块

* 获取本机的公网地址
* 更新DNS记录
* 依靠systemd的timer运行，如公网地址没变则不发起更新请求

# 配置介绍

通过环境变量配置脚本:

* `PROVIDER`: DNS服务商，目前支持`dnspod`和`cloudflare`
* `TOKEN_ID`: ID，对于DNSPod来说是token_id，对于CloudFlare说是用户邮箱
* `TOKEN_KEY`: 验证密钥，对于DNSPod来说是token, 对于CloudFlare来说是api_key
* `DOMAIN`: 域名，比如xdays.me
* `RECORD`: 记录，比如www.xdays.me
* `IP_TYPE`: 使用公网地址还是私网地址, 对应为`public`和`private`

# 安装

```
git clone git@github.com:xdays/ddns.git /opt/ddns
```

准备配置文件 `/opt/ddns/.env`

```
PROVIDER=cloudflare
TOKEN_ID=token_id
TOKEN_KEY=token_key
DOMAIN=example.com
RECORD=v.example.com
IP_TYPE=public
```

集成systemd

```
./install.sh
systemctl start ddns.timer
```
