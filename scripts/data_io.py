import json
from config import Config
import pandas as pd
import numpy as np
user_cache = {}
movie_cache = {}
     
class DataWriter(object):
    """Writes data to the hard disk.
        
    """
    def __init__(self):
        self.config = Config()
     
            
    
    def update_items(self,PC_matrix):
        """Update k_neighbors property in movie's fast access json files.
        
        Args:
            PC_matrix(pandas.Dataframe) : Dataframe with all Pearson Correlation
                coeficients between each movie pairs. 
                
                    Examples:
                        {
                            "movie_1" : {
                                "movie_2" : -0.3 #This is the PC between movie_1 and movie_2,
                                "movie_3" : 0.2,
                                ...
                                "moview_m" : 0.3
                            }
                        
                        }
        
        """
        for item_id, pc_with_others in PC_matrix.iterrows():
            item_file_name = '{}/{}.json'.format(self.config.items_folder_path, item_id)
            print(item_file_name)
            with open(item_file_name, 'r+') as data_file:
                    print("data file{}".format(data_file))    
                    jsonData= json.load(data_file)
                    jsonData['k_neighbors'] = json.loads(pc_with_others.to_json())
                    data_file.seek(0)
                    data_file.truncate()
                    try:                        
                        json.dump(jsonData,data_file)
                    except:
                        print("why")
                    movie_cache[item_id] = jsonData
                    data_file.close()
    
    def save_neighbors_file(self,  PC_matrix):
        """Save the map from each movie to all of its PC with other movies.
        
        Args:
        
            PC_matrix(pandas.Dataframe): Dictionary with all the PC between movies.
                Examples: 
                   {
                            "movie_1" : {
                                "movie_2" : -0.3 #This is the PC between movie_1 and movie_2,
                                "movie_3" : 0.2,
                                ...
                                "moview_m" : 0.3
                            }
                        
                    }
        
        """
        PC_matrix.to_json("k_neighbors.json")
                
     
    def write_to_json_files (self,data_dict):
        """Create json files with the name of the keys and dumps the value in the file.
        
        Args: 
        
            data_dict (dict): Dict with movie_id as keys and data of movie as 
                value.
                
                Examples:
                    {
                        "movie_1" : {
                            "mean_rating" : 3.3,
                            "ratings" : {
                                "user_1" : 3,
                                "user_2" : 4
                            }
                        }
                    }
                    
        """
        for key, value in data_dict.iteritems():
            output_file = open("{}/{}.{}".format(self.config.output_users_folder, key, 'json'),'w+')
            json.dump(value, output_file)
            output_file.close()
            
    def save_results(self, results_df):
        """Saves results to json file.
        
        Args:
            results_df(pandas.DataFrame): The results table.
        """    
        results_df.to_json("results.json")        

class DataReader(object):
    """Reads data in files.
    
    """
    
    def __init__(self):
        self.config = Config()
            
    def read_ratings_as_df(self):
        """Read original data as a pandas.Dataframe
        
        Returns:
            pandas.DataFrame: Data from the original movies.dat file
        """
        data =  pd.read_table(self.config.ratings_file_path, sep='::', skiprows=0, header=None, names=['user_id', 'movie_id', 'rating', 'timestamp'], converters = {'rating': np.int8} )
        
        data['rating'] =  data['rating'].values.astype(np.int8)
        
        return data
    
    def get_movie_data(self, movie_id, avoid_cache = False):
        """Return data of movie accessing directly to the file.
        
        Args:
            moview_id (str): The movie id.
            
        Returns:
            dict: The data of the movie.
        """
        if( not avoid_cache and movie_id in movie_cache):
            return movie_cache[movie_id]
        
        
        movies_path = self.config.items_folder_path
        movie_data = None
        json_file_path = "{}/{}.json".format(movies_path, movie_id)
        with open(json_file_path, "r") as json_file:
            movie_data = json.load(json_file)
            json_file.close()
            
        return movie_data
    
    def get_user_data(self, user_id, avoid_cache=False):
        """Return data of movie accessing directly to the file.
        
        Args:
            moview_id (str): The movie id.
            
        Returns:
            dict: The data of the movie.
        """
        if( not avoid_cache and user_id in user_cache):
            return user_cache[user_id]
        
        users_path = self.config.users_folder_path
        user_data = None
        json_file_path = "{}/{}.json".format(users_path, user_id)
        with open(json_file_path, "r") as json_file:
            user_data = json.load(json_file)
            json_file.close()
            
        return user_data