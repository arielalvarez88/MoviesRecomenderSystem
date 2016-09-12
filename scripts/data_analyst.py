import matplotlib
import matplotlib.pyplot as plt
from data_io import DataReader


class DataAnalyst(object):
    """Provides analytics of the data.
    """
    def __init__(self):
        self.report_metrics = ['Train_percentage', 'K_neighbors' , 'MAE', 'PC_calc_time', 'Throughput', "Time_MAE"]

    
    def provide_analysis(self, data_frame = None):
        """Provides visualization of the data's dist. and the data's statistic info.
        
        Args:
            data_frame (pandas.DataFrame): Original data.
        """
        if(data_frame is None):
            data_frame = DataReader().read_ratings_as_df()
            
        self.visualize_dist(data_frame)
        print(data_frame['user_id'])
        print(data_frame.describe())

    def visualize_dist (self,df=None):
        
        """Provides visualization of the distribution of the data.
        
        Args:
            data_frame (pandas.DataFrame): Original data.
        """
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
        
        sub_plot = plt.subplot()
        sub_plot.bar(X, Y, align='center')
        sub_plot.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) 
        
        
        plt.xlabel('Ratings', size=34, weight='bold')
        plt.ylabel('Frequency', size=34, weight='bold')
        
        plt.show()
        
    def simple_graph(self, xlabel,ylabel, xdata, ydata):
        fig = plt.figure()
        fig.add_subplot(111, xlabel = xlabel, ylabel=ylabel)        
        plt.plot(xdata,ydata,figure=fig)
        
        
    def graph_results(self,results):
        print "Brumm brumm"
        """Generate graphs showing results
        Args:
            dict: The results containing the following values.
        """        
        
        #K vs MAE         
        self.simple_graph("Number of Neighbors","MAE", results['K_neighbors'], results['MAE'])
                                
        #Train-Percentage vs MAE 
        self.simple_graph("Train_percentage","MAE", results['Train_percentage'], results['MAE'])
        
        #K vs Throughput 
        self.simple_graph("Number of Neighbors","Throughput", results['K_neighbors'], results['Throughput'])
        
        #Train-Precentage vs PC_calc_time
        self.simple_graph("Train_percentage","PC_calc_time", results['Train_percentage'], results['PC_calc_time'])
        
        #Train_percentage vs Time_MAE 
        self.simple_graph("Train_percentage","Time_MAE", results['Train_percentage'], results['Time_MAE'])
         

        plt.show()