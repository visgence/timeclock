"""
" clocker/hashMethods.py
" Contributing Authors:
"    Evan Salazar (Visgence, Inc)
"
" (c) 2012 Visgence, Inc., RegionIX Education Cooperative
"""
import hashlib
import base64


def hash64(data):
    # fix strange characters in some criterias causing problems
    # data = data.replace(u'\u2019',"'")

    data = data.encode('utf-8')
    h = base64.b64encode(hashlib.sha1(data).digest())
    print(h)

    # Fix the hash so it is URL Safe
    h = str(h).replace('+', '-')
    h = str(h).replace('/', '_')
    h = str(h).replace('=', '')
    return h
