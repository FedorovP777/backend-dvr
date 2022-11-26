import ast
import asyncio
import inspect
import os
import re
from _ast import Subscript, Load, Name, Constant, List, ImportFrom, alias
from re import sub
from typing import TypeVar

import autopep8
from jinja2 import Template
from test import middleware


class AstAddToDict(ast.NodeTransformer):
    def __init__(self, name: str, key: str, value: str):
        self.replace_variable = name
        self.add_value = value
        self.add_key = key

    def visit_Assign(self, node):
        if node.targets[0].id == self.replace_variable:
            print(node.value)
            print(dir(node.value))
            node.value.values.append(Name(id=self.add_value, ctx=Load()))
            node.value.keys.append(Constant(value=self.add_key))
        return node


def add_to_config():
    code = '''
    from collections.abc import Mapping
    from collections.abc import Mapping
    middleware = a1
    '''
    x = 1
    my_tree = ast.parse(code)
    print(ast.dump(my_tree, indent=4))
    # print(inspect.getsource(ast.unparse))
    # print(ast.unparse(my_tree))
    binopv = AstAddToDict().visit(my_tree)
    print(binopv.body.append(ImportFrom(module='middleware', names=[alias(name='a1')])))
    print(ast.unparse(binopv))
    a = ast.unparse(binopv)
    print(dir(a))
    import autopep8

    a = autopep8.fix_code(a, options={'max_line_length': 80, 'aggressive': True})
    f = open("test.py", "w")
    f.write(a)
    f.close()


def camel_case(s: str) -> str:
    """Convert uppercase to underscore. E.g.: GoodExample -> good_example.

    Args:
        s: str

    Returns:
        str
    """
    return re.sub('(?<!^)(?=[A-Z])', '_', s).lower()


def generate_middleware(classname: str) -> None:
    """Create new middleware from template and add it to config.

    Args:
        classname: str
    """
    with open('../web_framework/http/middleware/middleware_template.j2') as f:
        template = f.read()
    camel_case_classname = camel_case(classname)
    file_path = f"main/middleware/{camel_case_classname}.py"

    if os.path.exists(file_path):
        raise Exception("File already exist.")

    with open(file_path, "a") as f:
        f.write(Template(template).render({'classname': classname}))

    app_config_path = 'main/middleware/config.py'

    with open(app_config_path, 'r') as f:
        app_config_body = f.read()

    ast_parsed = ast.parse(app_config_body)
    ast_parsed.body.append(ImportFrom(module=f'app.main.middleware.{camel_case_classname}', names=[alias(name=classname)]))
    code = ast.unparse(AstAddToDict('middleware', camel_case_classname, classname).visit(ast_parsed))
    code = autopep8.fix_code(code, options={'max_line_length': 80, 'aggressive': 4, 'hang_closing': True, 'experimental': True})

    with open(app_config_path, "w") as f:
        f.write(code)
