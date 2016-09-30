import errno
import json
import os

from config import Config
import numpy as np
import pandas as pd


user_cache = {}
movie_cache = {}
     
class DataWriter(object):
    """Writes data to the hard disk.
        
    """
    
    
    def __init__(self):
        self.config = Config()
     
    
    def create_path(self, file_path):
        """Creates the folders in specified path if those doesn't exist already.
            
        Args:
            file_path(string): A file path in the system.
        
        Raise: OSError
        """
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:
                raise  exc                            
                
        
    def save_df(self,df,file_name):
        """Saves results to json file.
        
        Args:
            results_df(pandas.DataFrame): The results table.
            
            file_name (str): Name of file.
        """    
        df.to_json(file_name)      

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