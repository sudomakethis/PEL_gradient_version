import numpy as np
import random as rnd

class Phase4:
    def __init__(self, segments, ) -> None:
        self.segments = segments

    def thin_segments(self,min_length):
        contin = True
        last_i = 0
        size = len(self.segments)
        while contin:
            contin,last_i,size = self.private_thin_segments(last_i, size, min_length)

    def private_thin_segments(self,from_i,size,min_length):
        for i in range(from_i,size):
            if len(self.segments[i].get_nodes()) < min_length:
                self.segments = np.delete(self.segments,i)
                return (True,i,size-1)
        return (False,None,None)
    
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