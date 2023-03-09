"""
Resource: Brevets
"""
from flask import Response, request
from flask_restful import Resource

# You need to implement this in database/models.py
from database.models import Brevet

class Brevet(Resource):
     #GET: finds ALL brevets in the collection, returns them
    def get(self):
        json_object = Brevet.objects().to_jason(0)
        return Response(json_object, mimetype="application/json", status=200)
    
    #POST: inserts a new brevet into the collection based on the fields in the request
    def post(self):
        body = request.json
        result = Brevet(**body).save()
        return {'_id': str(result.id)}, 200

# MongoEngine queries:
# Brevet.objects() : similar to find_all. Returns a MongoEngine query
# Brevet(...).save() : creates new brevet
# Brevet.objects.get(id=...) : similar to find_one

# Two options when returning responses:
#
# return Response(json_object, mimetype="application/json", status=200)
# return python_dict, 200
#
# Why would you need both?
# Flask-RESTful's default behavior:
# Return python dictionary and status code,
# it will serialize the dictionary as a JSON.
#
# MongoEngine's objects() has a .to_json() but not a .to_dict(),
# So when you're returning a brevet / brevets, you need to convert
# it from a MongoEngine query object to a JSON and send back the JSON
# directly instead of letting Flask-RESTful attempt to convert it to a
# JSON for you.
