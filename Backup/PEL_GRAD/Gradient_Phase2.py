from enum import Enum
import numpy as np
import random as rnd
from collections import deque
import itertools

global ARR_CORRESP

class AlgoDirections(Enum):
    CENTER=0,
    UP=1,
    UP_RIGHT=2,
    RIGHT=3,
    DOWN_RIGHT=4,
    DOWN=5,
    DOWN_LEFT=6,
    LEFT=7
    UP_LEFT=8

ARR_CORRESP = [
    (1,0,AlgoDirections.UP),#1
    (1,1,AlgoDirections.UP_RIGHT),#2
    (0,1,AlgoDirections.RIGHT),#3
    (-1,1,AlgoDirections.DOWN_RIGHT),#4
    (-1,0,AlgoDirections.DOWN),#5
    (-1,-1,AlgoDirections.DOWN_LEFT),#6
    (0,-1,AlgoDirections.LEFT),#7
    (1,-1,AlgoDirections.UP_LEFT)#8
]

class Phase2_EdgeAvailabilityManager:
    def __init__(self,edges):
        self.av_arr=[]
        self.edges = edges
        #Populate temp list with all possible values allowed (so only the ones having 2 or
        #more neighboors)
        for i in range(edges.shape[0]):
            for j in range(edges.shape[1]):
                if edges[i,j]!=0:
                    self.av_arr.append((i,j))

    def search_neig(self,i,j):
        count=0
        for t_corresp in ARR_CORRESP:
            #Sum the "origin" position with relative positions provided by t_corresp
            t_x=i+t_corresp[0]
            t_y=j+t_corresp[1]
            if t_x < 0 or t_y < 0 or t_x >= self.edges.shape[0] or t_y >= self.edges.shape[1]:
                continue
            #Check if neighboor is an edge
            if self.edges[t_x,t_y]!=0 and self.is_edge_available(t_x,t_y):
                #if true check if there was already an edge
                if count==1:
                    #if true stop the cycle and return True
                    return (True,False)
                #Otherwhise increment the counter and check if there is another one
                count+=1
        #Otherwhise return false = the edge has less or equal then 1 neighboor
        if count == 0:
            #remove this element
            self.set_edge_unavailable(i,j)
            return (False,True)
        return (False,False)#is_ok? , one edge has been eliminated?

    def find_at(self,start_index,end_count):
        curr_index = 0
        for curr_index in range(start_index,end_count):
            t_value = self.av_arr[curr_index]
            found,elim = self.search_neig(t_value[0],t_value[1])
            if elim:
                #1 element has just been eliminated
                return (False, True, curr_index)
            if found:
                return (True, False, curr_index)
        return (False, False, curr_index) #Return error with none value
        
    def get_new_available_edge(self):
        #curr_index is the last "avaiable" index of "av_arr"
        _length = len(self.av_arr)
        curr_index=0
        found = False
        while (found == False):
            found,removed_one_element,curr_index = self.find_at(curr_index,_length)
            #If the algorithm remove one element, re-do the loop starting from i (and not from start)
            if removed_one_element:
                _length -= 1
                continue
            if found:
                #if found catch the value
                t_value = self.av_arr[curr_index]
                #remove it from avaliability array
                self.av_arr.remove(t_value)
                #and return
                return (True,t_value)
            #If not found break the loop immediately
            return (False, None)
        return (False, None)

 
    def is_edge_available(self,i,j):
        for x,y in self.av_arr:
            if x==i and y==j:
                return True
        return False

    def set_edge_unavailable(self,i,j):
        self.av_arr.remove((i,j))
        

