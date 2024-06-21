import numpy as np

class Evaluation:
    def f_score(algo, human):

        algo_map = np.where(algo != 0, 1, 0) # +1 = edge, 0 = non_edge

        human_map = np.where(human != 0, 1, -1) # +1 = edge, -1 = non_edge
        
        true_positive = np.argwhere((algo_map - human_map) == 0)
        true_negative = np.argwhere((algo_map - human_map) == 1)
        false_positive = np.argwhere((algo_map - human_map) == 2)
        false_negative = np.argwhere((algo_map - human_map) == -1)

        TP = len(true_positive)
        # print("TP = ", TP)
        FP = len(false_positive)
        # print("FP = ", FP)
        FN = len(false_negative)
        # print("FN = ", FN)
        TN = len(true_negative)
        # print("TN = ", TN)

        P = TP/(TP+FP)  # precision
        R = TP/(TP+FN)  # recall
        F_score = (2*P*R)/(P+R)

        '''BEM_FP = np.where((algo_map - human_map) == 2, 255, 0)
        dip.show_image(image = BEM_FP, title = "Binary Edge Map FP", info = False)

        BEM_TP = np.where((algo_map - human_map) == 0, 255, 0)
        dip.show_image(image = BEM_TP, title = "Binary Edge Map TP", info = False)

        BEM_FN = np.where((algo_map - human_map) == -1, 255, 0)
        dip.show_image(image = BEM_FN, title = "Binary Edge Map FN", info = False)

        BEM_TN = np.where((algo_map - human_map) == 1, 255, 0)
        dip.show_image(image = BEM_TN, title = "Binary Edge Map TN", info = False)'''

        return F_score

    def accuracy(algo, human):

        algo_map = np.where(algo != 0, 1, 0) # +1 = edge, 0 = non_edge

        human_map = np.where(human != 0, 1, -1) # +1 = edge, -1 = non_edge

        h = algo_map.shape[0]
        w = algo_map.shape[1]
        
        true_positive = np.argwhere((algo_map - human_map) == 0)
        true_negative = np.argwhere((algo_map - human_map) == 1)

        TP = len(true_positive)
        TN = len(true_negative)

        acc = (TP + TN)/(h*w)

        return acc
    
    def jaccard(algo, human):

        algo_map = np.where(algo != 0, 1, 0) # +1 = edge, 0 = non_edge

        human_map = np.where(human != 0, 1, -1) # +1 = edge, -1 = non_edge
        
        true_positive = np.argwhere((algo_map - human_map) == 0)
        false_positive = np.argwhere((algo_map - human_map) == 2)
        false_negative = np.argwhere((algo_map - human_map) == -1)

        TP = len(true_positive)
        FP = len(false_positive)
        FN = len(false_negative)

        jac_index = TP / (TP + FP + FN)
        jac_distance = 1.0 - jac_index

        return jac_distance
    
    def mse(algo, human):

        algo_map = np.where(algo != 0, 1, 0) # +1 = edge, 0 = non_edge
        human_map = np.where(human != 0, 1, 0) # +1 = edge, 0 = non_edge

        h = algo_map.shape[0]
        w = algo_map.shape[1]
        diff = human_map - algo_map
        value = np.sum(np.power(diff,2))/(h*w)
        
        return value
    
    # Edge Position Error
    # EPE = average distance of the edge pixels in the algo_map to the nearest edge pixel in the human_map
    def epe(algo, human):

        algo_map = np.where(algo != 0, 1, 0) # +1 = edge, 0 = non_edge
        human_map = np.where(human != 0, 1, 0) # +1 = edge, 0 = non_edge

        h = algo_map.shape[0]
        w = algo_map.shape[1]
        
        labelled = np.where(algo_map != 0)
        distances = np.zeros(len(labelled[0]))

        for k in range(len(labelled[0])):
            i = labelled[0][k]
            j = labelled[1][k]

            if human_map[i,j] == 1:
                distances[k] == 0
            else:
                stop = False
                radius = 1
                while stop == False:
                    detected = np.where(human_map[max(0,i-radius):min(i+1+radius,h) , max(0,j-radius):min(j+1+radius,w)] != 0)
                    if(len(detected[0])!=0):
                        stop = True
                    else:
                        radius += 1
                distances[k] = radius
        
        value = np.sum(distances) / len(distances)

        return value