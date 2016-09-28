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
        self.report_columns = ['Ratings_in_subset',  'MAE', 'Throughput', 'K_fold', "Neighbors_count" , 'Test_set_percentage']
        self.cv_results = pd.DataFrame(columns=self.report_columns)
        self.test_set_results = pd.DataFrame(columns=self.report_columns)
        self.reader = DataReader()
        self.writer = DataWriter()
       
    @staticmethod
    def train_test_split(ori_data, pivoted_data, test_set_percentage=0.2):
    
        test_ratings = ori_data.sample(frac=test_set_percentage)
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
            
        
    def grid_search(self, data=None, ratings_in_subsets=None, test_set_percentages = None, neighbors_counts=None, k_fold=3):
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
        best_mae = None
        time_stamp = datetime.now()
        for ratings_in_subset in ratings_in_subsets:
            data = all_data.sample(n=ratings_in_subset)

            for test_set_percentage in test_set_percentages:                
                train, test = sklearn.cross_validation.train_test_split(data, test_size=test_set_percentage)
                X = train.loc[:,['user_id','movie_id']]             
                y = train['rating']
       
                                    
                estimator_grid = GridSearchCV(estimator, {"neighbors_count": neighbors_counts}, cv=k_fold, n_jobs=4)            
                estimator_grid.fit(X, y)
                
                
                corr_mtx_file = '../data/runs_{timestamp}/corr_mtx_{ratings_in_subset}_{test_set_percentage}_{neighbors_count}'.format(timestamp=time_stamp,ratings_in_subset=ratings_in_subset, test_set_percentage=test_set_percentage, neighbors_count=estimator_grid.best_params_['neighbors_count'])
                pivoted_data_file = '../data/runs_{timestamp}/pivoted_{ratings_in_subset}_{test_set_percentage}_{neighbors_count}'.format(timestamp=time_stamp,ratings_in_subset=ratings_in_subset, test_set_percentage=test_set_percentage, neighbors_count=estimator_grid.best_params_['neighbors_count'])
                test_file = '../data/runs_{timestamp}/test_{ratings_in_subset}_{test_set_percentage}_{neighbors_count}'.format(timestamp=time_stamp,ratings_in_subset=ratings_in_subset, test_set_percentage=test_set_percentage, neighbors_count=estimator_grid.best_params_['neighbors_count'])
                
                self.writer.create_path(corr_mtx_file)
                self.writer.create_path(pivoted_data_file)
                self.writer.create_path(test_file)                
                
                
                self.writer.save_df(estimator_grid.best_estimator_.correlation_mtx, corr_mtx_file)
                self.writer.save_df(estimator_grid.best_estimator_.pivoted_data, pivoted_data_file)
                self.writer.save_df(test, test_file)
                
                throughput = datetime.now()
                
                test_set_to_predict = test.loc[:,['user_id','movie_id']]
                
                    
                MAE =  estimator_grid.best_estimator_.score(test_set_to_predict, test['rating']) 
                                            
                throughput = (datetime.now() - throughput).total_seconds()
                throughput = throughput/test.shape[0] 
                                                    
                cv_results = self.get_cv_logs(throughput = throughput, ratings_in_subset = ratings_in_subset,  test_set_percentage = test_set_percentage, k_fold= k_fold, grid_search_cv= estimator_grid)
                
                test_set_result = {
                    'Neighbors_count' : estimator_grid.best_params_['neighbors_count'],
                    'Ratings_in_subset' : ratings_in_subset, 
                    'MAE' : MAE, 
                    'Throughput' : throughput, 
                    'K_fold': k_fold, 
                    'Test_set_percentage' : test_set_percentage,                    
                    }
                
                self.test_set_results = self.test_set_results.append(test_set_result, ignore_index=True)                                                         
                self.cv_results = self.cv_results.append(cv_results, ignore_index=True)
                print('Finished iteration. test_set_percentage: {}, ratings_in_subset: {}'.format(test_set_percentage, ratings_in_subset))                                    
                                                        
              
        print('****************** finish ************* {}'.format(self.cv_results) )
        print('****************** finish test: ************* {}'.format(self.test_set_results) )
         
        cv_results_file = '../data/runs_{timestamp}/cv_results.json'.format(timestamp=time_stamp)
        test_set_results_file = '../data/runs_{timestamp}/test_set_results.json'.format(timestamp=time_stamp)
        
        self.writer.save_df(self.cv_results, cv_results_file)
        self.writer.save_df(self.test_set_results, test_set_results_file)
        return self.cv_results, self.test_set_results
    
    def get_cv_logs(self, throughput=None, ratings_in_subset=None, k_fold=None, grid_search_cv=None,  test_set_percentage=None):
        """Return cv_results for each param tested in the grid_search_cv.
      
            Args:
              ratings_in_subset (int): Number of ratings in the data.
              
              k_fold (int) : Number of chunks used in k fold.
              
              grid_search_cv (pandas.GridSearhCV): The GridSearhCV with the cv_results,
                which means is already trained.
            
            Returns:
                list: A list of dicts, one for each param tested, with the keys 
                    being the name of the params and metrics cv_results in this 
                    list -> ['Ratings_in_subset',  
                    'Neighbors_count' , 'MAE', 'PC_calc_time', 'Throughput', 
                    'Time_MAE', 'K_fold']
                    
        """
        
        all_results= []
        for grid_results in grid_search_cv.grid_scores_:
            params, mean_MAE = grid_results[0], grid_results[1]
            
            results = dict(params)
            results['Neighbors_count'] = params['neighbors_count']
            results['MAE'] = mean_MAE
            results['K_fold'] = k_fold
            results['Ratings_in_subset']=ratings_in_subset
            results['Test_set_percentage']= test_set_percentage
            
            results['Throughput'] = throughput            
            all_results.append(results)
                        
            
        return all_results
        
