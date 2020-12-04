from flask import Flask, render_template, flash, url_for, redirect, request
from forms import ResultBoardForm
from alpha_vantage.timeseries import TimeSeries
import datetime
import yfinance as yf
import requests
from datetime import date, timedelta
import os
from os import path
import json as JSON
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/", methods=['GET', 'POST'])
def calculator():
    form = ResultBoardForm()
    pass_queue = []
    fail_queue = []
    detail_page = 0
    for n in range(1,1000):
        fname = str(n) + ".json"
        if path.exists(fname):
            f = open(fname,)
            data = JSON.load(f)
            if data.get("Success") == "True":
                pass_queue.append(n)
            else:
                fail_queue.append(n)
        else:
            break
    if form.validate_on_submit():
        detail_page = form.detail_page.data
        return redirect(url_for('result_detail', fileName = detail_page))
    pass_rate = len(pass_queue)/(len(pass_queue) + len(fail_queue))
    result_detail_url = "localhost:8080/result_detail/" + str(detail_page)
    
    return render_template('result_board.html', title='result_board', form=form, pass_rate = pass_rate, pass_queue = pass_queue, fail_queue = fail_queue, detail_page = detail_page, result_detail_url = result_detail_url)

@app.route('/result_detail/<fileName>')
def result_detail(fileName):
    form = ResultBoardForm()
    fname = fileName+".json"
    f = open(fname,)
    data = JSON.load(f)


    Script_ID = data.get("Script_ID")
    Scenario_ID = data.get("Scenario_ID")
    Success = data.get("Success")
    Car_Type = data.get("Car_Type")
    Map = data.get("Map")
    Total_Time = data.get("Total_Time")
    Reach_Destination = data.get("Reach_Destination")
    Connection_Error = data.get("Connection_Error")
    Total_Distance = data.get("Total_Distance")
    Collision = data.get("Collision")

    #weather
    Weather = data.get("Weather")
    Rain = Weather[0]
    Fog = Weather[1]
    Wetness = Weather[2]

    Time_Of_Day = data.get("Time_Of_Day")
    Velocity = float(data.get("Velocity"))*60*60/1000

    #module status
    Module_Status = data.get("Module_Status")
    Camera = Module_Status.get("Camera")
    Control = Module_Status.get("Control")
    GPS = Module_Status.get("GPS")
    Guardian = Module_Status.get("Guardian")
    Localization = Module_Status.get("Localization")
    Perception = Module_Status.get("Perception")
    Planning = Module_Status.get("Planning")
    Prediction = Module_Status.get("Prediction")
    Radar = Module_Status.get("Radar")
    Recorder = Module_Status.get("Recorder")
    Routing = Module_Status.get("Routing")
    Storytelling = Module_Status.get("Storytelling")
    Traffic_Light = Module_Status.get("Traffic Light")
    Transform = Module_Status.get("Transform")
    Velodyne = Module_Status.get("Velodyne")
    

    # if form.validate_on_submit():
    #         return redirect(url_for('result_detail'))
    return render_template('result_detail.html', title='result', 
    form=form, Script_ID = Script_ID, Scenario_ID = Scenario_ID, Success = Success, Car_Type = Car_Type, 
    Map = Map, Total_Time = Total_Time, Reach_Destination = Reach_Destination, Connection_Error = Connection_Error, Total_Distance = Total_Distance,
     Collision = Collision, Rain = Rain, Fog = Fog, Wetness = Wetness, Time_Of_Day = Time_Of_Day, Velocity = Velocity,
      Camera = Camera, Control = Control, GPS = GPS, Guardian = Guardian,
    Localization = Localization, Perception = Perception, Planning = Planning, Prediction = Prediction, Radar = Radar,
    Recorder = Recorder, Routing = Routing, Storytelling = Storytelling, Traffic_Light = Traffic_Light, Transform = Transform,Velodyne = Velodyne)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
