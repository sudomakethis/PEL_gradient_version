import numpy as np
import random as rnd
import dip

class Phase3:
    def __init__(self, ES, BEM):
        self.JES = ES
        self.num_segms_init = len(ES)
        self.BEMJ = np.zeros((BEM.shape[0], BEM.shape[1], 3), dtype="uint8")
        self.T = []
        self.get_T(ES)
        self.C = []
        self.join_count = 0
        self.prune_count = 0
    
    def get_T(self, ES):
        self.T = []
        for i in range(len(ES)):
            self.T.append([ES[i][0], ES[i][-1]])

    def Algo(self, show = False):
        self.get_C()
        self.parse_C()
        self.JES = [segm for segm in self.JES if segm is not None]
        self.prune_cyclic_segments()
        self.BEMJ = self.get_segmented_image(self.JES, self.BEMJ)
        if show:
            dip.show_image(
                        image = self.BEMJ,
                        title = "Joined Segmented Edge Map")
            num_segms = len(self.JES)
            print("Number of Initial Segments:", self.num_segms_init)
            print("Number of Joined Segments:", self.join_count)
            print("Number of Cyclic Segments Pruned:", self.prune_count)
            print("Final Number of Segments:", num_segms)
        return self.JES, self.BEMJ

    def get_C(self):
        for i in range(0, len(self.T)-1):
            for j in range(i+1, len(self.T)):
                for k in range(4):
                    m = k // 2
                    n = k % 2
                    if self.DCheck(5, self.T[i][m],
                                      self.T[j][n]):
                        self.C.append([i,j])
                        break

    def parse_C(self):
        for couple in self.C:
            match = False
            if couple[0] == couple[1]:
                continue
            pixel_couple = [self.T[couple[0]], self.T[couple[1]]]
            tips = [item for segm_tips in pixel_couple for item in segm_tips]
            for index, tip in enumerate(tips):
                idx = 1 - (index // 2)
                L = max(min(5,len(self.JES[couple[idx]])),1)
                for edgel in range(-L, L):
                    if self.DCheck(1, tip, self.JES[couple[idx]][edgel]):
                        subj, obj = self.join(couple, index, idx, edgel)
                        self.join_count += 1
                        match = True
                        self.update_C(subj, obj)
                        self.update_T(subj, obj)
                        break
                if match:
                    break

    def join(self, couple, index, idx, edgel):
        if edgel >= 0:
            self.JES[couple[idx]] = self.JES[couple[idx]][edgel:]
            if index % 2 == 0:
                self.JES[couple[1 - idx]].reverse()
            self.JES[couple[1 - idx]].extend(self.JES[couple[idx]])
            self.JES[couple[idx]] = None
            subj = couple[1 - idx]
            obj = couple[idx]
        else:
            self.JES[couple[idx]] = self.JES[couple[idx]][:edgel + 1]
            if index % 2 == 1:
                self.JES[couple[1 - idx]].reverse()
            self.JES[couple[idx]].extend(self.JES[couple[1 - idx]])
            self.JES[couple[1 - idx]] = None
            subj = couple[idx]
            obj = couple[1 - idx]
        return subj, obj
    
    def update_C(self, subj, obj):
        for item in self.C:
                if item[0] == obj:
                    item[0] = subj
                if item[1] == obj:
                    item[1] = subj
    
    def update_T(self, subj, obj):
        self.T[subj] = [self.JES[subj][0], 
                        self.JES[subj][-1]]
        self.T[obj]  = [self.JES[subj][0], 
                        self.JES[subj][-1]]
        
    def prune_cyclic_segments(self):
        for segm in self.JES:
            pruned = False
            L = max(min(5,len(segm)),1)
            for i in range(L):
                for j in range(L):
                    if self.DCheck(1, segm[i], segm[-j-1]):
                        segm = segm[i:-j]
                        self.prune_count += 1
                        pruned = True
                        break
                if pruned:
                    break

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
    
dip.WizardFamiliar("Phase 3!")