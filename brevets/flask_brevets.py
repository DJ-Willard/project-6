"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import os
import logging
# The library we use to send requests to the API
# Not to be confused with flask.request.
import requests
import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations


###
# Globals
###
app = flask.Flask(__name__)


##################################################
################### API Callers ################## 
##################################################
API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

def retrieve_brevet():
    control_lists = requests.get(f"{API_URL}/brevets").json()
    brevet = control_lists[-1]
    return brevet["brevet_dist"], brevet["start_time"], brevet["control_list"]

def insert_brevet(brevet_dist, start_time, control_list):
    _id = requests.post(f"{API_URL}/brevets", json={"brevet_dist": brevet_dist, "start_time": start_time, "control_list": control_list}).json()
    return _id

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404

@app.route("/_insert_b", methods=["POST"])
def _insert_b():
    #Work Here
    app.logger.debug("in insert function")
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!

        # Because input_json is a dictionary, we can do this:
        brevet_dist = input_json["brevet_dist"]
        start_time = input_json["start_time"]
        control_list = input_json["control_list"]

        b_db_id = insert_brevet(brevet_dist, start_time, control_list)

        return flask.jsonify(result={},
                             message="Inserted!",
                             status=1,  # This is defined by you. You just read this value in your javascript.
                             mongo_id=b_db_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                             message="Oh no! Server error!",
                             status=0,
                             mongo_id='None')


@app.route("/_retrieve_b")
def _retrive_b():
    #WORK HERE
    """
    /fetch : fetches the newest to-do list from the database.
    Accepts GET requests ONLY!
    JSON interface: gets JSON, responds with JSON
    """
    app.logger.debug("we are in RB")
    try:
        brevet_dist, start_time, control_list = retrieve_brevet()
        app.logger.debug(f'bDist {brevet_dist}')
        app.logger.debug(f'sTime {start_time}')
        app.logger.debug(f'control {control_list}')
        return flask.jsonify(
                result={"brevet_dist": brevet_dist, "start_time": start_time, "control_list": control_list},
                status=1,
                message="Successfully fetched brevet list!")
    except:
        return flask.jsonify(
                result={},
                status=0,
                message="Something went wrong, couldn't fetch any Brevets!")

###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    #added fetch for the distance and start time
    brevet_dist = request.args.get('brevet_dist', 999, type=float)
    start_time  = request.args.get('start_time', type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    #fix implented distance reset and and start time reformated
    start_time_for = arrow.get(start_time, "YYYY-MM-DDTHH:mm")

    open_time = acp_times.open_time(km, brevet_dist, start_time_for).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, start_time_for).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


#############

app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(port=os.environ["PORT"], host="0.0.0.0")
