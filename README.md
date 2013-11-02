#简介
基于[DNSPod API](https://www.dnspod.cn/docs/records.html#dns)的动态DNS更新脚本

#功能模块
* 获取本机的公网地址
* 更新DNS记录
* crontab运行，如公网地址没变则不发起更新请求

#配置介绍
* `login_email`: 登陆邮箱
* `login_password`: 登陆密码
* `format`: 响应数据格式，如json
* `domain_id`: 域名ID，可通过`curl -k https://dnsapi.cn/Domain.List -d "login_email=xxx&login_password=xxx"`获取
* `record_id`: 记录ID，可通过`curl -k https://dnsapi.cn/Record.List -d "login_email=xxx&login_password=xxx&domain_id=xxx"`获取
* `sub_domain`: 子域名记录明，如www
* `record_line`: 线路名称，如默认

#感谢
感谢此[gist](https://gist.github.com/chuangbo/833369)作者
