import numpy as np
import random as rnd
import dip
from collections import deque

class Phase4:
    def __init__(self, ES, BEM):
        self.TES = deque(ES)
        self.BEMT = np.zeros((BEM.shape[0],BEM.shape[1],3), dtype="uint8")
        self.num_segms_init = len(ES)

    def Algo(self, min_length = 8, show = False):
        self.TES = self.thinning_segments(self.TES)
        self.TES = self.prune_short_segments(self.TES, min_length)
        self.BEMT = self.get_segmented_image(self.TES, self.BEMT)
        if show:
            dip.show_image(image = self.BEMT,
                    title = "Thinned Edge Map")
            print("Number of Initial Segments:", self.num_segms_init)
            print("Number of Short Segments Eliminated:", 
                   self.num_segms_init - len(self.TES))
            print("Final Number of Segments:", len(self.TES))
        return list(self.TES), self.BEMT
    
    def thinning_segments(self, ES):
        for segm in ES:
            idx = len(segm) - 1
            while idx >= 2:
                if self.DCheck(1, segm[idx - 2], segm[idx]):
                    segm.remove(segm[idx - 1])
                    idx -= 1
                idx -= 1
        return ES
    
    def prune_short_segments(self, ES, min_length = 8):
        ES = [segm for segm in ES if len(segm) >= min_length]
        return ES
    
    def DCheck(self, radius, x, y):
        return (abs(x[0]-y[0]) <= radius and
                abs(x[1]-y[1]) <= radius)

    def get_segmented_image(self, ES, BEM):
        for segment in ES:
            color = (rnd.randint(0, 255),
                     rnd.randint(0, 255),
                     rnd.randint(0, 255))
            for node in segment:
                BEM[node] = color
        return BEM

dip.WizardFamiliar("Phase 4!")