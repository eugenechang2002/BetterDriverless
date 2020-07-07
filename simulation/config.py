import os
import lgsvl

class Config():

    def __init__(self, simulator="SIMULATOR_HOST", ip="127.0.0.1", port=8181):
        self.simulator = simulator
        self.ip = ip
        self.port = port

    def Simulator(self):
        # Connects to the simulator instance at the ip defined by SIMULATOR_HOST, default is localhost or 127.0.0.1
        sim = lgsvl.Simulator(os.environ.get(self.simulator, self.ip), self.port)
        return sim

    def LoadOrResetScene(self, sim, sceneName):
        if sim.current_scene == sceneName:
            sim.reset()
        else:
            sim.load(sceneName)

    def Raycast_Layer(self, layers=[0,10,11,12]):
        # useful bits in layer mask
        # 0 - Default (road & ground)
        # 9 - EGO vehicles
        # 10 - NPC vehicles
        # 11 - Pedestrian
        # 12 - Obstacle

        # Included layers can be hit by the rays. Otherwise the ray will go through the layer
        layer_mask = 0
        for bit in layers: # do not put 9 here, to not hit EGO vehicle itself
            layer_mask |= 1 << bit
        return layer_mask

# uncomment for testing
# c = Config()
# sim = c.Simulator()
# print("Version =", sim.version)
# print("Current Time =", sim.current_time)
# print("Current Frame =", sim.current_frame)