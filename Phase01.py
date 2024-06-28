import numpy as np
import dip

EDGEL = 255
NODGEL = 0


class Phase1:
    def __init__(self, BEM, G = None, theta=None):

        #Self variabile di python che richiamo oggetto(Tipo this in java)
        self.BEMF = np.copy(BEM)

        #Conta gli edge
        self.num_edgels_init = np.count_nonzero(BEM == 255)

        self.fill_count = 0

        self.G = G
        self.theta = theta


        self.checks = ["check1", "check2", "check3"]

        #Contorno di un punto, ovvero i vicini
        self.neighbourhood = [(-1,-1),(-1, 0),(-1,+1),
                              ( 0,-1),        ( 0,+1),
                              (+1,-1),(+1, 0),(+1,+1)]
        
        #Per ogni vicino, vengono trovati i possibili candidati da riempire
        #Si parte da un quadrato 3*3 e si valuta per ogni quadrato i candidati e i controlli tramite i check
        self.filler = [
                {
                    "forelast": [(-1,-1)],
                    "candidate":[(1,1),(0,1),(1,0)],
                    "check1": [(2,2),(2,1),(1,2)],
                    "check2": [(0,2)],
                    "check3": [(2,0)]
                },{
                    "forelast": [(-1,0)],
                    "candidate":[(1,0),(1,-1),(1,1)],
                    "check1": [(2,0)],
                    "check2": [(2,-1),(2,-2),(1,-2)],
                    "check3": [(2,1),(2,2),(1,2)]
                },{
                    "forelast": [(-1,1)],
                    "candidate":[(1,-1),(1,0),(0,-1)],
                    "check1": [(2,-2),(1,-2),(2,-1)],
                    "check2": [(2,0)],
                    "check3": [(0,-2)]
                },{
                    "forelast": [(0,-1)],
                    "candidate":[(0,1),(1,1),(-1,1)],
                    "check1": [(0,2)],
                    "check2": [(1,2),(2,2),(2,1)],
                    "check3": [(-1,2),(-2,2),(-2,1)]
                },{
                    "forelast": [(0,1)],
                    "candidate":[(0,-1),(1,-1),(-1,-1)],
                    "check1": [(0,-2)],
                    "check2": [(1,-2),(2,-2),(2,-1)],
                    "check3": [(-1,-2),(-2,-2),(-2,-1)]
                },{
                    "forelast": [(1,-1)],
                    "candidate":[(-1,1),(0,1),(-1,0)],
                    "check1": [(-2,2),(-2,1),(-1,-2)],
                    "check2": [(0,2)],
                    "check3": [(-2,0)]
                },{
                    "forelast": [(1,0)],
                    "candidate":[(-1,0),(-1,-1),(-1,1)],
                    "check1": [(-2,0)],
                    "check2": [(-2,-1),(-2,-2),(-1,-2)],
                    "check3": [(-2,1),(-2,2),(-1,2)]
                },{
                    "forelast": [(1,1)],
                    "candidate":[(-1,-1),(-1,0),(0,-1)],
                    "check1": [(-2,-2),(-2,-1),(-1,-2)],
                    "check2": [(-2,0)],
                    "check3": [(0,-2)]
                }
            ]
    
    #Creo un array di 8 elementi, da pi/8,2pi/8,....,pi
    def initCondition(self):
        self.COND = np.pi/8 * np.arange(1, 9)

    # O(n^2 * (8+8+8+3+3*3) ) = O(n^2 * 36)
    def Algo(self, show = False):

        #Senza -2 cercherei celle che non ci sono, parto da 2 per lo stesso motivo
        for i in range(2, self.BEMF.shape[0]-2): 
            
            for j in range(2, self.BEMF.shape[1]-2):

                #Se è un bordo e se solo uno dei vicini è un bordo
                if ((self.BEMF[i,j] != NODGEL) and
                    (sum([self.BEMF[i + x, j + y] != NODGEL for x, y in self.neighbourhood]) == 1)):

                #Trova l'indice del primo pixel che ha valore diverso da 0 
                    recipe_num = [idx for idx, (x,y) in enumerate(self.neighbourhood)
                                  if self.BEMF[i + x, j + y] != NODGEL][0]
                    
                #Estra il filler di quello che ha trovato come border e fa un dizionario
                    recipe = dict(self.filler[recipe_num])
                    for key, value in recipe.items():
                        recipe[key] = [(i + x, j + y) for x, y in value] # Trasforma le coordinate da relative ad assolute
                
                #Se il forelast è considerato bordo e tutti i candidati sono non bordi, se non lo è non ha sens
                    if (any([self.BEMF[x, y] != NODGEL for x, y in recipe["forelast"]]) and
                        all([self.BEMF[x, y] == NODGEL for x, y in recipe["candidate"]])):

                #Se almeno un pixel nel check è diverso da NODGEL, metti vero e poi aggiorni il pixel come EDGEL 
                        for check in self.checks:
                            if next((True for x, y in recipe[check] if self.BEMF[x, y] != NODGEL), False):
                                self.BEMF[recipe["candidate"][self.checks.index(check)]] = EDGEL
                                self.fill_count += 1
                                break
        if show:
            dip.show_image(
                        image = self.BEMF,
                        title = "Filled Binary Edge Map")
            print("Number of Initial Edgels:", self.num_edgels_init)
            print("Number of Pixels Filled:", self.fill_count)
            print("Final Number of Edgels:", np.count_nonzero(self.BEMF == 255))
        return self.BEMF
    
