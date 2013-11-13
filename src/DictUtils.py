import collections
class DictUtils:
    
    @staticmethod
    def __retrieveFromDict(t, key):
        if None != t:
            found = True
            if str == type(key):
                keys = key.split('.')
            else:
                keys = key
            for k in keys:
                if k in t:
                    t = t[k]
                else:
                    found = False
                    break
            if found:
                return t
        return None
        
    @staticmethod
    def defaultIfNone(theDict, defaultDict, key):
        if None == key:
            return None
        
        val = DictUtils.__retrieveFromDict(theDict, key)
        if None != val:
            return val
        
        return DictUtils.__retrieveFromDict(defaultDict, key)
    
    @staticmethod
    def convert(data):
        if int == type(data):
            return int(data)
        elif float == type(data):
            return float(data)
        elif bool == type(data):
            return bool(data)
        elif isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(DictUtils.convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(DictUtils.convert, data))
        else:
            return data