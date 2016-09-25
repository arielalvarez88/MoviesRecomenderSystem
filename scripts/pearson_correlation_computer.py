

import ConfigParser
import pandas as pd
import numpy as np
from datetime import datetime
from scipy.stats import pearsonr
import random
from  data_io import DataWriter
from config import Config

class PearsonCorrelationComputer(object):
    """Calculate Pearson Correlation between movies.
    
    This class calculates Pearson Correlations between each movie provided
    and saves it to the json files that where created by data_formatter.
    
    """
    def __init__(self):
      
        self.config = Config()
        self.pearson_dict = {}
        self.file_writer = DataWriter()
    
    
        
    def __save_to_dict(self,id_i,id_j,pc):
        """Saves pearson correlation between movies in the pearson_dict.
        
        Args:
        
            id_i (str) : A movie id.
            
            id_j (str) : Another movie id.
            
            pc (float) : Pearson Correlation between movies with ids id_i and id_j.
            
        """
        id_i = str(id_i)
        id_j = str(id_j)
        
        self.pearson_dict[id_i] = self.pearson_dict[id_i] if id_i in self.pearson_dict else {}
        self.pearson_dict[id_j] = self.pearson_dict[id_j] if id_j in self.pearson_dict else {}
         
        self.pearson_dict[id_i][id_j] = pc
        self.pearson_dict[id_j][id_i] = pc
    
    
    def __calculate_pearson_corr(self,matrix_J_U, matrix_J_U_subset):
        """Computes pearson corrlation between each pair of movies
        
        Args:
        
            matrix_J_U (pandas.DataFrame) : Dataframe with movies to
                which you want to compute the Person Correlation.
                
            train_subset (pandas.DataFrame) : The subset of movies
                used to compute the pearson correlation.
        Returns:
        
            tuple: A dictionary as first element and the time it took to calculate  
                as second element. The dictionary has movies ids as keys and their 
                Pearson Correlation value with other movies as a dict in the value.
                
                    Examples:
                        ({
                            "movie_1" : {
                                "movie_2" : 0.5,
                                "movie_3" : -0.3
                            },
                            "movie_2" : {
                                "movie_1" : 0.5,
                                "movie_3" : 0.3 
                            },
                            ...
                        }, 200)
                    
                        
            
        """
        init_time = datetime.now()
        all_movies_ids = matrix_J_U.index.values.tolist()
        subeset_movies_ids = matrix_J_U_subset.index.values.tolist()
        movies_checked = {}
        #matrix_J_U = matrix_J_U.values
        #matrix_J_U_subset = matrix_J_U_subset.values
        
        for movie_i_id in all_movies_ids:
            for movie_j_id in subeset_movies_ids:
                
                if(movie_i_id in movies_checked and movie_j_id in movies_checked[movie_i_id] ):
                    continue
                
                self.__save_to_dict(movie_i_id, movie_j_id, True)                              
                  
                movie_j = matrix_J_U_subset.loc[movie_j_id]
                movie_i = matrix_J_U.loc[movie_i_id]                                
                
                common_ratings_idx = movie_j != 0
                common_ratings_idx = common_ratings_idx & (movie_i != 0)                                
                
                ratings_i_common = movie_i[common_ratings_idx]
                ratings_j_common = movie_j[common_ratings_idx]
                
                if(len(ratings_j_common) <= 0  or len(ratings_i_common) <= 0 ):
                    continue

                pearson_ij, _ = pearsonr(ratings_i_common, ratings_j_common)
                if(np.isnan(pearson_ij)):
                    continue
                
                self.__save_to_dict(movie_i_id,movie_j_id,pearson_ij)         
                
        timeDelta = datetime.now() - init_time 
        return  (self.pearson_dict, timeDelta.total_seconds())      
    
    
   
    def compute_pc(self, all_data = None):
     
        """Calculates pearson correlation between movies and saves them to files.
        
        Args:
            all_data (pandas.Dataframe) : All data as read from the original 
                ratings file.
        
            train_subset (pandas.Dataframe)  : Subset of data to use when founding
                PCs.
        """
        time_neighbors = datetime.now()
                
        
        PC_matrix = all_data.corr()
            
        time_neighbors = (datetime.now() - time_neighbors).total_seconds()
        self.file_writer.save_neighbors_file(PC_matrix)
        #self.file_writer.update_items(PC_matrix)
        
        print "Time spent in neighbors calculations {}".format(time_neighbors)
        return  PC_matrix, time_neighbors
        
