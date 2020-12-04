import simulation.config as config
import lgsvl
import copy
import json
import time
import numpy as np
from lgsvl.agent import NPCControl

def addWeatherCondition(secenarios, user_json, weather, difference=0.5):
    if weather in user_json["Weather"]:
        size = len(secenarios)
        for _ in range(size):
            cur = secenarios.pop(0)

            for v in np.arange(0,1.1,difference):
                temp = copy.deepcopy(cur)

                if "Weather" not in temp:
                    temp["Weather"] = {}
                temp["Weather"][weather] = v
                secenarios.append(temp)
    return secenarios

def addTimeCondition(secenarios, user_json, difference=0 , timeList=[5,7,9,11,13,15,17,19,21,23]):
    time_of_day = 24
    if "Time" in user_json:
        time_of_day = user_json["Time"]["TimeOfDay"]

    size = len(secenarios)
    for _ in range(size):
        cur = secenarios.pop(0)

        if time_of_day == 24:
            if(difference!=0):
                c = range(1,25,difference) 
                for v in c:
                    temp = copy.deepcopy(cur)

                    if "Time" not in temp:
                        temp["Time"] = {}
                    temp["Time"]["TimeOfDay"] = v
                    secenarios.append(temp)
            else:
                for v in timeList:
                    temp = copy.deepcopy(cur)

                    if "Time" not in temp:
                        temp["Time"] = {}
                    temp["Time"]["TimeOfDay"] = v
                    secenarios.append(temp)
        else:
            temp = copy.deepcopy(cur)
            if "Time" not in temp:
                temp["Time"] = {}
            temp["Time"]["TimeOfDay"] = time_of_day
            secenarios.append(temp)

    return secenarios

def addTrafficLight(secenarios, user_json):
    # TODO
    return


# Generating condition
def getAllPossibleConditions(secenarios, user_json):

    # Weather
    if "Weather" in user_json:
        for weather in user_json["Weather"]:
            addWeatherCondition(secenarios, user_json, weather, difference = 0.5)
    
    # Time
    addTimeCondition(secenarios, user_json)


    return secenarios

