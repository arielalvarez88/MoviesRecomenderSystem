from datetime import datetime

class PearsonCorrelationComputer(object):
    """Calculate Pearson Correlation between movies.            
    """    
            
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
        
        print "Time spent in neighbors calculations {}".format(time_neighbors)
        return  PC_matrix, time_neighbors
        
