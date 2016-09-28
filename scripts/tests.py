import pandas
import scipy.stats
import numpy as np
import sklearn.metrics 
from sklearn.svm import LinearSVC
from sklearn.utils.estimator_checks import check_estimator

from data_analyst import DataAnalyst
from estimator import RatingsEstimator
import estimator
import matplotlib.pyplot as plt
import pandas as pd


def test_estimator():
    
    ratings_est = estimator.RatingsEstimator()
    ratings_est.set_params(neighbors_count = 6000)
    X = pd.DataFrame(columns=['user_id', 'movie_id'])
    all_data = X.append([
        {
            'user_id' : 1,
            'movie_id' : 1,
            'rating': 3 
        },
                  {
            'user_id' : 2,
            'movie_id' : 3,
            'rating': 4 
        },
                  {
            'user_id' : 3,
            'movie_id' : 4,
            'rating': 5 
        },
                  {
            'user_id' : 1,
            'movie_id' : 3,
             'rating': 4
        },
                  
                          {
            'user_id' : 1,
            'movie_id' : 2,
            'rating': 3
        },        {
            'user_id' : 1,
            'movie_id' : 4,
            'rating': 5
        },        {
            'user_id' : 2,
            'movie_id' : 1,
             'rating': 2
        },        {
            'user_id' : 2,
            'movie_id' : 2,
            'rating': 5
        },        {
            'user_id' : 2,
            'movie_id' : 4,
             'rating': 5
        },        {
            'user_id' : 3,
            'movie_id' : 1,
            'rating': 0
        },        {
            'user_id' : 3,
            'movie_id' : 2,
            'rating': 2
        },        {
            'user_id' : 3,
            'movie_id' : 3,
            'rating': 3
        },
                  
                  
        ],ignore_index=True)

    X =  all_data.loc[:, ['user_id', 'movie_id']]    
    y = all_data.loc[:, ['rating']] 
    
    ratings_est.fit(X,y)
    to_predict = pd.DataFrame(columns=['user_id', 'movie_id'])
    to_predict = to_predict.append([
            {'user_id': 3, 'movie_id': 2},
            {'user_id': 3, 'movie_id': 1},
            {'user_id': 1, 'movie_id': 3},
        ], ignore_index=True)
    
    print(ratings_est.predict(to_predict))
    print(ratings_est.score(to_predict,all_data.iloc[ [10,9,3], :].loc[:, ['rating']] ))
    print('hola')


#test_estimator()


def test_real_vals():
    time_stamp = '2016-09-27 02:28:57.721536'
    ratings_in_subset='100000'
    test_set_percentage='0.3' 
    neighbors_count= '25'
    
    corr_mtx_file_name = '../data/runs_{timestamp}/corr_mtx_{ratings_in_subset}_{test_set_percentage}_{neighbors_count}.json'.format(timestamp=time_stamp, ratings_in_subset=ratings_in_subset, test_set_percentage=test_set_percentage, neighbors_count=neighbors_count)
    pivoted_data_file_name = '../data/runs_{timestamp}/pivoted_{ratings_in_subset}_{test_set_percentage}_{neighbors_count}.json'.format(timestamp=time_stamp,ratings_in_subset=ratings_in_subset, test_set_percentage=test_set_percentage, neighbors_count=neighbors_count)
    test_file_name = '../data/runs_{timestamp}/test_{ratings_in_subset}_{test_set_percentage}_{neighbors_count}.json'.format(timestamp=time_stamp,ratings_in_subset=ratings_in_subset, test_set_percentage=test_set_percentage, neighbors_count=neighbors_count)
    
    corr_mtx_file = open(corr_mtx_file_name, 'r')
    pivoted_data_file = open(pivoted_data_file_name, 'r')
    test_file = open(test_file_name, 'r')
    
    corr_mtx = pd.read_json(path_or_buf=corr_mtx_file)
    pivoted_data = pd.read_json(path_or_buf=pivoted_data_file)
    test_set = pd.read_json(path_or_buf=test_file)
    
    estimator = RatingsEstimator()
    estimator.neighbors_count= 6000
    estimator.correlation_mtx= corr_mtx
    estimator.pivoted_data = pivoted_data
    
        
    def find_more(array, columns=True):    


        if(columns):
            non_zero_pairs = np.where(estimator.pivoted_data.loc[:,array] != 0)
        else:
            non_zero_pairs = np.where(estimator.pivoted_data.loc[array, :] != 0)
    
        movie_more_rating = scipy.stats.mode(non_zero_pairs[1])
        user_more_rating = scipy.stats.mode(non_zero_pairs[0])
        print 'User more: {}, movie_more {}'.format(estimator.pivoted_data.index[user_more_rating.mode[0]], estimator.pivoted_data.columns[movie_more_rating.mode[0]])

    estimator.pivoted_data.iloc[:,:] = np.nan_to_num(estimator.pivoted_data.values)
    find_more(estimator.pivoted_data.columns)

    all_predictions = estimator.predict(test_set.loc[:,['user_id', 'movie_id']])
    print 'ya'
    
    
test_real_vals()
exit()



analyst = DataAnalyst()

results = pd.DataFrame(index=[], columns=['Ratings_in_subset', 'Throughput', 'Test_set_percentage'])

results= results.append([
    {
        
        'Ratings_in_subset': 20,
        "Throughput" : 10000,        
        'Test_set_percentage' : 0.2
    },
                
                {
        
        'Ratings_in_subset': 50,
        "Throughput" : 8000,        
        'Test_set_percentage' : 0.2
    },
                
                {
        
        'Ratings_in_subset': 100,
        "Throughput" : 4500,        
        'Test_set_percentage' : 0.2
    },
                
                
                
                {
        
        'Ratings_in_subset': 20,
        "Throughput" : 20000,        
        'Test_set_percentage' : 0.4
    },
                
                {
        
        'Ratings_in_subset': 50,
        "Throughput" : 10000,        
        'Test_set_percentage' : 0.4
    },
                
                {
        
        'Ratings_in_subset': 100,
        
        "Throughput" : 8000,        
        'Test_set_percentage' : 0.4
    }
    
    ], ignore_index=True)


analyst.multiple_lines_plot(results, "Ratings_in_subset","Throughput", 'Ratings_in_subset', 'Throughput', group_by_field='Test_set_percentage', line_legend_tpl = "Test set percentage: {}", figure_title= 'Ratings_in_subset vs Throughput at each test/train split')
