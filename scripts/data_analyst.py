import matplotlib
import matplotlib.pyplot as plt
from data_io import DataReader


class DataAnalyst(object):
    """Provides analytics of the data.
    """
    def __init__(self):
        self.report_metrics = ['Ratings_in_subset', 'Neighbors_count' , 'MAE',  'Throughput', 'Test_set_percentage' ]

    
    def provide_analysis(self, data_frame = None):
        """Provides visualization of the data's distribution and other statistic info.
        
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
        """Utility function to plot a figure.
        
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
        
        font = {'family' : 'normal',    
                'weight' : 'bold',
                'size'   : 34}
        
        matplotlib.rc('font', **font)
        
        fig = plt.figure() if figure is None else figure
        fig.add_subplot(111, xlabel = xlabel, ylabel=ylabel)
        plt.xlabel( xlabel, size=34, weight='bold')
        plt.ylabel( ylabel, size=34, weight='bold')
                
        plt.plot(xdata,ydata,line_format,figure=fig, label=label)        
        return fig
        
        

    def splits_vs_mae(self, results):
        """ Visualize the test percentages vs MAE for each subset of the data.
        
        Args :
            
            results (pandas.DataFrame): A DataFrame with the measurements.
            
        """
        figure = None

        #Ratings_in_subset vs MAE
        ratings_subsets = results['Ratings_in_subset'].unique()
        line_formats = ['r-o','b-o','k-o','r-o','g-o']
        for i, ratings_subset in enumerate(ratings_subsets):
            values_for_subset = results[results['Ratings_in_subset'] == ratings_subset]
            line_label = '# of ratings = {}'.format(ratings_subset)
            figure = self.simple_graph("Test_set_percentage", "MAE", values_for_subset['Test_set_percentage'], values_for_subset['MAE'], figure = figure, label=line_label, line_format =line_formats[i])
        
        plt.legend()            
        
        if(figure is not None):            
            figure.suptitle("Test_set_percentage vs MAE for different ratings subsets")
        plt.show()
        
    def multiple_lines_plot(self, results, xlabel, ylabel, x_data_field = None, y_data_field = None, group_by_field=None, figure_title='', line_legend_tpl= 'line for {}', figure = None,label= '', line_format = 'b-o' ):
        """ Visualize the test percentages vs MAE for each subset of the data.
        
        Args :
            
            results (pandas.DataFrame): A DataFrame with the measurements.
            
        """
        figure = None
    
        group_by_values = results[group_by_field].unique()
        line_formats = ['r-o','b-o','k-o','r-o','g-o']
        for i, group_by_value in enumerate(group_by_values):
            values_for_group = results[results[group_by_field] == group_by_value]
            line_label = line_legend_tpl.format(group_by_value)
            figure = self.simple_graph(xlabel, ylabel, values_for_group[x_data_field], values_for_group[y_data_field], figure = figure, label=line_label, line_format =line_formats[i])
        
        plt.legend()            
        
        if(figure is not None):
            figure.suptitle(figure_title)
            plt.show()
        
    def graph_size_sensitivities(self,cv_results, test_result):
        
        """Generate graphs showing results.
        
        Args:
            results(pandas.DataFrame): A DataFrame with the columns :'Ratings_in_subset', 
                'Neighbors_count' , 'MAE',  'Throughput'. It has the value of 
                the measurements.
        """                             
          
        #Test_set_percentange vs MAE
        self.splits_vs_mae(test_result)                                                       
                                
        #Ratings_in_subset vs MAE
        self.simple_graph("Ratings_in_subset","MAE", test_result['Ratings_in_subset'], test_result['MAE'])
        
        #Ratings_in_subset vs Throughput at test_set_percentage
        self.multiple_lines_plot(test_result, "Ratings_in_subset","Throughput", 'Ratings_in_subset', 'Throughput', group_by_field='Test_set_percentage', line_legend_tpl = "Test set percentage: {}", figure_title= 'Ratings_in_subset vs Throughput at each test/train split')
        
        
                                        
                                         
        plt.show()
        
    def graph_neighbors_sensitivity(self, cv_results):
        
        #Neighbors_count vs MAE         
        self.simple_graph("Number of Neighbors","MAE", cv_results['Neighbors_count'], cv_results['MAE'])