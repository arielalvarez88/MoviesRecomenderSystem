

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
        
            
        self.test_columns = ['Train', 'K' , 'MAE', 'Neighbors Time', '' , 'Throughput']
        self.pearson_dict = {}
        self.movies_ids = []
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
    
    
    def __calculate_pearson_corr(self,matrix_J_U_subset):
        """Computes pearson corrlation between each pair of movies
        
        Args:
        
            matrix_J_U_subset (pandas.DataFrame) : Dataframe with movies to
                which you want to compute their K neighbors.
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
        
        for i in range(0, matrix_J_U_subset.shape[0]):
            for j in range(i+1, matrix_J_U_subset.shape[0]):
                indeces_in_common = matrix_J_U_subset[j] != 0
                indeces_in_common = indeces_in_common * matrix_J_U_subset[i] != 0
                i_common = matrix_J_U_subset[i][indeces_in_common]
                j_common = matrix_J_U_subset[j][indeces_in_common]
                pearson_ij, _ = pearsonr(i_common, j_common)
                movie_i_id = self.movies_ids[i]            
                movie_j_id = self.movies_ids[j]
                self.__save_to_dict(movie_i_id,movie_j_id,pearson_ij)           
                
        timeDelta = datetime.now() - init_time 
        return  (self.pearson_dict, timeDelta.total_seconds())      
    
    
   
    def compute_pc(self, all_data = None, train_percentages = [0.001]):
     
        """Calculates pearson correlation between movies and saves them to files.
        
        Args:
            all_data (pandas.Dataframe) : All data as read from the original 
                ratings file.
        
            train_percentages (list) : List of floating numbers representing 
                the percentage of the total number of movies which the K
                neighbors will be computed.
        """   
        if(all_data is None):
            all_data = pd.read_table(self.config.ratings_file_path, sep='::', skiprows=0, header=None, names=['user_id', 'movie_id', 'rating', 'timestamp'])
    
        self.movies_ids = all_data['movie_id'].unique()
        
        self.results = pd.DataFrame(columns=self.test_columns)
        
        matrix_J_U = all_data.pivot(columns='user_id', index='movie_id', values='rating')
        self.movies_ids = matrix_J_U.index.values
        
        matrix_J_U = matrix_J_U.values
        
        #Replace NaN for 0
        matrix_J_U[np.isnan(matrix_J_U)] = 0
        
        time_neighbors = 0
        product_count = matrix_J_U.shape[0]
        range_of_rows = range(0, product_count)
            
    
        for train_percentage in train_percentages:
            subset_rows = int(matrix_J_U.shape[0] * train_percentage)
                    
            movies_subset = matrix_J_U[ random.sample(range_of_rows,  subset_rows) , :]
            self.pearson_dict, time_neighbors  = self.__calculate_pearson_corr(movies_subset)
            
            self.results.append({'Train' : train_percentage, 'Neighbors Time' : time_neighbors} , ignore_index=True)
            break
    
        self.file_writer.save_neighbors_file(self.pearson_dict)
        self.file_writer.update_items(self.pearson_dict)
    
        print "Time spent in neighbors calculations {}".format(time_neighbors)
    
