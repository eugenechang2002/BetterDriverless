import json

class scenario:
    scenarioID
    pedestrians_on_waypoint_reached
    NPC_waypoint_reached
    NPC_stop_line 
    NPC_lane_change
    weather
    time_of_day
    Ego_sensors
    Ego_position

    def __init__(self, name, age):
        self.scenarioID = scenarioID
        self.pedestrians_on_waypoint_reached = pedestrians_on_waypoint_reached
        self.NPC_waypoint_reached = NPC_waypoint_reached
        self.NPC_stop_line = NPC_stop_line
        self.NPC_lane_change = NPC_lane_change
        self.weather = weather
        self.time_of_day = time_of_day
        self.Ego_sensors = Ego_sensors
        self.Ego_position = Ego_position

    def get_scenarioID():
        return self.scenarioID
    
    def get_pedestrians_on_waypoint_reached():
        return self.pedestrians_on_waypoint_reached

    def get_NPC_waypoint_reached():
        return self.NPC_waypoint_reached

    def get_NPC_stop_line():
        return self.NPC_stop_line

    def get_weather():
        return self.weather

    def get_time_of_day():
        return self.time_of_day

    def get_Ego_sensors():
        return self.Ego_sensors

    def get_Ego_position():
        return self.Ego_position

def serialization(scenario):
    
