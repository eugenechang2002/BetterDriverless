from flask import Flask, render_template, flash, url_for, redirect, request
from forms import CalculateForm, realTimeInfoForm, invsForm, ResultBoardForm
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

@app.route('/result_board', methods=['GET', 'POST'])
def result_board():
    form = ResultBoardForm()
    pass_queue = []
    fail_queue = []
    detail_page = 0
    for n in range(1,100):
        fname = str(n) + ".json"
        if path.exists(fname):
            f = open(fname,)
            data = JSON.load(f)
            if data.get("Success") == "true":
                pass_queue.append(fname)
            else:
                fail_queue.append(fname)
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
    data = JSON.load(f)#TODO:need to know detailed col name


    Script_ID = data.get("Script_ID")
    Scenario_ID = data.get("Scenario_ID")
    Success = data.get("Success")
    Car_Type = data.get("Car_Type")
    Map = data.get("Map")
    Total_Time = data.get("Total_Time")
    Reach_Destination = data.get("Reach_Destination")
    Connection_Error = data.get("Connection_Error")
    Location_Start = data.get("Location_Start")
    Location_End = data.get("Location_End")
    Collision = data.get("Collision")

    Weather = data.get("Weather")
    Time_Of_Day = data.get("Time_Of_Day")
    Velocity = data.get("Velocity")

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
    

    if form.validate_on_submit():
            return redirect(url_for('result_detail'))
    return render_template('result_detail.html', title='result', 
    form=form, Script_ID = Script_ID, Scenario_ID = Scenario_ID, Success = Success, Car_Type = Car_Type, 
    Map = Map, Total_Time = Total_Time, Reach_Destination = Reach_Destination, Connection_Error = Connection_Error, Location_Start = Location_Start,
    Location_End = Location_End, Collision = Collision, Weather = Weather, Time_Of_Day = Time_Of_Day, Velocity = Velocity,
    Module_Status = Module_Status, Camera = Camera, Control = Control, GPS = GPS, Guardian = Guardian,
    Localization = Localization, Perception = Perception, Planning = Planning, Prediction = Prediction, Radar = Radar,
    Recorder = Recorder, Routing = Routing, Storytelling = Storytelling, Traffic_Light = Traffic_Light, Transform = Transform,Velodyne = Velodyne)




def creatImage(ts,img,input_amount, valueList, valueList2):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    imageUrl = os.path.join(SITE_ROOT, 'static/',img)
    profit = getProfit(input_amount, valueList, valueList2)
    days = [1,2,3,4,5]
    matplotlib.use('Agg')
    plt.plot(days, valueList)
    plt.xlabel('days')
    plt.ylabel('Prices')
    plt.title('Price vs. Days on First Method')
    plt.savefig(imageUrl)
    plt.clf()


def getJsonResult(symbol):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, symbol+".json")
    r = json.load(open(json_url))
    data=[]
    #dt = date.today()
    date_time_str = '2020-05-13'   #write todays date
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    dt = date_time_obj.date()
    for i in range(5):
        dt = getMostRecentBusinessDay(dt)
        data.append( r["Time Series (Daily)"][str(dt)]["4. close"] )
    return list(reversed(data))