Rhythm Comp System 音乐游戏竞赛服务系统
===
Made by M0Z@C from MozacLab/XJU2019/XJUSEC
---

![Logo](./static/images/logo.png)

![爱发电](https://afdian.moeci.com/d96a5484caf211ec9d4152540025c377/7H9nRTCjbQyxYWrNatfhcSBed3GKMpvw/badge.svg)

## 赞助者

首先感谢这些来自爱发电的赞助者：

<!-- AFDIAN-ACTION:START -->
<!-- AFDIAN-ACTION:END -->

## I.简介与功能
本系统包含***主页、倒计时、登录、后台、文件上传、文件管理*** 等多个页面，旨在为音乐游戏类竞赛提供基础的竞赛宣传、数据公开服务。

项目基于Python Flask ,需要的软件包已标注在**requirements.txt**中，将在后文的**部署教程**中详细介绍用法。

环境：
```
python ~= 3.7.9
```



## II.部署教程

关于python下载与安装请自行前往博客园、CSDN等站点寻找教程。

首先请安装相关软件包，此处建议通过python的**virtual environment**创建环境，在项目文件夹下打开虚拟环境/全局环境的**bash**中执行以下指令。
```bash
pip install -r requirements.txt
```

等待相关软件包安装完成后，可以通过以下指令启动项目：
```bash
python ./app.py
```

若控制台显示如下内容：
```python
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on https://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
```
则代表启动成功。



## III.配置/配置文件

### 1、倒计时：

重要的事情说三遍

```
请前往/statics/js/timer.js更新比赛时间
请前往/statics/js/timer.js更新比赛时间
请前往/statics/js/timer.js更新比赛时间
```



### 2、关于config.json

如下注释内容：

```json
{
  "main": {
    "name": "",	//比赛名称，字符串
    "database": {	//数据库相关，暂时未实现相关功能，此处可掠过
      "addr": "",
      "port": "",
      "name": "",
      "username": "",
      "passwd": ""
    },
    "comp": ["Phigros","Arcaea","Cytus2"], //比赛类型，支持多项比赛
    "datafile": {
      "path": "./upload/",
      "comps": {
        "Phigros": {
          "filetype": "xls"		//比赛成绩文件类型，目前仅支持xls类型，命名需与比赛名称相同，如“Phigros.xls”
        },
        "Arcaea": {
          "filetype": "xls"
        },
        "Cytus2": {
          "filetype": "xls"
        }
      }
    },
    "secure": {
      "SECRET_KEY": ""		//支持session功能必须，请自行设置，务必填写，禁止中文
    },
    "admins": {
      "username1": "password1",
      "username2": "password2"		//管理后台用户设置
    }
  },
  "addup": {
		//补充内容，等待后续开发
  }
}
```



### 3、https访问相关（必看）

为了方便在公网服务器部署，提供了对应的https访问服务支持，请预先通过域名服务商、第三方证书机构申请可被支持的SSL证书，需包含以下文件：

```
证书名称.crt （证书本体）
证书名称.key (私钥文件)
```

将两个文件放在项目根目录下，并在`app.py`文件下修改最后一行为：

```python
app.run(ssl_context=('./证书名称.crt', './证书名称.key'))
```

即可启用SSL加密访问，使平台支持HTTPS。



### 4、Flask服务运行端口与地址设置

请自行搜索 **“flask app.run()参数”**

后续更新正在路上，欢迎赞助哦：

https://azz.ee/mozaclab

https://afdian.net/a/mozaclab

