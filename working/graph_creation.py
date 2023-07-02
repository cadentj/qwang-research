import pandas as pd
import networkx as nx
from sklearn.cluster import KMeans
import numpy as np

class UserPOIGraph:

    def __init__ (self):
        pass

    def load_header_data (self):
        self.header_data = pd.read_csv('data/header_data.csv')

    def load_geo_data (self):
        self.geo_data = pd.read_csv('data/geo_data.csv')

    def load_stay_points(self, date):
        month = date[0]
        day = date[1]
        location = f'../data/raw/stay_points_{month}/2017-{month}-{day}.txt'
        column_names = ['userid', 'timecome','date','lat','long','count','timeleave','duration']
        stay_points = pd.read_csv(location, names=column_names)
        return stay_points
    
    def create_centroids(self):


    def cluster_to_pois(self):
        months = ['07','08','09']

        # Missing 31st day in September but eh...
        days = [day for day in range(1,31)]

        for month in months:
            for day in days:
                date = (month, day)
                stay_points = self.load_stay_points(date)

                stay_locations = stay_points[['lat', 'long']]
                stay_locations = stay_locations.to_numpy()

                n_cores = -1
                kmeans = KMeans(n_clusters=len(), n_jobs=n_cores, random_state=0)
                kmeans.fit(stay_locations)







    def initialize_mobility_graph(self):
        self.mobility_graph = nx.DiGraph()

    def weigh_mobility_graph():
        # Weight mobility graph based on stay point location and time spent at each location
        pass



test = UserPOIGraph()
test.load_stay_points(('01', '01'))