class Predictor:
    def __init__(self, Theta_original):
        self.last8directions = deque([])
        self.prediction = (None,None)
        self.Theta_original = Theta_original

    def update_prediction(self,i,j,curr_direction):
        if len(self.last8directions) == 9:
            self.last8directions.popleft()
        self.last8directions.append((i,j))
        self.calculate_next_prediction(curr_direction, self.Theta_original[i,j])
        
    def calculate_next_prediction(self, curr_direction, thetaij):
        if curr_direction == AlgoDirections.RIGHT or curr_direction == AlgoDirections.LEFT:
            #UP,DOWN
            if thetaij>0:
                self.prediction = AlgoDirections.UP
            else:
                self.prediction = AlgoDirections.DOWN
        elif curr_direction == AlgoDirections.DOWN or curr_direction == AlgoDirections.UP:
            if thetaij > -90 and thetaij <= 90:
                self.prediction = AlgoDirections.RIGHT
            else:
                self.prediction = AlgoDirections.LEFT

        elif curr_direction == AlgoDirections.DOWN_RIGHT:
            if thetaij < 45 and thetaij >= -135:
                self.prediction = AlgoDirections.RIGHT
            else:
                self.prediction = AlgoDirections.DOWN
        elif curr_direction == AlgoDirections.UP_LEFT:
            if thetaij < 45 and thetaij >= -135:
                self.prediction = AlgoDirections.UP
            else:
                self.prediction = AlgoDirections.LEFT

        elif curr_direction == AlgoDirections.DOWN_LEFT:
            if thetaij < 135 and thetaij >= -45:
                self.prediction = AlgoDirections.DOWN
            else:
                self.prediction = AlgoDirections.LEFT
        elif curr_direction == AlgoDirections.UP_RIGHT:
            if thetaij < 135 and thetaij >= -45:
                self.prediction = AlgoDirections.RIGHT
            else:
                self.prediction = AlgoDirections.UP

        
        #--error ... never occurred in theory ---  do nothing

    def get_prediction(self):
        return self.prediction


