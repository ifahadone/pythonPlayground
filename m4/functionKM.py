import pandas as pd
from sklearn.cluster import KMeans # Importing KMeans

def perform(c,d):

    df = pd.DataFrame(d,columns = ['id', 'lat', 'long'])


    # Creating an instance of KMeans to find n clusters
    kmeans_1 = KMeans(n_clusters=c)
    # Using fit_predict to cluster the dataset
    X = df[['lat','long']].values
    predictions = kmeans_1.fit_predict(X)
    clustered = pd.concat([df.reset_index(), 
                        pd.DataFrame({'Cluster':predictions})], 
                        axis=1)


    conditions = []

    for i in range(c):
        conditions.append(clustered['Cluster'] == i)
    

    centers = kmeans_1.cluster_centers_

    a = []
    for i in range(len(centers)):
        a.append(dict.fromkeys(['centroid', 'values']))
        
    b = {'clusters': None}
    b['clusters']=a

    for i in range(len(centers)):
        b['clusters'][i]['centroid'] = []
        b['clusters'][i]['centroid'].append(centers[i][0])
        b['clusters'][i]['centroid'].append(centers[i][1])

    rj = []
    #jk = []

    for i in range(len(centers)):
        c1= clustered.loc[clustered['Cluster'] == i]
        m = c1.to_dict('r')
        rj = []
        for j in range(len(m)):
            rj.append(m[j]['id'])
            #rj.append(m[j]['lat'])
            #rj.append(m[j]['long'])
            #jk.append(rj)

        b['clusters'][i]['values'] = rj
        #jk = []
    
   

    return b
