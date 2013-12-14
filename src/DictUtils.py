import base64
import collections
import mimetypes
import os
import random
import string
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
    def __quote_plus(val, doEncoding=True):
        if doEncoding:
            urllib.quote_plus(str(val))
        else:
            return val

    @staticmethod
    def __recursiveUrlencode(parentPath, key, val, doEncoding=True):
        # print "parentPath: " + str(parentPath) + ", key: " + str(key) + ", val: " + str(val)
        if None == key or 0 == len(key):
            return []
        if None != parentPath and 0 != len(parentPath):
            path = parentPath + "." + key
        else:
            path = key
        if None == val:
            return [(path, "")]
        if DictUtils.__isPrimitive(val):
            return [(path, DictUtils.__quote_plus(str(val), doEncoding))]
        
        encodedParams = []
        if list == type(val):
            index = 0
            for item in val:
                indexedPath = path + "[" + str(index) + "]"
                if None == item:
                    encodedParams += [(indexedPath, "")]
                elif DictUtils.__isPrimitive(item):
                    encodedParams += [(indexedPath, DictUtils.__quote_plus(str(item), doEncoding))]
                elif DictUtils.__isCollection(item):
                    encodedParams += DictUtils.__recursiveUrlencode("", indexedPath, item)
                index += 1
        elif dict == type(val):
            for k, v in val.iteritems():
                encodedParams += DictUtils.__recursiveUrlencode(path, k, v)
        return encodedParams

    @staticmethod
    def __recursiveUrlencodeAsList(paramDict, doEncoding=True):
        if None == paramDict or 0 == len(paramDict):
            return []
        urlEncodedParams = []
        for key, val in paramDict.iteritems():
            encodedParams = DictUtils.__recursiveUrlencode("", key, val, doEncoding)
            if None == encodedParams or 0 == len(encodedParams):
                continue
            if 0 < len(encodedParams):
                urlEncodedParams += encodedParams
        return urlEncodedParams

    @staticmethod
    def recursiveUrlencode(paramDict):
        urlEncodedParams = DictUtils.__recursiveUrlencodeAsList(paramDict)
        return "&".join(map(lambda u: "=".join(u), urlEncodedParams))
    
    _BOUNDARY_CHARS = string.digits + string.ascii_letters
    
    # Inspired by
    # source: http://code.activestate.com/recipes/578668-encode-multipart-form-data-for-uploading-files-via/
    
    @staticmethod
    def encode_multipart(paramDict, files, boundary=None):
        def escape_quote(s):
            return s.replace('"', '\\"')
    
        if boundary is None:
            boundary = ''.join(random.choice(DictUtils._BOUNDARY_CHARS) for i in range(30))
        lines = []
        
        fields = DictUtils.__recursiveUrlencodeAsList(paramDict, doEncoding=False)
        
        if None != fields and 0 < len(fields):
            for name, value in fields:
                lines.extend((
                    '--{0}'.format(boundary),
                    'Content-Disposition: form-data; name="{0}"'.format(escape_quote(name)),
                    '',
                    str(value),
                ))
        if None != files and 0 < len(files):
            for name, value in files:
                filepath = value['filepath']
                filename = os.path.split(filepath)[1]
                if 'mimetype' in value:
                    mimetype = value['mimetype']
                else:
                    mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
                if 'content' in value:
                    content = value['content']
                else:
                    content = ''
                    with open(filepath, "rb") as inputFile:
                        #content = base64.b64encode(inputFile.read())
                        content = inputFile.read()
                lines.extend((
                    '--{0}'.format(boundary),
                    'Content-Disposition: form-data; name="{0}"; filename="{1}"'.format(
                            escape_quote(name), escape_quote(filename)),
                    'Content-Type: {0}'.format(mimetype),
                    '',
                    content,
                ))
    
        lines.extend((
            '--{0}--'.format(boundary),
            '',
        ))
        body = '\r\n'.join(lines)
    
        headers = {
            'Content-Type': 'multipart/form-data; boundary={0}'.format(boundary),
            'Content-Length': str(len(body)),
        }
    
        return (body, headers)    


#--------------------------------
# [test code]
#--------------------------------
# print "=================================="
# d = {"user" : { "name" : "UJJAWAL", "address" : [ {"city" : "BLR", "phone" : [ ["111", "222"], ["333", "444"]]}, {"city" : "ALD", "phone" : ["555", "666"]}]}}
# print "d: " + str(d)
# print "urlencoded: " + DictUtils.recursiveUrlencode(d)
# print "=================================="
