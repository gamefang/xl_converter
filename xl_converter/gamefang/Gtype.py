# -*- coding: utf-8 -*-

import json
import ast

class gType:
    '''
    類型轉化模塊
    '''
    #region 基礎類型
    @staticmethod
    def to_int(raw) -> int:
        try:
            return int(raw)
        except:
            return 0
    @staticmethod
    def to_float(raw) -> float:
        try:
            return float(raw)
        except:
            return 0.0
    @staticmethod
    def to_bool(raw) -> bool:
        return True if str(raw).lower() in ('true', '1') else False
    @staticmethod
    def to_str(raw) -> str:
        if raw is None:
            return ''
        return str(raw)
    #endregion

    #region 列表
    @staticmethod
    def _parse_raw_list(raw, sep: str = ','):
        '''
        自動解析:
        1,2,3
        [1,2,3]
        (1,2,3)
        1 2 3
        '''
        if raw is None:
            return []
        s = str(raw).strip()
        # 空
        if not s or s in ('[]', '()'):
            return []
        # 嘗試嚴格解析
        for parser in (ast.literal_eval, json.loads):
            try:
                val = parser(s)
                if isinstance(val, (list, tuple)):
                    return list(val)
            except:
                pass        
        # 補全括號再次嘗試
        has_bracket = len(s) >= 2 and s[0] in '([' and s[-1] in ')]'
        if not has_bracket:
            s = '[' + s + ']'
        for parser in (ast.literal_eval, json.loads):
            try:
                val = parser(s)
                if isinstance(val, (list, tuple)):
                    return list(val)
            except:
                pass
        # 仍然失敗，直接分割原字符串
        inner = s[1:-1].strip() if s.startswith(('(', '[')) else s.strip()
        raw_items = inner.split(sep) if sep in inner else inner.split()
        result = []
        for item in raw_items:
            item = item.strip()
            if not item:
                continue
            try:
                result.append(ast.literal_eval(item))
            except:
                result.append(item)  # 純字符串，直接當 str 返回
        return result
        
    @classmethod
    def to_list_int(cls, raw, sep = ',') -> list[int]:
        return [cls.to_int(item) for item in cls._parse_raw_list(raw, sep)]
    @classmethod
    def to_list_float(cls, raw, sep = ',') -> list[float]:
        return [cls.to_float(item) for item in cls._parse_raw_list(raw, sep)]
    @classmethod
    def to_list_bool(cls, raw, sep = ',') -> list[bool]:
        return [cls.to_bool(item) for item in cls._parse_raw_list(raw, sep)]
    @classmethod
    def to_list_str(cls, raw, sep = ',') -> list[str]:
        return [cls.to_str(item) for item in cls._parse_raw_list(raw, sep)]
    #endregion

    #region 字典
    @staticmethod
    def to_dict(raw) -> dict:
        if raw is None:
            return {}
        s = str(raw).strip()
        if not s:
            return {}
        # 嘗試嚴格解析
        for parser in (ast.literal_eval, json.loads):
            try:
                val = parser(s)
                if isinstance(val, dict):
                    return val
            except:
                pass
        # 補全括號再次嘗試
        has_brace = s.startswith('{') and s.endswith('}')
        if not has_brace:
            s = '{' + s + '}'
        for parser in (ast.literal_eval, json.loads):
            try:
                val = parser(s)
                if isinstance(val, dict):
                    return val
            except:
                pass
        # 仍然失敗，寬鬆解析
        inner = s[1:-1].strip() if (has_brace or s.startswith('{')) else s.strip()
        result = {}
        pairs = [p.strip() for p in inner.split(',') if p.strip()]
        for pair in pairs:
            if ':' not in pair:
                continue
            key_part, val_part = pair.split(':', 1)
            key = key_part.strip().strip('"\'')
            if not key:
                continue
            val_str = val_part.strip()
            try:
                value = ast.literal_eval(val_str)
            except:
                value = val_str.strip('"\'')  # 純字符串去掉可能的外層引號
            result[key] = value
        return result
    @classmethod
    def to_list_dict(cls, raw, sep = ',') -> list[dict]:
        return [cls.to_dict(item) for item in cls._parse_raw_list(raw, sep)]
    #endregion

if __name__ == '__main__':
    print(gType.to_list_str('Saint,Cursed,Healing'))
    print(gType.to_list_str('[Saint,Cursed,Healing]'))
    print(gType.to_list_str('["Saint","Cursed","Healing"]'))
    # expect result: ['Saint', 'Cursed', 'Healing']
    print(gType.to_dict('{"ATK": 100}'))
    print(gType.to_dict('"ATK": 100'))
    print(gType.to_dict('ATK: 100, NAME: ABRA'))
    # expect result: {'ATK': 100}