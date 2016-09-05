import matplotlib

from data_io import DataReader
import matplotlib.pyplot as pl

"""Provides analytics of the data.
"""
class DataAnalyst(object):
    """Provides visualization of the data´s dist. and the data´s statistic info.
    
    Args:
        data_frame (pandas.DataFrame): Original data.
    """
    def provide_analysis(self, data_frame = None):
        if(data_frame is None):
            data_frame = DataReader().read_ratings_as_df()
            
        self.visualize_dist(data_frame)
        print(data_frame['user_id'])
        print(data_frame.describe())

    """Provides visualization of the distribution of the data.
    
    Args:
        data_frame (pandas.DataFrame): Original data.
    """
    def visualize_dist (self,df=None):
        
        if(df is None):
            df = DataReader().read_ratings_as_df()
            
        # Visualization of data
        ratings_dist = df.groupby('rating')
        X = ratings_dist.groups.keys()
        Y = ratings_dist.count()['movie_id']
        
        font = {'family' : 'normal',
                'weight' : 'bold',
                'size'   : 34}
        
        matplotlib.rc('font', **font)
        
        sub_plot = pl.subplot()
        sub_plot.bar(X, Y, align='center')
        sub_plot.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) 
        
        
        pl.xlabel('Ratings', size=34, weight='bold')
        pl.ylabel('Frequency', size=34, weight='bold')
        
        pl.show()