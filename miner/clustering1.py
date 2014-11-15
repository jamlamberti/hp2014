import matplotlib
import numpy as np
import scipy.cluster.hierarchy as hclust
from scipy.spatial import distance
import matplotlib.pyplot as plt
import fastcluster
import os
try:
    import db_manager
except:
    import sys, inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)
    import db_manager

def cluster(D):
    L = fastcluster.linkage(D, method='ward')
    return L
def flatten(L, threshold):
    C = hclust.fcluster(L, threshold, criterion='distance')
    for x in np.nditer(C, op_flags=['readwrite']):
        x[...] = x-1
    Cl = frozenset(C)
    return C
def gen_graphs(C,L,out_dir,threshold):
    try:
        plt.figure()
        D = hclust.dendrogram(L,color_threshold=threshold)
        plt.savefig(os.path.join(out_dir,'clust_dendrogram.png'))
        plt.close('all')
    except Exception, ex:
        print("generation of hclust dendrogram failed, (prob too large) Ex: %s" % ex)


def test():
    db = db_manager.DatabaseAccess('localhost', 'root', 'root', 'grades')
    db.connect()
    sql = "SELECT id, helpfulness, clarity, easiness, sentiment from postparse"
    r = db.execute_all(sql)

    import random
    X = np.array([[int(i[1]), int(i[2]), int(i[3]), int(i[4])] for i in r])
    D = distance.pdist(X, 'euclidean')
    L = cluster(D)
    C = flatten(L, 30)
    gen_graphs(C, L, 'clusters', 30)
    db.close()
test()
