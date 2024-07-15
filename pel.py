
#######     ########   ##
##     ##   ##         ##
##     ##   ##         ##
#######     ########   ##
##          ##         ##
##          ##         ##
##          ########   #########
import pandas as pd
import numpy as np
import cv2
import dip
import os
import random as rnd
from Clock import Clock
from Phase00 import Phase0, Phase0Gradient
from Phase01 import Phase1, Phase1Gradient
from Phase02 import Phase2, Phase2Gradient
from Phase03 import Phase3
from Phase04 import Phase4
from Evaluation import Evaluation


MIN_LENGTH = 8

### SETUP
def pelBase(data_dir, file_name, timer, show = False):
    parent_dir = os.path.dirname(__file__)
    folder_path = parent_dir + data_dir
    file_path = folder_path + file_name

    ### PHASE 0 - GET IMAGE AND BINARY EDGE MAP

    phase0 = Phase0()
    im, BEM = phase0.Algo(path = file_path, 
                        show_im = show,
                        show_BEM = show)
    timer.flag(name = 'Phase 0')

    ### PHASE 1 - FILL GAPS

    phase1 = Phase1(BEM)
    BEMF = phase1.Algo(show = show)
    timer.flag(name = 'Phase 1')


    ### PHASE 2 - CREATE SEGMENTS

    phase2 = Phase2(BEMF)
    seed = rnd.randint(0,65535)
    ES, BEMS = phase2.Algo(seed = seed, 
                        show = show)
    timer.flag(name = 'Phase 2')
    
    ### PHASE 3 - JOIN SEGMENTS

    phase3 = Phase3(ES, BEMS)
    JES, BEMJ = phase3.Algo(show = show)
    timer.flag(name = 'Phase 3')

    ### PHASE 4 - THINNING SEGMENTS

    phase4 = Phase4(JES, BEMJ)
    TES, BEMT = phase4.Algo(min_length = MIN_LENGTH, show = show)
    timer.flag(name = 'Phase 4')

    store(folder_path, file_name, BEMF, BEMS, BEMJ, BEMT)

    return BEMT

def pelModificato(data_dir, file_name, timer, show = False):
    parent_dir = os.path.dirname(__file__)  
    folder_path = parent_dir + data_dir
    file_path = folder_path + file_name

    ### PHASE 0 
    phase0 = Phase0Gradient()
    im1, BEM, G, Theta = phase0.Algo(path = file_path, 
                        show_im = show,
                        show_BEM = show)
    timer.flag(name = 'Phase 0')

    ### PHASE 1

    phase1 = Phase1Gradient(BEM, G, Theta)
    BEMF = phase1.Algo(show = show)
    timer.flag(name = 'Phase 1')

    ### PHASE 2 - CREATE SEGMENTS Variante gradiente

    phase2 = Phase2Gradient(BEMF, G, Theta)
    seed = rnd.randint(0,65535)
    ES, BEMS = phase2.Algo(seed = seed, 
                        show = show)
    timer.flag(name = 'Phase 2')

    ### PHASE 3 - JOIN SEGMENTS Variante gradiente

    phase3 = Phase3(ES, BEMS)
    JES, BEMJ = phase3.Algo(show = show)
    timer.flag(name = 'Phase 3')

    ### PHASE 4 - THINNING SEGMENTS Variante gradiente

    phase4 = Phase4(JES, BEMJ)
    TES, BEMT = phase4.Algo(min_length = MIN_LENGTH, show = show)
    timer.flag(name = 'Phase 4')

    store(folder_path+'\\Gradiente', file_name, BEMF, BEMS, BEMJ, BEMT)

    return BEMT

def store(folder_path, file_name, BEMF, BEMS, BEMJ, BEMT):
    # CREATE FOLDER TO STORE RESULTS
    image_name = os.path.splitext(file_name)[0]
    res_dir = folder_path + "\\" + image_name + "\\"
    os.makedirs(name = res_dir,
                exist_ok = True)
    # PHASE 1 RESULT
    colored_BEMF = cv2.applyColorMap(src = BEMF,
                                    colormap = cv2.COLORMAP_JET)
    cv2.imwrite(filename = res_dir + image_name + "_BEMF.png",
                img = colored_BEMF)
    # PHASE 2 RESULT
    colored_BEMS = cv2.applyColorMap(src = BEMS,
                                    colormap = cv2.COLORMAP_JET)
    cv2.imwrite(filename = res_dir + image_name + "_BEMS.png",
                img = colored_BEMS)
    # PHASE 3 RESULTS
    colored_BEMJ = cv2.applyColorMap(src = BEMJ,
                                    colormap = cv2.COLORMAP_JET)
    cv2.imwrite(filename = res_dir + image_name + "_BEMJ.png",
                img = colored_BEMJ)
    # PHASE 4 RESULT
    colored_BEMT = cv2.applyColorMap(src = BEMT,
                                    colormap = cv2.COLORMAP_JET)
    cv2.imwrite(filename = res_dir + image_name + "_BEMT.png",
                img = colored_BEMT)


def execute(data_dir, file_name, pel=pelBase):
    timer = Clock()
    BEMT = pel(data_dir, file_name, timer, show=False)

    ### RESULTS
    print(pel)
    print("\nTime Table: [ms]")
    timer.table(mode = "inc")

    parent_dir = os.path.dirname(__file__)  
    folder_path = parent_dir + data_dir
    file_path = folder_path + file_name.split(".")[0] + "_bem.png"
    BEM_human = cv2.imread(filename = file_path, flags = cv2.IMREAD_GRAYSCALE)
    BEMT = cv2.cvtColor(BEMT, cv2.COLOR_BGR2GRAY)
    BEM_algo = np.where(BEMT == 14, 0, BEMT) # put 0 as background, because PEL background in greyscale is 14
    
    return timer.getAllTimes() | eval(BEM_algo, BEM_human) | {'file': file_name.split('.')[0], 'pel': pel.__name__}

def eval(BEM1, BEM2):
    results = {}

    results['f_score'] = Evaluation.f_score(BEM1, BEM2)
    results['mse'] = Evaluation.mse(BEM1, BEM2)
    results['epe'] = Evaluation.epe(BEM1, BEM2)
    results['accuracy'] = Evaluation.accuracy(BEM1, BEM2)
    results['jaccard'] = Evaluation.jaccard(BEM1, BEM2)

    return results

data_dir = "\\Data\\"
# file_name = "lena.png"
for i in range(5):
    #images = ["lena.png", "apartment.png", "birds.png", 'cityscapes.png', 'kitchen.png', 'rose.png', 'saint.png', 'worm.png']
    images = ["lena.png"]
    results = []
    for file_name in images:
        results.append(execute(data_dir, file_name, pelModificato))
        results.append(execute(data_dir, file_name, pelBase))

    results = pd.DataFrame(results)
    print(results)
    results.to_csv(os.path.dirname(__file__) + '\\results.csv', mode='a', header=False, index=False)

dip.WizardFamiliar("PEL!")