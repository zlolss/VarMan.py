

import collections as __collections

class VarMan(__collections.abc.Mapping):
    
    '''
用法：
var=VarManager()
modifydset = var.POPMODIFY(tag='default')
for key in modifydset:
    print(var[key])

@var.ONMODIFY('varname')
def fun(pre, nxt):
    pass
    
注意：带前缀“_”的变量不会监听赋值状态，也不会被迭代
'''
    
    def __init__(self, **defaults):
        
        from typing import Callable, List, Dict
        
        self.__vars = defaults
        self.__modify_sequence = []
        self.__modify_sequence_dropped = 0
        self.__consumers_seek = {'default':0}
        self.__listeners:Dict[str,List[Callable]] = {}
        self.__anylisteners:List[Callable] = []
    
    
    def ONMODIFY(self, key:str):
        if key not in self.__listeners:
            self.__listeners[key] = []
        def onmodify(func):
            self.__listeners[key].append(func)
            # print(f'addlistener:{func}')
            return func
        return onmodify
        
    
    def REMOVELISTENER(self, key):
        if key in self.__listeners:
            del(self.__listeners[key])
            
    
    def REMOVEANYLISTENER(self):
        self.__anylisteners = []
    
    
    def ONMODIFYANY(self, func):
        self.__anylisteners.append(func)
        return func

    
    def POPMODIFY(self, tag = 'default'):
        seek = self.__consumers_seek.get(tag, self.__modify_sequence_dropped)
        dropped = self.__modify_sequence_dropped
        modify_sequence = self.__modify_sequence
        right = len(modify_sequence)
        left = seek - dropped
        left = 0 if left<0 else left
        modify_set = set(modify_sequence[left:right])
        self.__consumers_seek[tag] = dropped + right
        miniseek = min(self.__consumers_seek.values())
        dropnew = miniseek - dropped
        dropnew = 0 if dropnew<0 else dropnew
        self.__modify_sequence = modify_sequence[dropnew:]
        self.__modify_sequence_dropped = dropnew + dropped
        return modify_set
    
    def __getitem__(self, key):

        return self.__getattr__(key)
    
    
    def __setitem__(self, key, value):
        return self.__setattr__(key, value)
    
    # -------------- wrap dict ---------------
    def __iter__(self):

        return iter(self.__vars)
        
    def items(self):
        return self.__vars.items()
        
    def keys(self):
        return self.__vars.keys()
        
    def __str__(self):
        return str(self.__vars)
        
    def __repr__(self):
        return f'{self.__class__.__name__}({self.__str__()})'
            

    # todo: remove 
    
    # -------------- wrap dict end ---------------
    
    def __getattr__(self, key):
        if not self.__isValidVarName(key):
            raise TypeError(f'变量名{key}不合法')
        if key[0] == '_':
            return self.__dict__[key]
        return self.__vars[key]
    

    def __setattr__(self, key, value):
        if not self.__isValidVarName(key):
            raise TypeError(f'变量名{key}不合法')
        if key[0] == '_':
            self.__dict__[key] = value
            return 
        
        if key in self.__vars and self.__vars[key] == value:
            return
        
        prevalue = self.__vars.get(key, None)
        self.__vars[key] = value
        self.__modify_sequence.append(key)
        
        callbacks = self.__listeners.get(key, None)
        if callbacks is not None:
            for callback in callbacks:
                callback(prevalue, value)
                
        for callback in self.__anylisteners:
            callback(key, prevalue, value)
            
    
    def __len__(self):
        return 1
    
    def __isValidVarName(self, name):
        if not isinstance(name, str):
            return False
        if name[:2]=='__':
            return False
        first = ord(name[0].lower())
        if first>=ord('a') and first<=ord('z') or first==ord('_'):
            return True
        return False
    
    