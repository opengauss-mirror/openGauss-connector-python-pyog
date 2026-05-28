### About

This driver is modified based on [py-postgresql](https://github.com/python-postgres/fe) 1.3.0 and has the following new features:
- Connection to the openGauss ](https://opengauss.org/) database
- Connection of multiple IP addresses


### Installation

Installation through `pypi.org`

    $ pip install py-opengauss
    
Installation using source code

    $ git clone https://gitee.com/opengauss/openGauss-connector-python-pyog.git
    $ cd py-opengauss
    $ python3 setup.py install

### Connection

> Supported protocols: ['pq', 'postgres', 'postgresql', 'og', 'opengauss']

```python
>>> import py_opengauss
# General Format:
>>> db = py_opengauss.open('pq://user:password@host:port/database')

# Also support opengauss scheme:
>>> db = py_opengauss.open('opengauss://user:password@host:port/database')

# multi IP support, will return PRIMARY instance connect:
>>> db = py_opengauss.open('opengauss://user:password@host1:123,host2:456/database')

# Connect to 'postgres' at localhost with default user and password in the env, which only support postgresql.
# Note: This connection mode works only with PostgreSQL, not openGauss. For openGauss, provide the username and password.
>>> db = py_opengauss.open('localhost/postgres')
```

### Basic Usage

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

### SQLAlchemy multi-IP connection

*Note: Currently, SQLAlchemy does not support the `py_opengauss` package.*

SQLAlchemy parses connection strings and only supports those with a single IP address.
Therefore, download the custom [SQLAlchemy](https://github.com/vimiix/sqlalchemy) and manually install it.

https://github.com/vimiix/sqlalchemy

This custom version supports `py_opengauss` and multi-IP connection strings.

##### Usage

```python
from sqlalchemy import create_engine
# Initialize the multi-host connection for the openGauss database (applicable to primary/standby database clusters without fixed virtual IP addresses):
engine = create_engine('postgresql+pyopengauss://user:password@host1:port1,host2:port2/db')
```

### Documentation

http://py-postgresql.readthedocs.io

### Related

- http://postgresql.org
- http://python.org
