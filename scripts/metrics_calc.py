from datetime import datetime
import sklearn.cross_validation
from sklearn.grid_search import GridSearchCV
from data_io import DataReader, DataWriter
from estimator import RatingsEstimator
import pandas as pd



class MetricsCalc(object):
    
    def __init__(self):
        self.report_columns = ['Ratings_in_subset',  'MAE', 'Throughput', 'K_fold', "Neighbors_count" , 'Test_set_percentage']
        self.cv_results = pd.DataFrame(columns=self.report_columns)
        self.test_set_results = pd.DataFrame(columns=self.report_columns)
        self.reader = DataReader()
        self.writer = DataWriter()
   
    def train_with_cv(self, data=None, ratings_in_subsets=None, test_set_percentages = None, neighbors_counts=None, k_fold=3):
        """Performs the training with all parameters and returns the results.
               
        Args:
        
            data (pandas.DataFrame): Data in the original format.
            
            ratings_in_subsets (list): A list of absolute ratings counts that 
                are going to be used to calculate metrics.
            
            train_percentages (list): The percentage of ratings to user as train 
                sets.
                
            neighbors_counts (list): Numbers of K neighbors to use when predicting.
            
            k_fold (int): Numbers of folds to use in K-fold cross validation.
        
        Returns:
        
            pandas.DataFrame : A table with the results of the metrics. The MAE
                is performed with the training set (training error). 
            
            pandas.DataFrame : A table with the results of the metrics. The MAE
                is performed with the test set (testing error). 
            
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
                
                
                
                test_set_to_predict = test.loc[:,['user_id','movie_id']]
                
                throughput = datetime.now()
                    
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
            results['MAE'] = -mean_MAE
            results['K_fold'] = k_fold
            results['Ratings_in_subset']=ratings_in_subset
            results['Test_set_percentage']= test_set_percentage
            
            results['Throughput'] = throughput            
            all_results.append(results)
                        
            
        return all_results
        