class Segment:
    def __init__(self, center_coords, edges, edge_avail_manager,Theta_original):
        self.EdgeManager = edge_avail_manager
        self.nodes = [center_coords]
        self.center_coords = center_coords
        self.curr_direction = -1
        self.edges = edges
        self.predictor = Predictor(Theta_original)
        self.arr_pred = [ #dir, pred, arr_to_check_in_order
            [AlgoDirections.RIGHT, AlgoDirections.DOWN, [(1,-1),(1,1),(0,-1),(0,1),(-1,-1),(-1,1)]],
            [AlgoDirections.RIGHT, AlgoDirections.UP, [(1,1),(1,-1),(0,1),(0,-1),(-1,1),(-1,-1)]],
            [AlgoDirections.LEFT, AlgoDirections.UP, [(-1,1),(-1,-1),(0,1),(0,-1),(1,1),(1,-1)]],
            [AlgoDirections.LEFT, AlgoDirections.DOWN, [(-1,-1),(-1,1),(0,-1),(0,1),(1,-1),(1,1)]],

            [AlgoDirections.UP, AlgoDirections.LEFT, [(-1,1),(1,1),(-1,0),(1,0),(-1,-1),(1,-1)]],
            [AlgoDirections.UP, AlgoDirections.RIGHT, [(1,1),(-1,1),(1,0),(-1,0),(1,-1),(-1,-1)]],
            [AlgoDirections.DOWN, AlgoDirections.LEFT, [(-1,-1),(1,-1),(-1,0),(1,0),(-1,1),(1,1)]],
            [AlgoDirections.DOWN, AlgoDirections.RIGHT, [(1,-1),(-1,-1),(1,0),(-1,0),(1,1),(-1,1)]],

            [AlgoDirections.DOWN_RIGHT, AlgoDirections.DOWN, [(0,1),(1,0),(-1,1),(1,-1),(-1,0),(0,-1)]],
            [AlgoDirections.DOWN_RIGHT, AlgoDirections.RIGHT, [(1,0),(0,1),(1,-1),(-1,1),(0,-1),(-1,0)]],
            [AlgoDirections.UP_LEFT, AlgoDirections.LEFT, [(-1,0),(0,-1),(-1,1),(1,-1),(0,1),(1,0)]],
            [AlgoDirections.UP_LEFT, AlgoDirections.UP, [(0,-1),(-1,0),(1,-1),(-1,1),(1,0),(0,1)]],

            [AlgoDirections.DOWN_LEFT, AlgoDirections.DOWN, [(0,1),(-1,0),(1,1),(-1,-1),(1,0),(0,-1)]],
            [AlgoDirections.DOWN_LEFT, AlgoDirections.LEFT, [(-1,0),(0,1),(-1,-1),(1,1),(0,-1),(1,0)]],
            [AlgoDirections.UP_RIGHT, AlgoDirections.RIGHT, [(1,0),(0,-1),(1,1),(-1,-1),(0,1),(-1,0)]],
            [AlgoDirections.UP_RIGHT, AlgoDirections.UP, [(0,-1),(1,0),(-1,-1),(1,1),(-1,0),(0,1)]]
        ]
        self.predictor.update_prediction(center_coords[0],center_coords[1],self.curr_direction)

    def get_direction_from_coords(self,coords_center, other_coords):
        d_x = other_coords[0]-coords_center[0]
        d_y = other_coords[1]-coords_center[1]
        for i,j,code in ARR_CORRESP:
            if i==d_x and j==d_y:
                return code
        return None

    def get_relative_coords_from_direction(self,direction):
        for i,j,code in ARR_CORRESP:
            if code == direction:
                return (i,j)
        return (None,None)

    def set_initial_direction(self,coord1):#Set initial direction
        self.set_new_edge_and_update(coord1,True)

    def drive(self):
        while True:
            #First we've to check if there is one edge in current direction
            #Otherwise we'll use the "prediction manager".
            #So, the last element we've added is exactly the current pixel.
            last_node = self.nodes[-1]
            t_i,t_j = self.get_relative_coords_from_direction(self.curr_direction)
            if t_i == None:
                return False
            real_coord_x = last_node[0]+t_i
            real_coord_y = last_node[1]+t_j
           # print("Controllo ("+str(real_coord_x+1)+" "+str(real_coord_y+1)+")")
            if real_coord_x >= 0 and real_coord_y >= 0 and real_coord_x < self.edges.shape[0] and real_coord_y < self.edges.shape[1]:
                #Now check if there is one edge in that position
                if self.edges[real_coord_x,real_coord_y] != 0 and self.EdgeManager.is_edge_available(real_coord_x,real_coord_y):
                    #If ok continue without any problem
                    self.set_new_edge_and_update((real_coord_x,real_coord_y))
                    #No changes in current direction
                    continue
            predicted_direction = self.predictor.get_prediction()
            #Use the arr_pred to get new position
            for tdir, tpred, tordarr in self.arr_pred:
                if tpred == predicted_direction and tdir==self.curr_direction:
                    #Now check the ordered array the first occurrence (first edge)
                    if self.try_append_node_from_dir_and_pred(tordarr,last_node):
                        break
                    else:
                        return True
                        #If prediction and current direction fails, means that is
                        #the last edge of that segment, so stop the loop and return True
                        #cause segment is ok but finished. (In any other case return false).

    #This function try to find and to append a new node following t_ordered_array given in input
    def try_append_node_from_dir_and_pred(self,t_ordered_arr,last_node):
        for t_elem_in_ord_arr in t_ordered_arr:
            t_x = last_node[0] + t_elem_in_ord_arr[1]
            t_y = last_node[1] + t_elem_in_ord_arr[0]
            if t_x >= 0 and t_y >= 0 and t_x < self.edges.shape[0] and t_y < self.edges.shape[1]:
                if self.edges[t_x,t_y] != 0 and self.EdgeManager.is_edge_available(t_x,t_y):
                    newcoords = (t_x,t_y)
                    self.set_new_edge_and_update(newcoords,True)
                    return True
        return False

    def set_new_edge_and_update(self,newcoords,set_direction=False):
        tdir = self.get_direction_from_coords(self.nodes[-1],newcoords)
        self.EdgeManager.set_edge_unavailable(newcoords[0],newcoords[1])
        self.nodes.append(newcoords) #Append new edge
        #print("Appendo ("+str(newcoords[0]+1)+","+str(newcoords[1]+1)+")")
        self.predictor.update_prediction(newcoords[0],newcoords[1],tdir) #update prediction
        if set_direction:
            self.curr_direction = tdir

    def get_nodes(self):
        return self.nodes

    def append_nodes_at_start(self,other_nodes):
        del other_nodes[0]
        if len(other_nodes)>1:
            other_nodes.reverse()
        self.nodes = list(itertools.chain(other_nodes, self.nodes))

    def append_nodes_at_k(self,other_nodes, k):
        self.nodes = list(itertools.chain(self.nodes[0:k+1],other_nodes))
        


