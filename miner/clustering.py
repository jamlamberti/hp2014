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
def gen_graphs(C,L,out_dir,threshold, std=False):
    try:
        plt.figure()
        D = hclust.dendrogram(L,color_threshold=threshold)
        if not std:
            plt.savefig(os.path.join(out_dir,'prof_clust_dendrogram.png'))
        else:
            plt.savefig(os.path.join(out_dir, 'student_clust_dendrogram.png'))
        plt.close('all')
    except Exception, ex:
        print("generation of hclust dendrogram failed, (prob too large) Ex: %s" % ex)


def cluster_profs():
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
    db.execute_all("truncate table profClusters")
    for i in range(len(C)):
        sql = "INSERT into profClusters VALUES (null, %s, %s)"
        db.execute_all(sql%(r[i][0], C[i]))
    db.close()
def cluster_students():
    db = db_manager.DatabaseAccess('localhost', 'root', 'root', 'grades')
    db.connect()
    sql = "SELECT sid, crn, rating from students";
    r = db.execute_all(sql)
    vals = {}
    #for i in r:
    #    if i[0] not in r:
    #        vals[i[0]] = []
    #    vals[i[0]].append(i[1])
        # I think the fingerprint should cover the entire space, as in n-d fingerprint for n files
    #X = np.array([[int(i[1]), int(i[2]), int(i[3]), int(i[4])] for i in r])
    #D = distance.pdist(X, 'euclidean')
    #L = cluster(D)
    #C = flatten(C, L, 'clusters', 30)
    #db.execute_all("truncate table profStudents")
    #for i in range(len(C)):
    #    sql = "INSERT into studentClusters VALUES (null, %s, %s)"
    #    db.execute_all(sql%(r[i][0], C[i]))
    #db.close()
if __name__ == "__main__":
    cluster_profs()
    #cluster_students()
