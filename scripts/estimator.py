from datetime import datetime
import operator
from sklearn.base import BaseEstimator, ClassifierMixin
import sklearn.metrics

from data_formatter import DataFormatter
import numpy as np
import pandas as pd
from pearson_correlation_computer import PearsonCorrelationComputer


class RatingsEstimator(BaseEstimator, ClassifierMixin):
    """Class to  predict movie ratings for users.
    
    Attributes:
    
        neighbors_count (int) : The number of neighbors to take into account for 
            predicitons.
            
        X (pandas.DataFrame): The input training data. It has two columns:
            'user_id' and 'movie_id' 
        
        y (pandas.DataFrame): The output for the training data.
        
        pivoted_data (pandas.DataFrame): The training data in X and y is pivoted
            in a matrix where you map the user_id (in the rows) to the movie_id
            in the columns.
            
        pc_computer (pearson_correlation_computer.PearsonCorrelationComputer):
            A class that calculates the correlation matrix.
            
        correlation_mtx (pandas.DataFrame): The correlation matrix. It has the
            Pearson Correlation coeficient for each movie pair. Each row
            represents a movie and each column represents another movie.
    """
    def __init__(self, neighbors_count=5):        
        self.neighbors_count = neighbors_count                        
        self.X=None
        self.y=None
        self.pivoted_data=None        
        self.pc_computer = PearsonCorrelationComputer()
        self.correlation_mtx = None

    def fit(self, X, y):
        """ Method call to train the model.
        
        Args:
            X (pandas.DataFrame): The input training data. It has two columns:
            'user_id' and 'movie_id' 
        
            y (pandas.DataFrame): The output for the training data.
        
        """
        self.X = X
        self.y = y
        self.all_data = X.copy()
        self.all_data['rating'] = y
        
        self.pivoted_data = DataFormatter.pivot_data(self.all_data)        
        self.correlation_mtx, _ = self.pc_computer.compute_pc(self.pivoted_data)
        
        return self

    def predict(self, to_predict):       
        """Method to predicts the ratings.
                
        Args:
            
            X (pandas.Dataframe): Data to predict. It has two columns:
            'user_id' and 'movie_id'.            
                
        """                
                
        all_movies = set(to_predict['movie_id'].values).union(self.pivoted_data.columns.values)
        all_movies = pd.Series(list(all_movies))
        movies_to_predict_idxs = all_movies.isin( to_predict['movie_id'] )
        
        users_to_predict = list(set(to_predict['user_id'].values))
        to_predict_pivot = self.pivoted_data.reindex(index= users_to_predict,columns = all_movies) 
        correlation_mtx_k = self.correlation_mtx.reindex(index= all_movies , columns= all_movies[movies_to_predict_idxs])
        
        #Make 0 the correlation between an item with himself so it doesnt count in the predictions. 
        correlation_mtx_k.loc[all_movies[movies_to_predict_idxs], all_movies[movies_to_predict_idxs]] = 0
        
        
         
        to_predict_pivot.iloc[:,:] = np.nan_to_num(to_predict_pivot) 
        correlation_mtx_k.iloc[:,:] = np.nan_to_num(correlation_mtx_k)
         
        for column in correlation_mtx_k.columns.values:
            data = correlation_mtx_k.loc[:, column].to_dict()
           
            sorted_data = sorted(data.iteritems(), key=operator.itemgetter(1))
            last_index = -self.neighbors_count if self.neighbors_count <= len(sorted_data) else -len(sorted_data) 
            neighbors_to_eliminate = sorted_data[0 : last_index]
            correlation_mtx_k.loc[dict(neighbors_to_eliminate).keys(), column] = 0 
                    
        time_predicting = datetime.now()         

        predictions = to_predict_pivot.dot(correlation_mtx_k) / (to_predict_pivot != 0).dot(correlation_mtx_k.abs())
        time_predicting = (datetime.now() - time_predicting).total_seconds()
                        

        predictions = predictions.reindex(index=list(set(to_predict['user_id'])), columns = list(set(to_predict['movie_id'])) )

        results = []
        for row in to_predict.itertuples(index=False):
            user_id = row[0]
            movie_id = row[1]
            results.append(predictions.loc[user_id, movie_id] )    
        if(len(results) == 0):
            print ('kaboom')
        return results
    
     
    def score(self, X, y):
        """Returns the MAE.
        
        It will return the MAE for the predictions of X comparing it to y which
        the ral values. The MAE is returned in negative  because
        considers a bigger value as a better value.
        
        Args:
            
            X(pd.DataFrame) : The input data. It has two columns : 'user_id' and
                'movie_id'
                
            y(pd.DataFrame): The real ratings for the values in X. It has 1
                columns: 'rating'
                
        Returns:
        
            float: The MAE of the predictions of X.
        """                
        if(len(y) == 0):
            return np.nan
        
        predictions = self.predict(X)
        predictions = np.nan_to_num(predictions)         
        MAE = sklearn.metrics.mean_absolute_error(y,predictions)
        
        #I return the negative value of the MAE since sklearn considers a bigger value as a better value.
        return -MAE