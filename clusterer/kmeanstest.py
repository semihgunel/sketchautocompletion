import numpy as np
from getConstraints import *
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from random import randint
import copy
import matplotlib.markers as mark
from cudackmeans import *
sys.path.append("../../sketchfe/sketchfe")
sys.path.append('../predict/')
sys.path.append('../clusterer/')
sys.path.append('../classifiers/')
sys.path.append('../test/')
sys.path.append('../data/')
from extractor import *
from FileIO import *
from Predictor import *
from visualise import *
import random
def visualiseAfterClustering(out, features, classId, centers, isFull, title, sv):
    def getMarkerList():
        numClass = len(set(classId))
        marker_list = list(mark.MarkerStyle.filled_markers)
        markIndex = 4
        while numClass >= len(marker_list):
            marker_list.append((markIndex,1))
            markIndex+=1

        return marker_list
    clisEdge = ['black', 'yellow', 'red', 'blue']
    colorList = cm.rainbow(np.linspace(0, 1, len(out[0])))
    features = np.transpose(features)
    fig1 = plt.figure()
    fig1.canvas.set_window_title(str(title))
    ax1 = fig1.add_subplot(111)

    fig2 = plt.figure()
    fig2.canvas.set_window_title("K="+str(title) + " Full Sketch")
    ax2 = fig2.add_subplot(111)

    centers = np.asarray(centers).astype(int)
    colorList = cm.rainbow(np.linspace(0, 1, len(out[0])))
    #print len(centers[0])
    for i in range(len(centers[0])):
         ax1.scatter(centers[0][i], centers[1][i], c='#000000', s=300,
                    alpha=0.5, edgecolors='black')
    index = 0
    marker_list = getMarkerList()

    count = 0
    for cluster in out[0]:
        index+=1
        color = colorList[index-1]
        ax1.scatter(out[1][index-1][0], out[1][index-1][1], c='red', s=300, label=color,
                    alpha=0.5, edgecolors='black')

        color = colorList[index - 1]
        edgecolor = colorList[random.randint(0, len(clisEdge)) - 1]

        for i in cluster.astype(int):

            x = features.tolist()[i]
            scale = 80
            marker = classId[i]

            ax1.scatter(x[0], x[1], c=color, s=scale, label=color,
                alpha=0.5, edgecolors=edgecolor, marker= marker_list[marker],linewidth='2')

            if(isFull[i] == 1):
                count += 1
                ax2.scatter(x[0], x[1], c=color, s=scale, label=color,
                    alpha=0.5, edgecolors='black', marker= marker_list[marker],linewidth='2')


    if sv:
        sv_x, sv_y = [], []
        for point in sv:
            try:
                sv_x.append(point[1])
                sv_y.append(point[2])
            except:
                pass

        plt.scatter(sv_x, sv_y, c='black', s=100, label=color,
                    alpha=0.5, edgecolors='black', marker='+')

        ax1.scatter(sv_x, sv_y, c='black', s=100, label=color,
                    alpha=0.5, edgecolors='black', marker='+')

        ax2.scatter(sv_x, sv_y, c='black', s=100, label=color,
                    alpha=0.5, edgecolors='black', marker='+')

    plt.grid(True)
    ax1.grid(True)
    plt.show(block=True)

def main():
    numpoint = 200
    numclass = 10
    features,isFull,classId,centers = getFeatures(numpoint, numclass)
    constArray = getConstraints(numpoint, isFull, classId)
    l = CKMeans(constArray, features, 10)
    kmeansoutput = l.getCKMeans()

    trainerkmeans = Trainer(kmeansoutput, classId, np.transpose(features))
    heteClstrFeatureId, heteClstrId = trainerkmeans.getHeterogenous()

    svmkmeans = trainerkmeans.trainSVM(heteClstrFeatureId, None)

    predictor = Predictor(kmeansoutput, classId, None, svm=svmkmeans)
    svkmeans = predictor.getSV()

    visualiseAfterClustering( kmeansoutput, features, classId, centers, isFull, 'k-means', sv=svkmeans)

    clusterer = CuCKMeans(np.transpose(features), numclass, classId, isFull)
    clusters, centersx = clusterer.cukmeans()
    kmeansoutput = [clusters, centersx]

    trainer = Trainer(kmeansoutput, classId, np.transpose(features))
    heteClstrFeatureId, heteClstrId = trainer.getHeterogenous()

    svm = trainer.trainSVM(heteClstrFeatureId, None)

    predictor = Predictor(kmeansoutput, classId, None, svm=svm)
    sv = predictor.getSV()

    visualiseAfterClustering(kmeansoutput, features, classId, centers, isFull, 'ck-means', sv=sv)

    for cluster in kmeansoutput[0]:
        currCLass = -1
        for pointIn in range(len(cluster)):
            if currCLass == -1 and isFull[cluster[pointIn]]:
                currCLass =  classId[cluster[pointIn]]
            if currCLass != classId[cluster[pointIn]] and isFull[cluster[pointIn]]:
                print 'Nope'

    raw_input()
if __name__ == "__main__": main()