class Phase1Gradient:
    def __init__(self, BEM, G, theta):
        self.BEMF = np.copy(BEM)
        self.num_edgels_init = np.count_nonzero(BEM == 255)
        self.fill_count = 0
        self.G = G
        self.theta = theta
        self.checks = ["check1", "check2", "check3"]
        self.neighbourhood = [(-1,-1),(-1, 0),(-1,+1),
                              ( 0,-1),        ( 0,+1),
                              (+1,-1),(+1, 0),(+1,+1)]
        self.filler2 = {
            400: {
                    'candidate': [(0,1),(-1,1)],
                    "check1": [(0,2)],
                    "check2": [(-1,2),(-2,2),(-2,1)]
            },
            410: {
                    'candidate': [(0,1),(-1,1)],
                    "check1": [(0,2)],
                    "check2": [(-1,2),(-2,2),(-2,1)]
            },
            420: {
                    'candidate': [(0,1),(-1,1)],
                    "check1": [(0,2)],
                    "check2": [(-1,2),(-2,2),(-2,1)]
            },
            402: {
                    'candidate': [(0,-1),(1,-1)],
                    "check1": [(0,-2)],
                    "check2": [(1,-2),(2,-2),(2,-1)]
            },
            412: {
                    'candidate': [(0,-1),(1,-1)],
                    "check1": [(0,-2)],
                    "check2": [(1,-2),(2,-2),(2,-1)]
            },
            422: {
                    'candidate': [(0,-1),(1,-1)],
                    "check1": [(0,-2)],
                    "check2": [(1,-2),(2,-2),(2,-1)]
            },
            401: {
                    'candidate': [(1,-1)],
                    'check1': [(1,-2),(2,-2),(2,-1)]
            },
            421: {
                    'candidate': [(-1,1)],
                    'check1': [(-1,2),(-2,2),(-2,1)]
            },
            500:{
                    'candidate': [(-1,1),(0,1)],
                    "check1": [(-2,2),(-1,2),(-2,1)],
                    "check2": [(0,2)]
            },
            510:{
                    'candidate': [(-1,1),(0,1)],
                    "check1": [(-2,2),(-1,2),(-2,1)],
                    "check2": [(0,2)]
            },
            520:{
                    'candidate': [(-1,1),(0,1)],
                    "check1": [(-2,2),(-1,2),(-2,1)],
                    "check2": [(0,2)]
            },
            502:{
                    'candidate': [(1,-1),(0,-1)],
                    "check1": [(2,-2),(1,-2),(2,-1)],
                    "check2": [(0,-2)]
            },
            512:{
                    'candidate': [(1,-1),(0,-1)],
                    "check1": [(2,-2),(1,-2),(2,-1)],
                    "check2": [(0,-2)]
            },
            522:{
                    'candidate': [(1,-1),(0,-1)],
                    "check1": [(2,-2),(1,-2),(2,-1)],
                    "check2": [(0,-2)]
            },
            501:{
                    'candidate': [(1,-1)],
                    'check1': [(2,-2),(1,-2),(2,-1)]
            },
            521:{
                    'candidate': [(-1,1)],
                    'check1': [(-1,2),(-2,2),(-2,1)]
            },
            600:{
                    'candidate': [(1,-1),(1,0)],
                    "check2": [(2,-2),(2,-1),(1,-2)],
                    "check1": [(2,0)]
            },
            601:{
                    'candidate': [(1,-1),(1,0)],
                    "check2": [(2,-2),(2,-1),(1,-2)],
                    "check1": [(2,0)]
            },
            602:{
                    'candidate': [(1,-1),(1,0)],
                    "check2": [(2,-2),(2,-1),(1,-2)],
                    "check1": [(2,0)]
            },
            620:{
                    'candidate': [(-1,1),(-1,0)],
                    "check2": [(-2,2),(-2,1),(-1,2)],
                    "check1": [(-2,0)]
            },
            621:{
                    'candidate': [(-1,1),(-1,0)],
                    "check2": [(-2,2),(-2,1),(-1,2)],
                    "check1": [(-2,0)]
            },
            622:{
                    'candidate': [(-1,1),(-1,0)],
                    "check2": [(-2,2),(-2,1),(-1,2)],
                    "check1": [(-2,0)]
            },
            610:{
                    'candidate': [(-1,1)],
                    'check1': [(-2,2),(-2,1),(-1,2)]
            },
            612:{
                    'candidate': [(1,-1)],
                    'check1': [(2,-2),(2,-1),(1,-2)]
            },
            700:{
                    'candidate': [(1,0),(1,-1)],
                    "check1": [(2,0)],
                    "check2": [(2,-1),(2,-2),(1,-2)]
            },
            701:{
                    'candidate': [(1,0),(1,-1)],
                    "check1": [(2,0)],
                    "check2": [(2,-1),(2,-2),(1,-2)]
            },
            702:{
                    'candidate': [(1,0),(1,-1)],
                    "check1": [(2,0)],
                    "check2": [(2,-1),(2,-2),(1,-2)]
            },
            720:{
                    'candidate': [(-1,0),(-1,1)],
                    "check2": [(-2,0)],
                    "check1": [(-2,1),(-2,2),(-1,2)]
            },
            721:{
                    'candidate': [(-1,0),(-1,1)],
                    "check2": [(-2,0)],
                    "check1": [(-2,1),(-2,2),(-1,2)]
            },
            722:{
                    'candidate': [(-1,0),(-1,1)],
                    "check2": [(-2,0)],
                    "check1": [(-2,1),(-2,2),(-1,2)]
            },
            710:{
                    'candidate': [(-1,1)],
                    'check1': [(-2,1),(-2,2),(-1,2)]
            },
            712:{
                    'candidate': [(1,-1)],
                    'check1': [(2,-1),(2,-2),(1,-2)]
            },
            0:{
                    'candidate': [(0,1),(1,1)],
                    "check1": [(0,2)],
                    "check2": [(2,1),(2,2),(1,2)]
            },
            1:{
                    'candidate': [(0,1),(1,1)],
                    "check1": [(0,2)],
                    "check2": [(2,1),(2,2),(1,2)]
            },
            2:{
                    'candidate': [(0,1),(1,1)],
                    "check1": [(0,2)],
                    "check2": [(2,1),(2,2),(1,2)]
            },
            20:{
                    'candidate': [(0,-1),(-1,-1)],
                    "check2": [(0,-2)],
                    "check1": [(-2,-1),(-2,-2),(-1,-2)]
            },
            21:{
                    'candidate': [(0,-1),(-1,-1)],
                    "check2": [(0,-2)],
                    "check1": [(-2,-1),(-2,-2),(-1,-2)]
            },
            22:{
                    'candidate': [(0,-1),(-1,-1)],
                    "check2": [(0,-2)],
                    "check1": [(-2,-1),(-2,-2),(-1,-2)]
            },
            10:{
                    'candidate': [(1,1)],
                    'check1': [(2,2),(2,1),(1,2)]
            },
            12:{
                    'candidate': [(-1,-1)],
                    'check1': [(-2,-1),(-2,-2),(-1,-2)]
            },
            100:{
                    'candidate': [(1,1),(1,0)],
                    "check1": [(2,2),(1,2),(2,1)],
                    "check2": [(2,0)],
            },
            101:{
                    'candidate': [(1,1),(1,0)],
                    "check1": [(2,2),(1,2),(2,1)],
                    "check2": [(2,0)],
            },
            102:{
                    'candidate': [(1,1),(1,0)],
                    "check1": [(2,2),(1,2),(2,1)],
                    "check2": [(2,0)],
            },
            120:{
                    'candidate': [(-1,-1),(-1,0)],
                    "check2": [(-2,-2),(-2,-1),(-1,-2)],
                    "check1": [(-2,0)]
            },
            121:{
                    'candidate': [(-1,-1),(-1,0)],
                    "check2": [(-2,-2),(-2,-1),(-1,-2)],
                    "check1": [(-2,0)]
            },
            122:{
                    'candidate': [(-1,-1),(-1,0)],
                    "check2": [(-2,-2),(-2,-1),(-1,-2)],
                    "check1": [(-2,0)]
            },
            110:{
                    'candidate': [(1,1)],
                    'check1': [(2,2),(2,1),(1,2)]
            },
            112:{
                    'candidate': [(-1,-1)],
                    'check1': [(-2,-2),(-2,-1),(-1,-2)]
            },
            200:{
                    'candidate': [(1,1),(0,1)],
                    "check1": [(2,2),(1,2),(2,1)],
                    "check2": [(0,2)]
            },
            210:{
                    'candidate': [(1,1),(0,1)],
                    "check1": [(2,2),(1,2),(2,1)],
                    "check2": [(0,2)]
            },
            220:{
                    'candidate': [(1,1),(0,1)],
                    "check1": [(2,2),(1,2),(2,1)],
                    "check2": [(0,2)]
            },
            202:{
                    'candidate': [(-1,-1),(0,-1)],
                    "check1": [(-2,-2),(-1,-2),(-2,-1)],
                    "check2": [(0,-2)]
            },
            212:{
                    'candidate': [(-1,-1),(0,-1)],
                    "check1": [(-2,-2),(-1,-2),(-2,-1)],
                    "check2": [(0,-2)]
            },
            222:{
                    'candidate': [(-1,-1),(0,-1)],
                    "check1": [(-2,-2),(-1,-2),(-2,-1)],
                    "check2": [(0,-2)]
            },
            201:{
                    'candidate': [(1,1)],
                    'check1': [(2,2),(1,2),(2,1)]
            },
            221:{
                    'candidate': [(-1,-1)],
                    'check1': [(-2,-2),(-1,-2),(-2,-1)]
            },
            300:{
                    'candidate': [(0,1),(1,1)],
                    "check1": [(0,2)],
                    "check2": [(1,2),(2,2),(2,1)]
            },
            310:{
                    'candidate': [(0,1),(1,1)],
                    "check1": [(0,2)],
                    "check2": [(1,2),(2,2),(2,1)]
            },
            320:{
                    'candidate': [(0,1),(1,1)],
                    "check1": [(0,2)],
                    "check2": [(1,2),(2,2),(2,1)]
            },
            302:{
                    'candidate': [(0,-1),(-1,-1)],
                    "check2": [(0,-2)],
                    "check1": [(-1,-2),(-2,-2),(-2,-1)]
            },
            312:{
                    'candidate': [(0,-1),(-1,-1)],
                    "check2": [(0,-2)],
                    "check1": [(-1,-2),(-2,-2),(-2,-1)]
            },
            322:{
                    'candidate': [(0,-1),(-1,-1)],
                    "check2": [(0,-2)],
                    "check1": [(-1,-2),(-2,-2),(-2,-1)]
            },
            301:{
                    'candidate': [(0,1)],
                    'check1': [(0,2),(1,2)]
            },
            321:{
                    'candidate': [(0,-1)],
                    'check1': [(0,-2),(-1,-2)]
            },
        }
        self.initCondition()
    
    def initCondition(self):
        self.COND = np.pi/8 * np.arange(1, 9) - np.pi/2

    def selectNeighbourhood2(self, i, j, a, b):
        t = 0
        for it in range(8):
            if self.theta[i,j] < 0 : theta = self.theta[i,j] + np.pi
            else : theta = self.theta[i,j] - np.pi
            if theta <= self.COND[it]: 
                t = it
                break       
        id = t * 100 + (a + 1) * 10 + (b + 1)
        return self.filler2[id]
      
    ## return the coordinates of the edgel if only one is found in the neighbourhood
    # O(8)
    def count(self, i, j):
        a, b = None, None
        for x, y in self.neighbourhood:
            if self.BEMF[i + x, j + y] != NODGEL:
                if a is None:
                    a, b = x, y
                else:
                    return None, None
        return a, b

    # O(n^2) * (O(8) + O(9) + O(2) + O(3) + O(2) * O(3) = O(n^2 * 28)
    def Algo(self, show = False):
        for i in range(2, self.BEMF.shape[0]-2):
            for j in range(2, self.BEMF.shape[1]-2):
                if (self.BEMF[i,j] != NODGEL): 
                    a, b = self.count(i, j)
                    if a is not None:
                        recipe = dict(self.selectNeighbourhood2(i, j, a, b))
                        for key, value in recipe.items():
                            recipe[key] = [(i + x, j + y) for x, y in value] # passo da coordinate relative a coordinate assolute
                        if (all([self.BEMF[x, y] == NODGEL for x, y in recipe["candidate"]])):
                            counter=0
                            for check in self.checks:
                                if(counter==len(recipe["candidate"])):
                                    break
                                counter += 1
                                if next((True for x, y in recipe[check] if self.BEMF[x, y] != NODGEL), False):
                                    self.BEMF[recipe["candidate"][self.checks.index(check)]] = EDGEL
                                    self.fill_count += 1
                                    break
        if show:
            dip.show_image(
                        image = self.BEMF,
                        title = "Filled Binary Edge Map - Gradient")
            print("Number of Initial Edgels:", self.num_edgels_init)
            print("Number of Pixels Filled:", self.fill_count)
            print("Final Number of Edgels:", np.count_nonzero(self.BEMF == 255))
        return self.BEMF
    
dip.WizardFamiliar("Phase 1!")