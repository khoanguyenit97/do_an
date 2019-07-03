# Prerequisite
Django=2.0.4
python>=3.6.5
## Sympy
```
pip install mpmath
git clone git://github.com/quangpq/sympy
git pull origin master
python setup.py install
```
## Unidecode
```
pip install Unidecode
```
## Graphviz
Run all these commands:

```
pip install graphviz
```
# Source
If Pycharm warning about absolute import (ex: from parse import parse_expr). Do:

1. Open File -> Settings -> Project: -> Project Structure

2. Then mark these folder as a Source directory:

	* inference_module
	* inference_module/logic
	* inference_module/relation

# Error
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module. Did you install mysqlclient?

pip install pymysql
Then, edit the __init__.py file in your project origin dir(the same as settings.py)

add:

import pymysql

pymysql.install_as_MySQLdb()