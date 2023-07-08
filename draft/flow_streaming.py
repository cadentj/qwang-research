import pandas as pd
import geopandas as gpd
# Using forked skmob package
# https://github.com/cadentj/scikit-mobility
import skmob
from skmob.tessellation import tilers
from shapely import wkt, MultiPolygon
import pickle as pkl

class StreamFlows :
    def __init__(self) -> None:
        self.load_bg_shapes()

    def load_stay_points(self, date):
        month = date[0]
        day = date[1]
        location = f'./../data/raw/stay_points_{month}/2017-{month}-{day}.txt'
        column_names = ['userid', 'timecome','date','lat','long','count','timeleave','duration']
        stay_points = pd.read_csv(location, names=column_names)
        print(f"Loaded stay points {month}-{day}")
        return stay_points
    

    def create_indv_fdfs(self):
        months = ['07','08','09']

        days = [str(day).zfill(2) for day in range(2,31)]  

        for month in months:
            for day in days:
                month = '07'
                day = '31'
                print(f"Creating flowdataframe for {month}-{day}")
                date = (month, day)

                stay_points = self.load_stay_points(date)
                tdf_cols = ['userid', 'timecome', 'lat', 'long']
                to_tdf = stay_points[tdf_cols]
                tdf = skmob.TrajDataFrame(to_tdf, latitude='lat', longitude='long', datetime='timecome', user_id='userid')

                flow, tessellation = tdf.to_flowdataframe(tessellation=self.bg_tessellation, self_loops=True)
                flow = pd.DataFrame(flow)
                flow.origin = flow.origin.astype('int64')
                flow.destination = flow.destination.astype('int64')

                fdf = skmob.FlowDataFrame(data=flow, tessellation=tessellation)
                pkl.dump(fdf, open(f'./pkl_data/data_{month}_{day}.pkl', 'wb'))
                return


    def create_agg_fdf(self):
        months = ['07','08','09']

        days = [str(day).zfill(2) for day in range(2,31)]  

        aggregated_fdf = -1

        aggregated_shapes = []
        running_shapes = []
        for month in months:
            for day in days:
                print(f"Creating flowdataframe for {month}-{day}")
                date = (month, day)

                stay_points = self.load_stay_points(date)
                tdf_cols = ['userid', 'timecome', 'lat', 'long']
                to_tdf = stay_points[tdf_cols]
                tdf = skmob.TrajDataFrame(to_tdf, latitude='lat', longitude='long', datetime='timecome', user_id='userid')
                
                flow, tessellation = tdf.to_flowdataframe(tessellation=self.bg_tessellation, self_loops=True)
                flow = pd.DataFrame(flow)
                flow.origin = flow.origin.astype('int64')
                flow.destination = flow.destination.astype('int64')
                flow.head()
                if type(aggregated_fdf) == type(-1):
                    print("Created initial flowdataframe")
                    aggregated_fdf = skmob.FlowDataFrame(data=flow, tessellation=tessellation)
                    running_shapes.append(aggregated_fdf.shape)
                else:
                    print(f"Aggregated flowdataframe. Depth: {len(aggregated_shapes)}")
                    current_fdf = skmob.FlowDataFrame(data=flow, tessellation=tessellation)
                    running_shapes.append(current_fdf.shape)
                    combined_df = pd.concat([aggregated_fdf, current_fdf], ignore_index=True)
                    aggregated_fdf = combined_df.groupby(['origin', 'destination']).sum().reset_index()

                aggregated_shapes.append(aggregated_fdf.shape)
                
                if (len(aggregated_shapes) % 5 == 0):
                    pack = (aggregated_fdf, aggregated_shapes, running_shapes)
                    pkl.dump(pack, open(f'./pkl_data/data_{month}_{day}.pkl', 'wb'))
                


    def load_bg_shapes(self):
        # 1: Load processed blockgroup shapes from pygris
        bg_shapes = pd.read_csv('./../data/processed/bg_shapefile.csv')

        # 2: Convert into geodataframe 
        bg_shapes = gpd.GeoDataFrame(bg_shapes, geometry=bg_shapes['geometry'].apply(wkt.loads))

        # 3: Drop multipolygons. They are not supported by skmob.
        bg_shapes = bg_shapes.drop(bg_shapes[bg_shapes['geometry'].apply(lambda geom: isinstance(geom, MultiPolygon))].index)
        bg_shapes.reset_index(inplace=True, drop=True)

        # 4: Create a tessellation of the blockgroups
        tessellation_columns = ['GEOID', 'geometry']
        bg_tessellation = bg_shapes[tessellation_columns]
        bg_tessellation.rename(columns={'GEOID':'tile_ID'}, inplace=True)

        # 5: Set the crs to epsg:4326
        bg_tessellation = bg_tessellation.set_crs('epsg:4326')

        self.bg_tessellation = bg_tessellation


obj = StreamFlows()
obj.create_indv_fdfs()

# pkl.dump(data, open(f'./pkl_data/data.pkl', 'wb'))