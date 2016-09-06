import json
from config import Config
import pandas as pd
class DataWriter(object):
    
    def __init__(self):
        self.config = Config()
     
            
    
    def update_items(self,info_dict):
        """Update k_neighbors property in movie's fast access json files.
        
        Args:
            info_dict (dict) : Maps a movie to each of its Pearson Correlation
                coeficients between the other movies.
                
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
        for item_id, neighbor_data in info_dict.iteritems():
            item_file_name = '{}/{}.json'.format(self.config.items_folder_path, item_id)
            print(item_file_name)
            with open(item_file_name, 'r+') as data_file:    
                    jsonData= json.load(data_file)
                    data_file.seek(0)
                    jsonData['k_neighbors'] = neighbor_data
                    json.dump(jsonData,data_file)
                    data_file.close()
    
    def save_neighbors_file(self,  neighbors_dict):
        """Save the map from each movie to all of its PC with other movies.
        
        Args:
        
            neighbors_dict: Dictionary with all the PC between movies.
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
        with open("neighbors.json", 'w+') as data_file:
            data_file.seek(0)    
            json.dump(neighbors_dict, data_file)
            data_file.close()
                
     
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
        return pd.read_table(self.config.ratings_file_path, sep='::', skiprows=0, header=None, names=['user_id', 'movie_id', 'rating', 'timestamp'])
