from data_formatter import DataFormatter
from  pearson_correlation_computer import PearsonCorrelationComputer
from data_analyst import DataAnalyst

from data_io import DataReader

dataframe = DataReader().read_ratings_as_df()
#analyst = DataAnalyst()
#analyst.provide_analysis()

#data_formatter  = DataFormatter()
#data_formatter.ori_data_to_json_files(dataframe)

neighbors_calc = PearsonCorrelationComputer()
neighbors_calc.compute_pc(dataframe,[0.1])
