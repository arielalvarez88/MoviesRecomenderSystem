from data_io import DataReader
import operator
from numpy.core.test_rational import denominator, numerator

class NotEnoughInfoException(Exception):
    def __init___(self, dErrorArguments):
        Exception.__init__(self,"There is no information to predict the movie. The user has to have ratings for at least 1 of the k neighbors.")
        self.dErrorArguments = dErrorArguments

class Predictor(object):
    """Class to recommend and predict movie ratings for users.
    
    Attributes:
        __k (int) : The number of neighbors to take into account for predicitons
            and suggestions.
                
    """
    def __init__(self, k=5):
      
        self.__k = k
      
        self.reader = DataReader()

        
    
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
        
        ordered_pcs = sorted(pcs_with_others.iteritems(), key=operator.itemgetter(1))
        
        k_neighbors = ordered_pcs[ self.k * -1 : -1]
        
        return dict(k_neighbors)
        
    def predict(self, user_id, movie_id):
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
       
        
        for movie in k_neighbors_rated_by_user:
            PC = k_neighbors[movie]
            user_rating = user_data['ratings'][movie]
            numerator += PC * int(user_rating)
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
    
    def get_k(self):
        return self.__k


    def set_k(self, value):
        self.__k = value


    def del_k(self):
        del self.__k

    k = property(get_k, set_k, del_k, "k's docstring")
 