class Phase2_Algorithm:
    def __init__(self,edges):
        self.EdgeManager = Phase2_EdgeAvailabilityManager(edges)
        self.segments = []
        self.edges = edges

    def start_algorithm(self,Theta_original):
        while True:#While new edge is available
            (is_ok,coords) = self.EdgeManager.get_new_available_edge()
            #Return coordinates of an edge which has at least 2 neighboors
            if is_ok:
                #print("Parto da ("+str(coords[0]+1)+" "+str(coords[1]+1)+")")
                #If is ok, obtain pixel coordinates in the most opposite directions possible
                (coord1,coord2) = self.get_coords_of_opposite_directions(coords[0],coords[1])
                #print(str(coord1)+" - "+str(coord2))
                segment1 = Segment(coords,self.edges,self.EdgeManager,Theta_original)#Create new segment
                segment1.set_initial_direction(coord1)#Set initial opposite directions

                segment2 = Segment(coords,self.edges,self.EdgeManager,Theta_original)#Create new segment
                segment2.set_initial_direction(coord2)#Set initial opposite directions

                segment1_ok = segment1.drive()#And move throught both direction until reach the end from both.
                segment2_ok = segment2.drive()#And move throught both direction until reach the end from both.

                if segment1_ok and segment2_ok:
                    #unify 2 segments
                    segment1.append_nodes_at_start(segment2.get_nodes())
                    self.segments.append(segment1)
                elif segment1_ok and segment2_ok == False:#If is ok append it
                    self.segments.append(segment1)
                elif segment2_ok and segment1_ok == False:#If is ok append it
                    self.segments.append(segment2)
                #else nothing

                #otherwise do nothing
                #and continue the cycle
            else:
                #If is not ok we get all the possible and available edges. So return segments
                return self.segments

    def get_coords_of_opposite_directions(self,i,j):
        t_coords = []
        for t_corresp in ARR_CORRESP:
            t_x = i + t_corresp[0]
            t_y = j + t_corresp[1]
            if t_x >= 0 and t_y >= 0 and t_x < self.edges.shape[0] and t_y < self.edges.shape[1]:
                if self.edges[t_x,t_y] != 0 and self.EdgeManager.is_edge_available(t_x,t_y):#if there is an edge in that position
                    t_coords.append(t_corresp)#append coordinates

        possible_combinations = list(itertools.combinations(t_coords,2))
        max_distance = 0
        final_coord_1 = (0,0)
        final_coord_2 = (0,0)
        for pcomb in possible_combinations:
            c1 = pcomb[0]
            c2 = pcomb[1]
            dist = np.sqrt((c2[0] - c1[0])**2 +(c2[1] - c1[1])**2)
            if max_distance < dist:
                max_distance = dist
                final_coord_1 = (c1[0],c1[1])
                final_coord_2 = (c2[0],c2[1])
        final_coord_1 = (final_coord_1[0] + i, final_coord_1[1] + j)
        final_coord_2 = (final_coord_2[0] + i, final_coord_2[1] + j)
        return (final_coord_1,final_coord_2)

    def get_segments(self):
        return self.segments

    def get_segmented_image(self, shape):
        newimg = np.zeros((shape[0],shape[1],3),dtype="uint8")
        for segment in self.segments:
            color1 = (rnd.randint(0, 255),rnd.randint(0, 255),rnd.randint(0, 255))
            for node in segment.get_nodes():
                newimg[node[0],node[1]] = color1
        return newimg

    def get_total_pixel_count(self):
        count = 0
        for segment in self.segments:
            count += len(segment.get_nodes())
        return count