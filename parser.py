import simulation.config as config
import lgsvl
import copy
import json
import time
from lgsvl.agent import NPCControl

def addWeatherCondition(queue, user_json, weather, difference):
    if weather in user_json["Weather"]:
        size = len(queue)
        for _ in range(size):
            cur = queue.pop(0)

            for v in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]:
                temp = copy.deepcopy(cur)

                if "Weather" not in temp:
                    temp["Weather"] = {}
                temp["Weather"][weather] = v
                queue.append(temp)
    return queue

# Generating condition
def getAllPossibleConditions(user_json):
    # EGO

    # Weather
    if "Weather" in user_json:

        for weather in user_json["Weather"]:
            addWeatherCondition(queue, user_json, weather, 0.1)

    return queue

