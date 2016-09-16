import matplotlib
import matplotlib.pyplot as plt
from data_io import DataReader


class DataAnalyst(object):
    """Provides analytics of the data.
    """
    def __init__(self):
        self.report_metrics = ['Train_percentage', 'Movies_count', 'K_neighbors' , 'MAE', 'PC_calc_time', 'Throughput', "Time_MAE"]

    
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
        
    def simple_graph(self, xlabel,ylabel, xdata, ydata, figure = None,label= '', line_format = 'b-'):
        """Utility function to plot in a figure.
        
        Args:
            
            xlabel (string) : Label in X axis.
            
            ylabel (string) : Label in Y axis.
            
            xdata (list) : Data for X axis.
            
            ydata (list) : Data for Y axis.
            figure (matplotlib.figure.Figure): The figure where to plot. A new one is
                created if is None.
                
            label (string) : Title of the figure.
            
            line_format (string): String with line format and color code a la
                matplotlib.
        Return:
            matplotlib.figure.Figure: The figure where the plot was done.
        """
        fig = plt.figure() if figure is None else figure
        fig.add_subplot(111, xlabel = xlabel, ylabel=ylabel)        
        plt.plot(xdata,ydata,line_format,figure=fig, label=label)        
        return fig
        
        

    def compare_train_percentage(self, results):
        
        figure = None

        #MAE vs Train_percentage
        movies_subsets = results['Movies_count'].unique()
        line_formats = ['r-','b-','k-','r-','g-']
        for i, movies_subset in enumerate(movies_subsets):
            values_for_subset = results[results['Movies_count'] == movies_subset]
            line_label = '# of movies = {}'.format(movies_subset)
            figure = self.simple_graph("Train_percentage", "MAE", values_for_subset['Train_percentage'], values_for_subset['MAE'], figure = figure, label=line_label, line_format =line_formats[i])
        
        plt.legend()            
        
        figure.suptitle("Train_percentage vs MAE for different movies subsets")
        plt.show()
        
    def graph_results(self,results):
        
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