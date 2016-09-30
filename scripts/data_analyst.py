import matplotlib
import matplotlib.pyplot as plt
from data_io import DataReader


class DataAnalyst(object):
    """Provides analytics of the data.
    """
    def __init__(self):
        self.report_metrics = ['Ratings_in_subset', 'Neighbors_count' , 'MAE',  'Throughput', 'Test_set_percentage' ]

    
    def provide_analysis(self, data_frame = None):
        """Provides visualization of the data's distribution and other statistic
             info.
        
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
        sub_plot.set_title('Ratings data distribution')
        sub_plot.bar(X, Y, align='center')
        sub_plot.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))) 
        
        
        plt.xlabel('Ratings', size=34, weight='bold')
        plt.ylabel('Frequency', size=34, weight='bold')
        
        plt.show()
        
    def simple_graph(self, xlabel,ylabel, xdata, ydata, figure = None, label= '', line_format = 'b-o', legend_loc = 'upper right'):
        """Utility function to plot a line.
        
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
                
            legend_loc (string): Location of the legend.
            
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
        
                
    def multiple_lines_plot(self, results, xlabel, ylabel, x_data_field = None, y_data_field = None, group_by_field=None, figure_title='', line_legend_tpl= 'line for {}', figure = None, line_format = 'b-o', legend_loc = 'upper right'):
        """ Utility function to plot multiple lines in the same axes.
        
        Args:
            
            xlabel (string) : Label in X axis.
            
            ylabel (string) : Label in Y axis.
            
            x_data_field (str) : Name of the pandas.DataFrame column to use as X in
                plot.
            
            y_data_field (st) : Name of the pandas.DataFrame column to use as Y in
                plot.
            
            group_by_field (str): Name of the pandas.DataFrame column to group
                by in order to get the different groups that will represent each
                line.   
                         
            figure_title (str): Title in the figure.
            
            figure (matplotlib.figure.Figure): The figure where to plot. A new one is
                created if is None.
    
            line_legend_tpl (str) = Template string for the legend. {} will get
                replaced by the value in group_by_field argument.                                
            
            line_format (string): String with line format and color code a la
                matplotlib.
                
            legend_loc (string): Location of the legend.
            
        """
        figure = None
    
        group_by_values = results[group_by_field].unique()
        line_formats = ['r-o','b-o','k-o','r-o','g-o','c-o', 'm-o', 'r-o','b-o','k-o','r-o','g-o','c-o', 'm-o']
        for i, group_by_value in enumerate(group_by_values):
            values_for_group = results[results[group_by_field] == group_by_value]
            line_label = line_legend_tpl.format(group_by_value)
            figure = self.simple_graph(xlabel, ylabel, values_for_group[x_data_field], values_for_group[y_data_field], figure = figure, label=line_label, line_format =line_formats[i], legend_loc = legend_loc)
        
        plt.legend(loc=legend_loc, prop={'size': 20})            
        
        if(figure is not None):
            figure.suptitle(figure_title)
            plt.show()
        
    def graph_size_sensitivities(self,cv_results, test_result):
        
        """Generate graphs showing results of first run.
        
        First run consist in running with a fixed Neighbors_count value
        to see how the MAE and throughput behaves when changing the test set
        percentage and model size.
        
        Args:
        
            cv_results(pandas.DataFrame): A DataFrame with the columns :'Ratings_in_subset', 
                'Neighbors_count' , 'MAE',  'Throughput'. It has the value of 
                the measurements. It has the training errors and other metrics.
            
            test_result(pandas.DataFrame): A DataFrame with the columns :'Ratings_in_subset', 
                'Neighbors_count' , 'MAE',  'Throughput'. It has the value of 
                the measurements. It has the test errors and other metrics.   
                
        """                             
          
        #Test_set_percentange vs MAE                    
        self.multiple_lines_plot(test_result, "Test_set_percentage", "MAE", "Test_set_percentage", "MAE", group_by_field="Ratings_in_subset", line_legend_tpl = "Ratings in subset: {}", figure_title= 'Test_percentage vs MAE at each test/train split', legend_loc = 'upper right')                                                       
                                
        #Ratings_in_subset vs MAE        
        self.multiple_lines_plot(test_result, "Ratings_in_subset", "MAE", "Ratings_in_subset", "MAE", group_by_field="Test_set_percentage", line_legend_tpl = "Test set percentage: {}", figure_title= 'Ratings_in_subset vs MAE at each test/train split', legend_loc = 'lower right')
        
        #Ratings_in_subset vs Throughput at test_set_percentage
        self.multiple_lines_plot(test_result, "Ratings_in_subset","Throughput", 'Ratings_in_subset', 'Throughput', group_by_field='Test_set_percentage', line_legend_tpl = "Test set percentage: {}", figure_title= 'Ratings_in_subset vs Throughput at each test/train split', legend_loc = 'lower right')
        
        
                                        
                                         
        plt.show()
        
    def graph_neighbors_sensitivity(self, cv_results):
        """Generate graphs showing results of the second run.
        
        Second run consist in running with multiple values of Neighbors_count 
        to see how the MAE and throughput behaves while keeping the test set percentage 
        and model size fixed.
        
        Args:
            cv_results(pandas.DataFrame): A DataFrame with the columns :'Ratings_in_subset', 
                'Neighbors_count' , 'MAE',  'Throughput'. It has the value of 
                the measurements.
        """                             
                 
        #Neighbors_count vs MAE
        self.simple_graph(xlabel="Neighbors_count", ylabel="MAE", xdata=cv_results['Neighbors_count'], ydata=cv_results['Neighbors_count'], label="Neighbors_count vs MAE")