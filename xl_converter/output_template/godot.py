# -*- coding: utf-8 -*-
# godot配置輸出

from gamefang.Gfile import gFile

def __to_godot(value) -> str:
    '''
    遞歸清洗Python值為Godot類型
    '''
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if value is None:
        return 'null'
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        escaped = value.replace('\\', '\\\\').replace("'", "\\'")
        return f"'{escaped}'"
    if isinstance(value, (list, tuple)):
        if list(value) == [None]:   # [None]視為空list
            return '[]'
        items = ', '.join(__to_godot(v) for v in value)
        return f'[{items}]'
    if isinstance(value, dict):
        items = ', '.join(f'{__to_godot(k)}: {__to_godot(v)}' for k, v in value.items())
        return f'{{{items}}}'
    return str(value)   # 未知類別爲字符串

def output_in_one(dic_converted_data : dict, output_fp, header='', tail=''):
    '''
    輸出配置文件至一個文件中
    '''
    result = ''
    result += header.replace('\\n', '\n')
    for conf_name, converted_data in dic_converted_data.items():
        result += f'static var {conf_name} := {__to_godot(converted_data)}\n'
    result += tail.replace('\\n', '\n')
    gFile.write_to_file(result, output_fp)
    print(f'Godot File Done! <{output_fp}>')