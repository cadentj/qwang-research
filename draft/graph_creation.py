import pandas as pd
import networkx as nx
from sklearn.cluster import KMeans
import numpy as np
import pickle as pkl

class UserPOIGraph:

    def __init__ (self):
        self.load_header_data()
        self.load_poi_data()
        self.init_node_labels()

    def load_header_data (self):
        self.header_data = pd.read_csv('data/processed/processed_header.csv')
        print("Loaded header data")
    

    def load_poi_data (self):
        self.poi_data = pd.read_csv('data/processed/houston_poi.csv')
        print("Loaded POI data")

    def load_stay_points(self, date):
        month = date[0]
        day = date[1]
        location = f'data/raw/stay_points_{month}/2017-{month}-{day}.txt'
        column_names = ['userid', 'timecome','date','lat','long','count','timeleave','duration']
        stay_points = pd.read_csv(location, names=column_names)
        print(f"Loaded stay points {month}-{day}")
        return stay_points
            

    def cluster_to_pois(self, depth=1, step_size=10000):
        months = ['07','08','09']

        # Missing 31st day in September but eh...
        # Also like July data starts on the second 
        days = [str(day).zfill(2) for day in range(2,31)]

        deep = 0
        for month in months:
            for day in days:
                print(f"Clustering for {month}-{day}")
                date = (month, day)
                stay_points = self.load_stay_points(date)

                stay_locations = stay_points[['lat', 'long']]
                stay_locations = stay_locations.to_numpy()

                kmeans = KMeans(n_clusters=len(self.node_labels), init=self.node_labels, random_state=0)

                for i in range(0,len(stay_locations),step_size):
                    print(f"Clustering {i} to {i+step_size}")
                    slice = stay_locations[i:i+step_size]
                    kmeans.fit(slice)
                    pkl.dump(kmeans, open(f'working/clustered_stay_points/kmeans_{month}_{day}_{i}.pkl', 'wb'))

                deep += 1
                if deep == depth:
                    break


    def init_node_labels(self):
        header_locations = self.header_data[['lat', 'lon']]
        poi_locations = self.poi_data[['lat', 'lon']]
        node_labels = pd.concat([header_locations, poi_locations])
        self.node_labels = node_labels.to_numpy()

    def initialize_mobility_graph(self):
        self.mobility_graph = nx.DiGraph()


    def weigh_mobility_graph():
        # Weight mobility graph based on stay point location and time spent at each location
        pass



test = UserPOIGraph()
test.cluster_to_pois()

# print(pkl.load(open('working/clustered_stay_points/test.pkl','rb')))