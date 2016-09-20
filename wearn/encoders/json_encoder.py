# Dependencies
import json

"""
	JSON Encoder class
"""
class JSONEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, float):
       	    return str(obj)
        return json.JSONEncoder.encode(self, obj)