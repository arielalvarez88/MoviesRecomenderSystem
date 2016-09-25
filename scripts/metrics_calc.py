from datetime import datetime

import operator
import random

import pandas
import sklearn
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
import sklearn.metrics
from sklearn.metrics.regression import mean_absolute_error

from data_formatter import DataFormatter
from data_io import DataReader, DataWriter
from estimator import RatingsEstimator, NotEnoughInfoException
from log import EstimatorLogger
import numpy as np
import pandas as pd
from pearson_correlation_computer import PearsonCorrelationComputer


class MetricsCalc(object):
    
    def __init__(self):
        self.report_columns = ['Ratings_in_subset',  'MAE', 'Throughput', 'K_fold', "Neighbors_count"]
        self.results = pd.DataFrame(columns=self.report_columns)
        self.reader = DataReader()
        self.writer = DataWriter()
       
    @staticmethod
    def train_test_split(ori_data, pivoted_data, test_percentage=0.2):
    
        test_ratings = ori_data.sample(frac=test_percentage)
        ratings_in_test_set = test_ratings.shape[0]
        
        test_set = np.zeros(pivoted_data.shape)
        test_set = pandas.DataFrame(columns=pivoted_data.columns, index=pivoted_data.index, data=test_set)            
        train_set = pivoted_data        
        
        user_movie_rating = test_ratings[['user_id', 'movie_id', 'rating']].values
        
        subsets_size_to_update = 1000
        start = 0
        
        while (start < ratings_in_test_set):
            stop = start + subsets_size_to_update
            slice = test_ratings.iloc[start:stop , :]
            test_set.loc[slice['user_id'] , slice['movie_id']] = slice['rating']
            train_set.loc[slice['user_id'] , slice['movie_id']] = 0
            
            start += subsets_size_to_update
                                
        return train_set, test_set, ori_data.drop(test_ratings.index,axis=0)
            
        
    def grid_search(self, data=None, ratings_in_subsets=None, neighbors_counts=None, k_fold=3):
        """Gives a report of MAE and Throughput and PC calculation time.
       
        Does a grid search for the K, and percentages and reports back MAE, 
        Throughput and PC calculation time for each of the param values.
        
        Args:
        
            data (pandas.DataFrame): Data in the original format.
            
            ratings_in_subsets (list): A list of absolute movie counts that 
                are going to be used to calculate metrics.
            
            train_percentages (list): The percentage of movies to use when 
                calculating the Pearson Corrlation between movies.
                
            neighbors_counts (list): Numbers of K neighbors to use when predicting.
        
        Returns:
            dict : A dict with the values of all metrics for each
                train_percentages and K_neighbor combination.
        
        
            
       """ 
        
        all_data = data.copy()
        estimator = RatingsEstimator()
        
        
        for ratings_in_subset in ratings_in_subsets:
            EstimatorLogger.clear_log()                                    
            data = all_data.sample(n=ratings_in_subset)
            X = data.loc[:,['user_id','movie_id']]             
            y = data['rating']
            #TODO use 4 jobs in parallel           
            estimator_grid = GridSearchCV(estimator, {"neighbors_count": neighbors_counts}, cv=k_fold, n_jobs=4)            
            estimator_grid.fit(X, y)
            
            throughput = datetime.now()                        
            estimator_grid.predict(X)
            throughput = (datetime.now() - throughput).total_seconds()
            throughput = throughput/y.shape[0] 
                                                
            logs = self.logs_from_gridsearch(throughput = throughput, ratings_in_subset = ratings_in_subset, k_fold= k_fold, grid_search_cv= estimator_grid)
            print('***** otro acabo **** : {}'.format(logs))                                            
            self.results = self.results.append(logs, ignore_index=True)                                    
                                                        
                    
        print('****************** finish ************* {}'.format(self.results) )
        self.writer.save_results(self.results)
        print self.results                    
        return self.results
    
    def logs_from_gridsearch(self, throughput=None, ratings_in_subset=None, k_fold=None, grid_search_cv=None):
        """Return results for each param tested in the grid_search_cv.
      
            Args:
              ratings_in_subset (int): Number of ratings in the data.
              
              k_fold (int) : Number of chunks used in k fold.
              
              grid_search_cv (pandas.GridSearhCV): The GridSearhCV with the results,
                which means is already trained.
            
            Returns:
                list: A list of dicts, one for each param tested, with the keys 
                    being the name of the params and metrics results in this 
                    list -> ['Ratings_in_subset',  
                    'Neighbors_count' , 'MAE', 'PC_calc_time', 'Throughput', 
                    'Time_MAE', 'K_fold']
                    
        """
        estimator_params = EstimatorLogger.log.groupby("Neighbors_count").mean()
        logs_for_these_params=None
        all_results= []
        for grid_results in grid_search_cv.grid_scores_:
            params, mean_val = grid_results[0], grid_results[1]
            logs_for_these_params = estimator_params.loc[params['neighbors_count'],:]
            results = dict(params)
            results['Neighbors_count'] = params['neighbors_count']
            results['MAE'] = mean_val
            results['K_fold'] = k_fold
            results['Ratings_in_subset']=ratings_in_subset
            
            results['Throughput'] = throughput            
            all_results.append(results)
                        
            
        return results
        
