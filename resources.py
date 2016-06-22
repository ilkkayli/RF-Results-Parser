import falcon
import json
from bson.json_util import dumps

# Resource class for handling HTTP requests
class Resource(object):

    def __init__(self, db):
        self.db = db
    
    # Method for handling GET requests. Returns all documents from the db.    
    def on_get(self, req, resp):
        
        result = self.db.find({}).sort("date") # Sorts the query result in ascending order, date as the key
        l = list(result)
        l = dumps(l)        
        resp.body = l # Result converted to JSON data and returned
        resp.status = falcon.HTTP_200
     
    # Method for handling PUT requests
    def on_put(self, req, resp):
        
        '''Example raw_json: {"date":"2016-06-21", "passRate":"96.7"} that updates all documents
         having date 2016-06-21. New value for the passrate is 96.7'''
        
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)
        
        try:
            result_json = json.loads(raw_json, encoding='utf-8')
            json_args = raw_json.split(',')
            json_arg0 = json_args[0].split('"')
            json_arg0 = json_arg0[3]
            json_arg1 = json_args[1].split('"')
            json_arg1 = json_arg1[3]

        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON '
                                   'Please use format {"value_name":"query_value","value_name":"new_value"}' )

        update_result = self.db.update_one({"date":json_arg0}, {"$set": {"passRate":json_arg1}})
        resp.status = falcon.HTTP_202
    
    # Method for handling POST requests    
    def on_post(self, req, resp):
        
        '''Example raw_json: {"date":"2016-06-21", "passRte":"96.7"} that creates a new document in a collection'''
       
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)
        
        try:
            result_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON')

        self.db.insert_one(result_json).inserted_id        
        resp.status = falcon.HTTP_201       
    
    # Method for handling DELETE requests 
    def on_delete(self, req, resp):
        
        '''Removes one document from a collection
        Example raw_json: {"date":"2016-06-21", "passRate":"96.7"} OR {"date":"2016-06-21"}'''
        
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', ex.message)
        
        try:
            result_json = json.loads(raw_json, encoding='utf-8')
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON')

        self.db.delete_one(result_json)        
        resp.status = falcon.HTTP_200           
        

        

