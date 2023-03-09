# UOCIS322 - Project 6 #
Brevet time calculator with MongoDB speficially mongo engine, and a RESTful API!

Read about MongoEngine and Flask-RESTful before you start: [http://docs.mongoengine.org/](http://docs.mongoengine.org/), [https://flask-restful.readthedocs.io/en/latest/](https://flask-restful.readthedocs.io/en/latest/).

## Project Overview

This project we Focusing on Restful API. According to Redhat.com
"A REST API (also known as RESTful API) is an application programming interface (API or web API) that conforms to the constraints of REST architectural style and allows for interaction with RESTful web services. REST stands for representational state transfer and was created by computer scientist Roy Fielding.
REST is a set of architectural constraints, not a protocol or a standard. API developers can implement REST in a variety of ways."

* REST Principles
	* #1 The key abstraction of information is a resource, named by a URI. Any information that can be named can be a resource
	* #2 All interactions are context-free: each 	interaction contains all of the information necessary to understand the request, independent of any requests that may have preceded it.
	* #3 The representation of a resource is a sequence of bytes, plus representation metadata to describe those bytes. The particular form of the representation can be negotiated between REST components
	* #4 Components perform only a small set of well-defined methods on a resource producing a representation to capture the current or intended state of that resource and transfer that representation between components. These methods are global to the specific architectural instantiation of REST; for instance, all resources exposed via HTTP are expected to support each operation identically

I also used a postman to test my api Restful i woulkd reccommend others do the same.
So we fallowed the Schema below in tasks completed to implement.


In this Project We will use project 5s base code which focused on Mongo DB and Docker compose, This project already has two services:

* Brevets
	* The entire web service
* MongoDB
	* As a database

For this project, We re-organized `Brevets` into two separate services:

* Web (Front-end)
	* Time calculator (basically everything you had in project 4)
* API (Back-end)
	* A RESTful service to expose/store structured data in MongoDB.

## Tasks Completed

* Implement a RESTful API in `api/`:
	* Write a data schema using MongoEngine for Checkpoints and Brevets:
		* `Checkpoint`:
			* `distance`: float, required, (checkpoint distance in kilometers), 
			* `location`: string, optional, (checkpoint location name), 
			* `open_time`: datetime, required, (checkpoint opening time), 
			* `close_time`: datetime, required, (checkpoint closing time).
		* `Brevet`:
			* `length`: float, required, (brevet distance in kilometers),
			* `start_time`: datetime, required, (brevet start time),
			* `checkpoints`: list of `Checkpoint`s, required, (checkpoints).
	* Using the schema, build a RESTful API with the resource `/brevets/`:
		* GET `http://API:PORT/api/brevets` should display all brevets stored in the database.
		* GET `http://API:PORT/api/brevet/ID` should display brevet with id `ID`.
		* POST `http://API:PORT/api/brevets` should insert brevet object in request into the database.
		* DELETE `http://API:PORT/api/brevet/ID` should delete brevet with id `ID`.
		* PUT `http://API:PORT/api/brevet/ID` should update brevet with id `ID` with object in request.

* Copy over `brevets/` from your completed project 5.
	* Replace every database related code in `brevets/` with calls to the new API.
		* Hint: Submit should send a POST request to the API to insert, Display should send a GET request, and display the last entry.
	* Remove `config.py` and adjust `flask_brevets.py` to use the `PORT` and `DEBUG` values specified in env variables (see `docker-compose.yml`).

* Updated README.md with API documentation added.

As always you'll turn in your `credentials.ini` through Canvas.

## Personal Notes

* This project is a built out project form p4 and p5 each biuilding on eachother. 
* this project required no html/ js updtaes.
* this code focues on flask and files cross commuication though directory structure.
*This project uses an api to access database and reuse of project 4 alogithm and p5 flask API strucure. 
* We just change this to a restful API

## Authors

Daniel Willard
