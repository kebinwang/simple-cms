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

在项目根目录创建下面文件并运行：

```
from simplecms import database
from simplecms.models.user import User
from simplecms.models.post import Post
from simplecms.models.magazine import Magazine, MagazinePost


def create_tables():
    database.connect()
    database.create_tables([User, Post, Magazine, MagazinePost])

if __name__ == '__main__':
    create_tables()
    User.create(
        username='xcf',
        password='xcf')

```

会在项目根目录创建 `simplecms-dev.db` sqlite 数据库文件。

### 3. 运行

```
python run.py
```

Postman 测试信息：https://www.getpostman.com/collections/b80b730b03fee0389f8d

## Dependencies

## Run

## API

