from datetime import datetime
import operator
import sys

from numpy.core.test_rational import denominator, numerator
import sklearn
from sklearn.base import BaseEstimator, ClassifierMixin
import sklearn.metrics

from data_formatter import DataFormatter
from data_io import DataReader
import datastructures
from log import EstimatorLogger
import numpy as np
import pandas as pd
from pearson_correlation_computer import PearsonCorrelationComputer
from datastructures import OrderedSet


class NotEnoughInfoException(Exception):
    def __init___(self, dErrorArguments):
        Exception.__init__(self,"There is no information to predict the movie. The user has to have ratings for at least 1 of the k neighbors.")
        self.dErrorArguments = dErrorArguments

class RatingsEstimator(BaseEstimator, ClassifierMixin):
    """Class to recommend and predict movie ratings for users.
    
    Attributes:
        __k (int) : The number of neighbors to take into account for predicitons
            and suggestions.
                
    """
    def __init__(self, neighbors_count=5, df_log=None):        
        self.neighbors_count = neighbors_count            
        self.reader = DataReader()        
        self.X=None
        self.y=None
        self.pivoted_data=None
        self.df_log = None
        self.pc_computer = PearsonCorrelationComputer()
        self.correlation_mtx = None

    def fit(self, X, y):
        self.X = X
        self.y = y
        self.all_data = X.copy()
        self.all_data['rating'] = y
        
        self.pivoted_data = DataFormatter.pivot_data(self.all_data)        
        self.correlation_mtx, _ = self.pc_computer.compute_pc(self.pivoted_data)
        
        return self

    def predict(self, to_predict):       
        """Predicts values.
                
        Args:
            
            X (pandas.Dataframe): Data to predict.            
        
        I want a matrix of Movies x Movies dimention with the PC values, but PC =0 i
            f the its not a K neighbor. The K neighbors for Movie i will be in 
            the Vertical Axis. The product of my #Users x #Movies matrix with that   
            matrix will a matrix with Movies in the columns and Users in the Rows
            and each value represents the numerator of the rating forumla the 
            predicted ratings between that user and that movie
        """
        
        time_mae = datetime.now()
        all_movies = set(to_predict['movie_id'].values).union(self.pivoted_data.columns.values)
        users_to_predict = list(set(to_predict['user_id'].values))
        to_predict_pivot = self.pivoted_data.reindex(index= users_to_predict,columns = all_movies) 
        correlation_mtx_k = self.correlation_mtx.reindex(index= all_movies , columns= all_movies)
        
        ratings_positions = to_predict_pivot != 0
         
        to_predict_pivot.iloc[:,:] = np.nan_to_num(to_predict_pivot) 
        correlation_mtx_k.iloc[:,:] = np.nan_to_num(correlation_mtx_k)
         
        for column in correlation_mtx_k.columns.values:
            data = correlation_mtx_k.loc[:, column].to_dict()
           
            sorted_data = sorted(data.iteritems(), key=operator.itemgetter(1))
            neighbors_to_eliminate = sorted_data[0 : len(sorted_data) - self.neighbors_count]
            correlation_mtx_k.loc[dict(neighbors_to_eliminate).keys(), column] = 0 
                    
        time_predicting = datetime.now() 
        np.fill_diagonal(correlation_mtx_k.values, 0)

        predictions = to_predict_pivot.dot(correlation_mtx_k) / (to_predict_pivot != 0).dot(correlation_mtx_k.abs())
        time_predicting = (datetime.now() - time_predicting).total_seconds()
        
        try:
            throughput = ratings_positions.sum().sum() / (time_predicting )
        except ZeroDivisionError:
            throughput = sys.maxint
     
        key = self.get_params()['neighbors_count']
                  

        predictions = predictions.reindex(index=list(set(to_predict['user_id'])), columns = list(set(to_predict['movie_id'])) )

        results = []
        for row in to_predict.itertuples(index=False):
            user_id = row[0]
            movie_id = row[1]
            results.append(predictions.loc[user_id, movie_id] )    
        if(len(results) == 0):
            print ('kaboom')
        return results
    
    def suggest(self, user_id, number_of_suggestions = 1):
        """Returns a list of movies ids that the user might like. 
        
        It suggests movies to the specified user by going in to his top rated
        items and getting their K neighbors.
        
        """
    
    def get_k_neighbors(self, pcs_with_others):
        """Returns the k biggest Pearson Correlations, there for the k neighbors.
        
        Args:
        
            pcs_with_others (dict): The Pearson Correlation between the movie
                of which you want the k neighbors and all the other movies. It
                has the movie_ids as keys and the PC as values
            
                Examples: 
                    {
                        "movie_id2" : -0.3,
                        "movie_id3" : 0.89
                
                    }
                    
        Returns:
            dict: A dict with the ids of the K Neighbors with their PC as value.
        """
        pcs_without_none = pd.DataFrame(columns=pcs_with_others.keys())
        pcs_without_none = pcs_without_none.append(pcs_with_others,ignore_index=True)
        pcs_without_none = pcs_without_none.fillna(-1)
        pcs_without_none = pcs_without_none.to_dict('records')[0]
        
        ordered_pcs = sorted(pcs_without_none.iteritems(), key=operator.itemgetter(1))
        
        k_neighbors = ordered_pcs[ self.k * -1 : -1]
        
        return dict(k_neighbors)
        
    def predict_single(self, user_id, movie_id):
        """ Predicts rating the user will give to the movie.
            
            This method receives an user_id and returns the predicted rating 
            for the specified movie. 
        Args:
        
            user_id (str) : The id of the user for which you want to predict the 
                rating on the movie.
                
            movie_id(str) : The id of the movie on which the prediction will be made.
            
        Returns:
            float: The predicted rating
        Raise:
            NotEnoughInfoException: When user doesn't have any rating on the k neighbors of movie.
        """
        movie_data = self.reader.get_movie_data(movie_id)
        user_data = self.reader.get_user_data(user_id)
        k_neighbors = self.get_k_neighbors(movie_data['k_neighbors'])
        
        k_neighbors_rated_by_user = self.__k_neighbors_rated_by_user(user_data['ratings'].keys(), k_neighbors.keys() )
        
        if(len(k_neighbors_rated_by_user) == 0):
            raise NotEnoughInfoException()
        numerator = 0
        denominator = 0
       
        PC = None
        
        for movie in k_neighbors_rated_by_user:
            PC = k_neighbors[movie]
            user_rating = user_data['ratings'][movie]
            try:
                numerator += PC * int(user_rating)
            except Exception as err:
                print err 
            denominator += abs(PC)
        
        try:
            return numerator/denominator
        except ZeroDivisionError:
            return 0
        
    
    
    def __k_neighbors_rated_by_user(self, movies_rated_by_user, k_neighbors):
        """Get the k_neighbors that user has rated.
                
        Returns:
            set: Set with the movies ids of the k_neighbors rated by user
            
        """
   
        return set(movies_rated_by_user).intersection(set(k_neighbors))
    
    def score(self, X, y):
        predictions = self.predict(X)        
        if(len(y) == 0):
            return 0    
        MAE = np.sum(np.abs(predictions - y))/y.shape[0]
        return MAE
        
    def get_k(self):
        return self.__k


    def set_k(self, value):
        self.__k = value


    def del_k(self):
        del self.__k

    k = property(get_k, set_k, del_k, "k's docstring")
 