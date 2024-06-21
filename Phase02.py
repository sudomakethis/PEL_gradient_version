import numpy as np
import random as rnd
import dip
import math
from collections import deque

EDGEL = 255
NODGEL = 0

neighbourhood = [(-1,-1),(-1, 0),(-1,+1),
                 ( 0,-1),        ( 0,+1),
                 (+1,-1),(+1, 0),(+1,+1)]

class Phase2:
    def __init__(self, BEM):
        self.ES = []
        self.BEM = np.copy(BEM)
        self.num_edgels_init = np.count_nonzero(BEM == 255)
        self.BEMS = np.zeros((BEM.shape[0],BEM.shape[1],3), dtype="uint8")
        self.parser = Parser()
        self.driver = Driver()

    def Algo(self, seed, show = False):
        while len(np.argwhere(self.BEM != NODGEL)) > 0:
            pivot, dirs = self.parser.get_pivot(self.BEM, seed)
            if pivot is not None:
                segment = self.driver.get_segment(self.BEM, pivot, dirs)
                self.ES.append(segment)        
        self.BEMS = self.get_segmented_image(self.ES, self.BEMS)
        if show:
            dip.show_image(
                        image = self.BEMS,
                        title = "Segmented Edge Map")
            num_segms = len(self.ES)
            num_edgels= sum(len(segm) for segm in self.ES)
            print("Number of Initial Edgels:", self.num_edgels_init)
            print("Number of Segmented Edgels:", num_edgels)
            print("Number of Edgels Eliminated:", self.parser.kill_count)
            print("Number of Segments Created:", num_segms)
        return self.ES, self.BEMS
    
    def get_segmented_image(self, ES, BEM):
        for segment in ES:
            color = (rnd.randint(0, 255),
                     rnd.randint(0, 255),
                     rnd.randint(0, 255))
            for node in segment:
                BEM[node] = color
        return BEM

class Parser:
    def __init__(self):
        self.pivot = None
        self.dirs = None
        self.kill_count = 0

    def get_pivot(self, BEM, seed):
        self.pivot = None
        self.dirs = None
        survivors = np.argwhere(BEM != NODGEL)
        while len(survivors) > 0:
            rnd.seed(seed)
            i, j = rnd.choice(survivors)
            if BEM[i, j] != NODGEL:
                nbr = [(x, y) for x, y in neighbourhood
                        if 0 <= i + x < BEM.shape[0] 
                        and 0 <= j + y < BEM.shape[1]
                        and BEM[i + x, j + y] != NODGEL]
                if len(nbr) == 0:
                    BEM[i,j] = NODGEL
                    self.kill_count += 1 
                    survivors = [(x,y) for x,y in survivors 
                                if (x,y) != (i,j)]
                    continue
                if len(nbr) == 1:
                    if sum([BEM[i + nbr[0][0] + x, j + nbr[0][1] + y] != NODGEL
                            for x, y in neighbourhood
                            if 0 <= i + nbr[0][0] + x < BEM.shape[0] 
                            and 0 <= j + nbr[0][1] + y < BEM.shape[1]]) == 1:
                        BEM[(i,j)] = NODGEL
                        survivors = [(x,y) for x,y in survivors 
                                    if (x,y) != (i,j)]
                        BEM[(i + nbr[0][0], j + nbr[0][1])] = NODGEL
                        self.kill_count += 2 
                        survivors = [(x,y) for x,y in survivors 
                                    if (x,y) != (i + nbr[0][0], j + nbr[0][1])]
                    else:
                        survivors = [(x,y) for x,y in survivors 
                                    if (x,y) != (i,j)]
                        continue
                if len(nbr) >= 2:
                    comb, weig = self.search_directions(nbr)
                    if min(weig) > 2:
                        survivors = [(x,y) for x,y in survivors 
                                    if (x,y) != (i,j)]
                        continue
                    else:
                        self.pivot = (i,j)
                        min_index = weig.index(min(weig))
                        self.dirs = comb[min_index]
                        break
        return self.pivot, self.dirs

    def search_directions(self, nbr):
        combinations = []
        weights = []
        for i in range(len(nbr)):
            for j in range(i + 1, len(nbr)):
                combinations.append((nbr[i], nbr[j]))
        for couple in combinations:
            weight = (abs(sum(dir[0] for dir in couple)) +
                      abs(sum(dir[1] for dir in couple)))
            weights.append(weight)
        return combinations, weights

