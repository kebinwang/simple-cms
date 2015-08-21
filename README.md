# simple-cms

## 开发部分初始化

使用 python3。

### 1. 建立虚拟环境、启动虚拟环境、安装依赖：

```
$ pyvenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
...
```

### 2. 初试化数据库

```
(venv) $ python
>>> from simplecms.app import *
>>> create_tables()
```

会在项目根目录创建 `simplecms-dev.db` sqlite 数据库文件，手动去里面添加一个用户。

### 3. 运行

```
python run.py
```

Postman 测试信息：https://www.getpostman.com/collections/b80b730b03fee0389f8d

## Dependencies

## Run

## API

