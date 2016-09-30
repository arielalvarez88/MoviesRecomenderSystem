import copy
from config import Config
from data_io import DataReader
import numpy as np

class DataFormatter(object):
    """Helper for pivoting data.
    """
                
    @staticmethod
    def pivot_data(data):
        """Transform raw data into the a matrix where each row represents a
            user and each column a movie.
                
        Args:
            
            data(pandas.Dataframe): Data as presented in the raw file.
        
        Returns:
            pandas.Dataframe: The pivoted pandas.Dataframe.
        """
        data = data.pivot(index='user_id', columns='movie_id', values='rating')        
                    
        return data
                