class Driver:
    def __init__(self):
        self.segment = deque()
        self.predictor1 = Predictor()
        self.predictor2 = Predictor()
        self.maps = [
                {
                    "dir": [(0,1)], #RIGHT
                    "left": [(-1,1),(1,1),(-1,0),(1,0),(-1,-1),(1,-1)],
                    "right": [(1,1),(-1,1),(1,0),(-1,0),(1,-1),(-1,-1)]
                },{
                    "dir": [(0,-1)], #LEFT
                    "left": [(1,-1),(-1,-1),(1,0),(-1,0),(1,1),(-1,1)],
                    "right": [(-1,-1),(1,-1),(-1,0),(1,0),(-1,1),(1,1)]
                },{
                    "dir": [(-1,0)], #UP
                    "left": [(-1,-1),(-1,1),(0,-1),(0,1),(1,-1),(1,1)],
                    "right": [(-1,1),(-1,-1),(0,1),(0,-1),(1,1),(1,-1)]
                },{
                    "dir": [(1,0)], #DOWN
                    "left": [(1,1),(1,-1),(0,1),(0,-1),(-1,1),(-1,-1)],
                    "right": [(1,-1),(1,1),(0,-1),(0,1),(-1,-1),(-1,1)]
                },{
                    "dir": [(-1,1)], #UP-RIGHT
                    "left": [(-1,0),(0,1),(-1,-1),(1,1),(0,-1),(1,0)],
                    "right": [(0,1),(-1,0),(1,1),(-1,-1),(1,0),(0,-1)]
                },{
                    "dir": [(-1,-1)], #UP-LEFT
                    "left": [(0,-1),(-1,0),(1,-1),(-1,1),(1,0),(0,1)],
                    "right": [(-1,0),(0,-1),(-1,1),(1,-1),(0,1),(1,0)]
                },{
                    "dir": [(1,-1)], #DOWN-LEFT
                    "left": [(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0)],
                    "right": [(0,-1),(1,0),(-1,-1),(1,1),(-1,0),(0,1)]
                },{
                    "dir": [(1,1)], #DOWN-RIGHT
                    "left": [(0,1),(1,0),(-1,1),(1,-1),(-1,0),(0,-1)],
                    "right": [(1,0),(0,1),(1,-1),(-1,1),(0,-1),(-1,0)]
                }
            ]

    def get_segment(self, BEM, pivot, dirs):
        self.segment = deque()
        self.segment.append(pivot)
        pivot1, pivot2 = pivot, pivot
        dir1, dir2 = dirs
        go1 = go2 = True
        while go1 or go2:
            if go1:
                pivot1, dir1, diag1 = self.step(BEM, pivot1, 
                                                dir1, self.predictor1)
                if diag1 is not None:
                    self.segment.appendleft(diag1)
            if pivot1 is not None:
                self.segment.appendleft(pivot1)
            else:
                go1 = False
            if go2:
                pivot2, dir2, diag2 = self.step(BEM, pivot2, 
                                                dir2, self.predictor2)
                if diag2 is not None:
                    self.segment.append(diag2)
            if pivot2 is not None:
                self.segment.append(pivot2)
            else:
                go2 = False
        self.predictor1.buffer.clear()
        self.predictor2.buffer.clear()
        return list(self.segment)
    
    def step(self, BEM, pivot, dir, predictor):
        center = pivot
        diag = None
        BEM[center] = NODGEL
        map = [dict(d) for d in self.maps if dir in d["dir"]][0]        
        for key, value in map.items():
            map[key] = [(center[0] + x, center[1] + y) for x, y in value
                        if 0 <= center[0] + x < BEM.shape[0] 
                        and 0 <= center[1] + y < BEM.shape[1]]
        if (any([BEM[x, y] != NODGEL for x, y in map["dir"]])):
            pivot = map["dir"][0]
        else:
            predictor.get_prediction(dir)
            pivot = next((((x, y)) for (x, y) in map[predictor.prediction]
                            if BEM[x, y] != NODGEL), None)
        if pivot is not None:
            BEM[pivot] = NODGEL
            dir = (pivot[0] - center[0], pivot[1] - center[1])
            diag_check = abs(dir[0]) + abs(dir[1])
            if diag_check > 1:
                for d in self.maps[4:]:
                    if d["dir"] == [dir]:
                        for offset in d[predictor.prediction][:2]:
                            xd = center[0] + offset[0]
                            yd = center[1] + offset[1]
                            if (0 <= xd < BEM.shape[0] and
                                0 <= yd < BEM.shape[1] and
                                BEM[(xd,yd)] != NODGEL):
                                diag = (xd,yd)
                                BEM[(xd,yd)] = NODGEL
                                break
                        break
        predictor.buffer.appendleft(dir)
        return pivot, dir, diag
    
