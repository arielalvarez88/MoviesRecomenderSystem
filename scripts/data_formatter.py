import copy
from config import Config
from data_io import DataReader
import numpy as np

class DataFormatter(object):
    """Gathers all data for the movies and create fast access files.
    
    This modules gathers all ratings given to an movie and saves it into 
    a file with its mean_rating and other info.
    
    Example:
        A dataframe with original data is given with multiple rows with these columns = ['user-id','movie-id','rating'].
        The result is multiple json files, each one representing a movie and with the id of the movie as file name, in the next format:
            
            moview_10.json:
            
                {    
                    "movie_id": 10, 
                    "mean_rating", 3.5,
                    "ratings": {
                        "user_001": 5,
                        "user_003": 2
                    }
                }
        
    
    """
    def __init__(self, break_after = 1000, break_after_limit=False):
        self.break_after = self.break_after
        self.break_after_limit = self.break_after_limit
        
        self.config = Config()
       
        
        self.rating_file_order = ["user_id","movie_id","rating","timestamp"]
        
        self.movie_file_tpl = {
                        
            "mean_rating" : "3.3",
        
            "ratings" : {
                     
                        "user_id" : "3.3"
            },
                        
            "pearson_correlation_computer": {
                    "movie_id" : "3.3 (weight)"
            }
                        
        }
        
        
        
        self.movie_file_tpl = {
            "ratings": {
                "movie-id" : 2.2
            }
        }
        
        self.all_movie_data = {
                      
        }
        
        self.all_user_data = {
        
        }
    
        
  
    def _fill_formatted_dicts(self,data):
        """Formats data into dicts.
        Args:
            data (pandas.Dataframe) : A dataframe representation of the original data.
        """    
        for i, vals in data.iterrows(): 
            #vals = dict( zip(self.rating_file_order, vals) )
            user_id = vals['user_id']
            movie_id = vals['movie_id']
                    
            movie_data =   self.all_movie_data[movie_id] if movie_id in self.all_movie_data else copy.deepcopy(self.movie_file_tpl) 
            user_data = self.all_user_data[user_id] if user_id in self.all_user_data else copy.deepcopy(self.movie_file_tpl) 
            
                   
            movie_data['ratings'][user_id] = vals['rating']
            
            user_data['ratings'] [movie_id] = vals['rating']
            
            self.all_user_data[user_id] = user_data
            self.all_movie_data[movie_id] = movie_data       
            if(i >= self.break_after and self.break_after_limit):
                break;
    
    
    def ori_data_to_json_files(self, data=None):
        """Gathers all info of the movies and write it to files.
       
        Args:
            data (pandas.Dataframe) : Representation of the original data in a dataframe.
            
        """
        if(data is None):
            data = DataReader().read_ratings_as_df()
        self._fill_formatted_dicts(data)
        self.write_to_json_files(self.all_user_data)
        self.write_to_json_files(self.all_movie_data)      
                
    @staticmethod
    def pivot_data(data):
        """Transform raw data into formated numpy matrix.
        
        Transforms raw data into a matrix where each row represents a movie,
        each column a user and each value the rating that the user gave the movie.
        
        Args:
            
            data(pandas.Dataframe): Data as presented in the raw file.
        
        Returns:
            pandas.Dataframe: The formatted pandas.Dataframe.
        """
        data = data.pivot(columns='user_id', index='movie_id', values='rating')        
                
        #Replace NaN for 0
        data[np.isnan(data)] = 0
        
        return data
                
