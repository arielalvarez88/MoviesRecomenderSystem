from data_formatter import DataFormatter
from data_analyst import DataAnalyst
from data_io import DataReader
from metrics_calc import MetricsCalc

dataframe = DataReader().read_ratings_as_df()
analyst = DataAnalyst()
#analyst.provide_analysis()

#data_formatter  = DataFormatter()
#data_formatter.ori_data_to_json_files(dataframe)

metrics_calc = MetricsCalc()

all_movies_count = len(dataframe['movie_id'].unique())

results = metrics_calc.grid_search(dataframe, [all_movies_count],[0.8], [10,20,30,40,50,60])
#results = metrics_calc.grid_search(dataframe, [0.0001,0.001,0.01],[0.2,0.4,0.6,0.8], [30])

analyst.graph_results(results)