class Predictor:
    def __init__(self):
        self.buffer = deque(maxlen = 8)
        self.prediction = "left"

    def get_prediction(self, dir):
        buffer_pruned = deque([x for x in self.buffer if x != dir])
        buffer_sum = tuple(sum(b) for b in zip(*buffer_pruned))
        if len(buffer_sum) > 0:
            angle = self.get_angle(dir,buffer_sum)
            if angle >= 0:
                self.prediction = "left"
            else:
                self.prediction = "right"
        return self.prediction
    
    def get_angle(self, dir1, dir2):
        dir1 = np.array(dir1)
        dir2 = np.array(dir2)
        angle = math.atan2(np.linalg.det(np.vstack((dir1, dir2))), 
                           np.dot(dir1,dir2))
        return angle

class Phase2Gradient:
    def __init__(self, BEM, G, theta):
        self.ES = []
        self.BEM = np.copy(BEM)
        self.num_edgels_init = np.count_nonzero(BEM == 255)
        self.BEMS = np.zeros((BEM.shape[0],BEM.shape[1],3), dtype="uint8")
        self.parser = Parser()
        self.driver = DriverGradient(theta)
        self.G = G
        self.theta = theta

    def Algo(self, seed, show = False):
        while len(np.argwhere(self.BEM != NODGEL)) > 0:
            pivot, dirs = self.parser.get_pivot(self.BEM, seed)
            if pivot is not None:
                segment = self.driver.get_segment(self.BEM, pivot, dirs)
                self.ES.append(segment)        
        self.BEMS = self.get_segmented_image(self.ES, self.BEMS)
        if show:
            dip.show_image(
                        image = self.BEMS,
                        title = "Segmented Edge Map")
            num_segms = len(self.ES)
            num_edgels= sum(len(segm) for segm in self.ES)
            print("Number of Initial Edgels:", self.num_edgels_init)
            print("Number of Segmented Edgels:", num_edgels)
            print("Number of Edgels Eliminated:", self.parser.kill_count)
            print("Number of Segments Created:", num_segms)
        return self.ES, self.BEMS
    
    def get_segmented_image(self, ES, BEM):
        for segment in ES:
            color = (rnd.randint(0, 255),
                     rnd.randint(0, 255),
                     rnd.randint(0, 255))
            for node in segment:
                BEM[node] = color
        return BEM
    
