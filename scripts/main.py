from data_formatter import DataFormatter
from data_analyst import DataAnalyst
from data_io import DataReader
from metrics_calc import MetricsCalc

dataframe = DataReader().read_ratings_as_df()
analyst = DataAnalyst()
analyst.provide_analysis()

#data_formatter  = DataFormatter()
#data_formatter.ori_data_to_json_files(dataframe)



metrics_calc = MetricsCalc()

results = metrics_calc.grid_search(dataframe,[0.1], [2])

analyst.show_results(results)