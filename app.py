import falcon
import resources
from pymongo import MongoClient

# Init connection to the MongoDB collection
connection = MongoClient('mongodb://localhost:27017')
db = connection.test.firstcollection

api  = application = falcon.API()

resource = resources.Resource(db)
api.add_route('/', resource)