class DriverGradient:
    def __init__(self, theta):
        self.segment = deque()
        self.predictor1 = PredictorGradient(theta)
        self.predictor2 = PredictorGradient(theta)
        self.maps = [
                {
                    "dir": [(0,1)], #RIGHT
                    "left": [(-1,1),(1,1),(-1,0),(1,0),(-1,-1),(1,-1)],
                    "right": [(1,1),(-1,1),(1,0),(-1,0),(1,-1),(-1,-1)]
                },{
                    "dir": [(0,-1)], #LEFT
                    "left": [(1,-1),(-1,-1),(1,0),(-1,0),(1,1),(-1,1)],
                    "right": [(-1,-1),(1,-1),(-1,0),(1,0),(-1,1),(1,1)]
                },{
                    "dir": [(-1,0)], #UP
                    "left": [(-1,-1),(-1,1),(0,-1),(0,1),(1,-1),(1,1)],
                    "right": [(-1,1),(-1,-1),(0,1),(0,-1),(1,1),(1,-1)]
                },{
                    "dir": [(1,0)], #DOWN
                    "left": [(1,1),(1,-1),(0,1),(0,-1),(-1,1),(-1,-1)],
                    "right": [(1,-1),(1,1),(0,-1),(0,1),(-1,-1),(-1,1)]
                },{
                    "dir": [(-1,1)], #UP-RIGHT
                    "left": [(-1,0),(0,1),(-1,-1),(1,1),(0,-1),(1,0)],
                    "right": [(0,1),(-1,0),(1,1),(-1,-1),(1,0),(0,-1)]
                },{
                    "dir": [(-1,-1)], #UP-LEFT
                    "left": [(0,-1),(-1,0),(1,-1),(-1,1),(1,0),(0,1)],
                    "right": [(-1,0),(0,-1),(-1,1),(1,-1),(0,1),(1,0)]
                },{
                    "dir": [(1,-1)], #DOWN-LEFT
                    "left": [(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0)],
                    "right": [(0,-1),(1,0),(-1,-1),(1,1),(-1,0),(0,1)]
                },{
                    "dir": [(1,1)], #DOWN-RIGHT
                    "left": [(0,1),(1,0),(-1,1),(1,-1),(-1,0),(0,-1)],
                    "right": [(1,0),(0,1),(1,-1),(-1,1),(0,-1),(-1,0)]
                }
            ]

    def get_segment(self, BEM, pivot, dirs):
        self.segment = deque()
        self.segment.append(pivot)
        pivot1, pivot2 = pivot, pivot
        dir1, dir2 = dirs
        go1 = go2 = True
        while go1 or go2:
            if go1:
                pivot1, dir1, diag1 = self.step(BEM, pivot1, 
                                                dir1, self.predictor1)
                if diag1 is not None:
                    self.segment.appendleft(diag1)
            if pivot1 is not None:
                self.segment.appendleft(pivot1)
            else:
                go1 = False
            if go2:
                pivot2, dir2, diag2 = self.step(BEM, pivot2, 
                                                dir2, self.predictor2)
                if diag2 is not None:
                    self.segment.append(diag2)
            if pivot2 is not None:
                self.segment.append(pivot2)
            else:
                go2 = False
        self.predictor1.clearBuffer()
        self.predictor2.clearBuffer()
        return list(self.segment)
    
    def step(self, BEM, pivot, dir, predictor):
        center = pivot
        diag = None
        BEM[center] = NODGEL
        map = [dict(d) for d in self.maps if dir in d["dir"]][0]        
        for key, value in map.items():
            map[key] = [(center[0] + x, center[1] + y) for x, y in value
                        if 0 <= center[0] + x < BEM.shape[0] 
                        and 0 <= center[1] + y < BEM.shape[1]]
        if (any([BEM[x, y] != NODGEL for x, y in map["dir"]])):
            pivot = map["dir"][0]
        else:
            predictor.get_prediction(dir, map['dir'])
            pivot = next((((x, y)) for (x, y) in map[predictor.prediction]
                            if BEM[x, y] != NODGEL), None)
        if pivot is not None:
            BEM[pivot] = NODGEL
            dir = (pivot[0] - center[0], pivot[1] - center[1])
            diag_check = abs(dir[0]) + abs(dir[1])
            if diag_check > 1:
                for d in self.maps[4:]:
                    if d["dir"] == [dir]:
                        for offset in d[predictor.prediction][:2]:
                            xd = center[0] + offset[0]
                            yd = center[1] + offset[1]
                            if (0 <= xd < BEM.shape[0] and
                                0 <= yd < BEM.shape[1] and
                                BEM[(xd,yd)] != NODGEL):
                                diag = (xd,yd)
                                BEM[(xd,yd)] = NODGEL
                                break
                        break
        predictor.appendleft(dir)
        return pivot, dir, diag
    

class PredictorGradient:
    def __init__(self, theta):
        self.buffer = deque(maxlen = 8)
        self.prediction = "left"
        self.map = {(0,1):np.pi/2, 
                    (0,-1):np.pi/2, 
                    (-1,0):np.pi, 
                    (1,0):0, 
                    (-1,1):3*np.pi/4, 
                    (-1,-1):np.pi/4, 
                    (1,-1):3*np.pi/4, 
                    (1,1):np.pi/4
                }
        self.pimezzi = np.pi/2
        self.theta = theta
    
    def appendleft(self, dir):
        self.buffer.appendleft(dir)

    def clearBuffer(self):
        self.buffer.clear()

    def get_prediction(self, dir, mapdir):
        if len(mapdir) > 0:
            angle = self.map[dir]  - self.theta[mapdir[0][0], mapdir[0][1]] - self.pimezzi
            if angle < 0:
                self.prediction = "left"
            else:
                self.prediction = "right"
        return self.prediction

dip.WizardFamiliar("Phase 2!")