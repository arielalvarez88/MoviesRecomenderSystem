import matplotlib
import matplotlib.pyplot as plt
from data_io import DataReader


class DataAnalyst(object):
    """Provides analytics of the data.
    """
    def __init__(self):
        self.report_metrics = ['Ratings_in_subset', 'Movies_count', 'Neighbors_count' , 'MAE',  'Throughput']

    
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
        
    def simple_graph(self, xlabel,ylabel, xdata, ydata, figure = None,label= '', line_format = 'b-o'):
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
        
        

    def compare_ratings_in_subset(self, results):
        
        figure = None

        #Ratings_in_subset vs MAE
        movies_subsets = results['Ratings_in_subset'].unique()
        line_formats = ['r-o','b-o','k-o','r-o','g-o']
        for i, movies_subset in enumerate(movies_subsets):
            values_for_subset = results[results['Ratings_in_subset'] == movies_subset]
            line_label = '# of movies = {}'.format(movies_subset)
            figure = self.simple_graph("Ratings_in_subset", "MAE", values_for_subset['Ratings_in_subset'], values_for_subset['MAE'], figure = figure, label=line_label, line_format =line_formats[i])
        
        plt.legend()            
        
        figure.suptitle("Ratings_in_subset vs MAE for different movies subsets")
        plt.show()
        
    def graph_results(self,results,all_movies_count):
        
        """Generate graphs showing results
        Args:
            dict: The results containing the following values.
        """                             
        
        #Ratings in subset vs MAE                   
        self.compare_ratings_in_subset(results) 
        
        #K vs MAE         
        self.simple_graph("Number of Neighbors","MAE", results['Neighbors_count'], results['MAE'])
                                
        #Train-Percentage vs MAE 
        self.simple_graph("Ratings_in_subset","MAE", results['Ratings_in_subset'], results['MAE'])
        
        #K vs Throughput 
        self.simple_graph("Number of Neighbors","Throughput", results['Neighbors_count'], results['Throughput'])
                                
         
         

        plt.show()