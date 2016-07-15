"""
CKMeans class
Amir H - Arda I
15.07.2016
"""
import numpy as np
import getConstraints
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class CKMeans:
    
    MUST_LINK = 1
    CANNOT_LINK = -1
    
    def __init__(self, consArr, featArr, k):

        self.consArr = consArr
        self.featArr = np.transpose(featArr)
        self.k = k
        self.clusterList = []
    
    def initCluster(self):
        #method to initialize the cluster
        
        for i in range(0,self.k):
            cluster = np.array([])
            center = self.featArr[i]
            self.clusterList.append((cluster,center))
    
    def violateConstraints(self, data, cluster):
        # method to check if the instance violates the constraints (part of CK-Means)
        # data : id of the instance
        # cluster : current cluster in which we're checking the condition
        
        for i in self.consArr[data]:
            if(i == MUST_LINK):
                if i not in cluster:
                    return true
            elif(i == CANNOT_LINK):
                if i in cluster:
                    return true
        return false
    
    def CKMeans(self) :
        # method to apply CK_Means
        
        # Counter to limit the number of iterations
        iterCounter = 0
        
        #Old centers of clusters
        oldCenters = np.arrayzeros(self.k)
        
        while iterCounter < 20 :
            
            #Check for convergence
            difference = 0
            for i in range(0, self.k):
                difference += np.linalg.norm(oldCenters[i] - self.clusterList[1][i])
                
            if difference == 0:
                break
            
            ############ Assign each instance of feature matrix to a cluster #############
            
            for i, line in enumerate(self.featArr):
                # i : id of the instance
                # line : points of that instance
                
                availClus = []
                for j in self.clusterList:
                    # j : Tuple (Cluster, Center of the cluster)
                    
                    constraint = self.violateConstraints(i, j[0])
                    if not constraint:
                        availClus.append(j)
                        
                if not availClus:
                    print "ERROR : No available clusters found"
                    continue
                    
                # Find the closest cluster
                minDist = sys.maxint
                clusNum = 0
                counter = 0              
                for clus in availClus:
                    # clus : Tuple (Cluster, Center of the cluster)
                    
                    dist = np.linalg.norm(line - clus[1])
                    if dist <= minDist:
                        minDist = dist
                        clusNum =counter
                    counter+=1
                
                # Assign the instance to the cluster
                self.clusterList[clusNum][0].append(i)
            
                ########################################################################

            # Save current cluster centers
            for i in range(0, self.k):
                oldCenters[i] = self.clusterList[1][i]
                
            # Find new centers of each cluster
            dim = self.featArr.shape[1] #720    
            for order in range(0, self.k):
                
                # clus : Tuple (Cluster, Center of the cluster)
                clus = self.clusterList[order] 
                clusLength = len(clus[0][0])
                
                for i in range(0, dim):
                    # i : order that we're in (0...719)
                    
                    coorSum = 0
                    for j in clus[0]:
                        # j : id of the instance
                        coorSum += self.featArr[j][i]      
                    coorSum /= clusLength
                    self.clusterList[1][order][i] = coorSum

            # Empty out the assigned instances of clusters
            for i in range(0, self.k):
                self.clusterList[0][i] = np.array([])
            
            # Increment the counter
            iterCounter += 1        

        return self.clusterList



def visualiseBeforeClustering(out,features):
    color = 'black'
    for cluster in out[0]:
        for i in cluster:
              x = features.tolist()[i]
              scale = 80
              plt.scatter(x[0], x[1], c=color, s=scale, label=color,
                    alpha=0.5, edgecolors='black')
    plt.figure()
    plt.grid(True)

def visualiseAfterClustering(out,features):
    colorList = cm.rainbow(np.linspace(0, 1, len(out[0])))
    index = 0
    for cluster in out[0]:
        index+=1
        color = colorList[index-1]
        for i in cluster:
              x = features.tolist()[i]
              scale = 80




              plt.scatter(x[0], x[1], c=color, s=scale, label=color,
                    alpha=0.5, edgecolors='black')

    plt.grid(True)

    
def main():
    CKMeans()
   

    
if __name__ == '__main__':
    main()
    #profile.run('print main(); print')
