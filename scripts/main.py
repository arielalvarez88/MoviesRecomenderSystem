from data_formatter import DataFormatter
from data_analyst import DataAnalyst
from data_io import DataReader
from metrics_calc import MetricsCalc
""" This module runs the whole process in order. 

"""


dataframe = DataReader().read_ratings_as_df()

analyst = DataAnalyst()
#analyst.provide_analysis()

#data_formatter  = DataFormatter()
#data_formatter.ori_data_to_json_files(dataframe)

metrics_calc = MetricsCalc()

all_movies_count = len(dataframe['movie_id'].unique())

results = metrics_calc.grid_search(data=dataframe, ratings_in_subsets=[1000000], neighbors_counts=[6000],k_fold=3)


analyst.graph_results(results,all_movies_count)
