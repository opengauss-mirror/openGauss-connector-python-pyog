### 关于

该驱动是基于 [py-postgresql](https://github.com/python-postgres/fe) 1.3.0 版本进行修改的，新增了两个特性：
- 支持 [openGauss](https://opengauss.org/) 数据库连接
- 支持多 IP 连接


### 安装方式

通过 pypi.org:

    $ pip install py-opengauss
    
通过源码安装：

    $ git clone https://gitee.com/opengauss/openGauss-connector-python-pyog.git
    $ cd py-opengauss
    $ python3 setup.py install

### 连接方式：

> 支持的连接协议列表: ['pq', 'postgres', 'postgresql', 'og', 'opengauss']

```python
>>> import py_opengauss
# General Format:
>>> db = py_opengauss.open('pq://user:password@host:port/database')

# Also support opengauss scheme:
>>> db = py_opengauss.open('opengauss://user:password@host:port/database')

# multi IP support, will return PRIMARY instance connect:
>>> db = py_opengauss.open('opengauss://user:password@host1:123,host2:456/database')

# Connect to 'postgres' at localhost with default user and password in the env, which only support postgresql.
# 注意: 该连接方式只支持PG, 不支持openGauss, 对于openGauss, 必须要输入user和password
>>> db = py_opengauss.open('localhost/postgres')
```

### 基本用法

```python
import py_opengauss
db = py_opengauss.open('opengauss://user:password@host:port/database')

get_table = db.prepare("SELECT * from information_schema.tables WHERE table_name = $1")
print(get_table("tables"))

# Streaming, in a transaction.
with db.xact():
    for x in get_table.rows("tables"):
        print(x)
```

### sqlalchemy 多IP连接用法

*注：sqlalchemy 目前本身是不支持 py_opengauss 包的*

由于 sqlalchemy 在内部会解析连接串，且目前仅支持单个IP的连接串。
所以需下载定制后的 [sqlalchemy](https://github.com/vimiix/sqlalchemy) 手动安装使用

https://github.com/vimiix/sqlalchemy

该定制版本在内部增加了对于 py_opengauss 包的支持，且支持了多IP连接串。

##### 使用方式

```python
from sqlalchemy import create_engine
# 初始化opengauss数据库多主机连接（适用于没有固定虚拟IP的数据库主备集群）:
engine = create_engine('postgresql+pyopengauss://user:password@host1:port1,host2:port2/db')
```

### Documentation

http://py-postgresql.readthedocs.io

### Related

- http://postgresql.org
- http://python.org
