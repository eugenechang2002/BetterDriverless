import simulation.config as config
import lgsvl
import copy
import json
import time
import random as rd
from lgsvl.agent import NPCControl

def getModuleStatus(fail=False):
  status = {}
  if (fail==False):
    status['Control'] = True
    status['Localization'] = True
    status['Perception'] = True
    status['Radar'] = True
    status['Planning'] = True
    status['Prediction'] = True
    status['Radar'] = True
    status['Routing'] = True
    status['Transform'] = True
    status['Traffic Light'] = True
    status['Camera'] = False
    status['Canbus'] = False
    status['Guardian'] = False
    status['Recorder'] = False
    status['Storytelling'] = False
    status['Third Party Perception'] = False
    status['Velodyne'] = False
  else:
    status['Control'] = False
    status['Localization'] = False
    status['Perception'] = False
    status['Radar'] = False
    status['Planning'] = False
    status['Prediction'] = False
    status['Radar'] = False
    status['Routing'] = False
    status['Transform'] = False
    status['Traffic Light'] = False
    status['Camera'] = False
    status['Canbus'] = False
    status['Guardian'] = False
    status['Recorder'] = False
    status['Storytelling'] = False
    status['Third Party Perception'] = False
    status['Velodyne'] = False
  return status

def outputJSON(size, Script_ID, Scenario_ID, weather, time, velocity=10, total_distance=50, total_time=20, map_name="Boragas Ave", car_type="Lincoln2017MKZ"):
    #sample output file
    output={}
    output['Script_ID'] = Script_ID
    output['Scenario_ID'] = Scenario_ID 

    rand = rd.randint(1,1000)
    if (rand <= 10):
        output['Connection_Error'] = str(True)
        output['Total_Distance'] = 0
        output['Module_Status'] = getModuleStatus(fail=True)
        output['Reach_Destination'] = str(False)
        output['Success']= str(False)
    else:
        output['Connection_Error'] = str(False)
        output['Total_Distance'] = total_distance
        output['Module_Status'] = getModuleStatus()
        output['Reach_Destination'] = str(True)
        output['Success']= str(True)

    ran = rd.randint(1,1000)
    if (ran >= 10):
        output['Collision'] = str(False)
    else:
        output['Collision'] = str(True)

    output['Car_Type'] = car_type
    output['Map'] = map_name
    output['Total_Time'] = total_time
    output['Weather'] = weather ##[1.0, 1.0, 1.0] ##[rain, fog, wetness]
    output['Time_Of_Day'] = time
    output['Velocity'] = velocity

    with open(f"./output/{(size*(Script_ID-1) + Scenario_ID)}.json", "w") as outfile:  
        json.dump( output, outfile, indent = 4) 

