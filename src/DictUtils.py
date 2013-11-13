import collections
import urllib


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
    def __isPrimitive(val):
        return type(val) in [int, float, bool, str]

    @staticmethod
    def __isCollection(val):
        return type(val) in [dict, list]

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

    @staticmethod
    def __recursiveUrlencode(parentPath, key, val):
        #print "parentPath: " + str(parentPath) + ", key: " + str(key) + ", val: " + str(val)
        if None == key or 0 == len(key):
            return []
        if None != parentPath and 0 != len(parentPath):
            path = parentPath + "." + key
        else:
            path = key
        if None == val:
            return [(path, "")]
        if DictUtils.__isPrimitive(val):
            return [(path, urllib.quote_plus(str(val)))]
        
        encodedParams = []
        if list == type(val):
            index = 0
            for item in val:
                indexedPath = path + "[" + str(index) + "]"
                if None == item:
                    encodedParams += [(indexedPath, "")]
                elif DictUtils.__isPrimitive(item):
                    encodedParams += [(indexedPath, urllib.quote_plus(str(item)))]
                elif DictUtils.__isCollection(item):
                    encodedParams += DictUtils.__recursiveUrlencode("", indexedPath, item)
                index += 1
        elif dict == type(val):
            for k, v in val.iteritems():
                encodedParams += DictUtils.__recursiveUrlencode(path, k, v)
        return encodedParams

    @staticmethod
    def recursiveUrlencode(paramDict):
        if None == paramDict or 0 == len(paramDict):
            return ""
        urlEncodedParams = []
        for key, val in paramDict.iteritems():
            encodedParams = DictUtils.__recursiveUrlencode("", key, val)
            if None == encodedParams or 0 == len(encodedParams):
                continue
            if 0 < len(encodedParams):
                urlEncodedParams += encodedParams
        return "&".join(map(lambda u: "=".join(u), urlEncodedParams))


#--------------------------------
# [test code]
#--------------------------------
print "=================================="
d = {"user" : { "name" : "UJJAWAL", "address" : [ {"city" : "BLR", "phone" : [ ["111", "222"], ["333", "444"]]}, {"city" : "ALD", "phone" : ["555", "666"]}]}}
print "d: " + str(d)
print "urlencoded: " + DictUtils.recursiveUrlencode(d)
print "=================================="