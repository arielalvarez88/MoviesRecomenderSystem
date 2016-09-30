""" This module runs the whole process in order. 

"""

from data_analyst import DataAnalyst
from data_formatter import DataFormatter
from data_io import DataReader
from metrics_calc import MetricsCalc
import pandas as pd

dataframe = DataReader().read_ratings_as_df()

analyst = DataAnalyst()
analyst.provide_analysis()

metrics_calc = MetricsCalc()

all_ratings_count = dataframe.shape[0] 
best_split = 0

report_columns = ['Ratings_in_subset',  'MAE', 'Throughput', 'K_fold', "Neighbors_count" , 'Test_set_percentage']

cv_results_all = pd.DataFrame(columns=report_columns)
test_set_results_all = pd.DataFrame(columns=report_columns)


#Around 1 hr to run in my pc (Intel core i7, 16gb of ram).
def determine_best_split():
    cv_results, test_set_results = metrics_calc.grid_search(data=dataframe, ratings_in_subsets=[50000, 100000, 150000, 200000],test_set_percentages=[0.3, 0.5, 0.8], neighbors_counts=[100],k_fold=3)
    cv_results_all.append(cv_results, ignore_index=True)
    test_set_results_all.append(test_set_results, ignore_index=True)
    analyst.graph_size_sensitivities(cv_results, test_set_results)

#Around 1 hr to run in my pc (Intel core i7, 16gb of ram). 
def train_model(best_split):
    cv_results, test_set_results = metrics_calc.grid_search(data=dataframe, ratings_in_subsets=[all_ratings_count],test_set_percentages=[best_split], neighbors_counts=[25,50,75,100,125,150,175,200,6000],k_fold=3)
    cv_results_all.append(cv_results, ignore_index = True)                       
    test_set_results_all.append(test_set_results, ignore_index = True)
    analyst.graph_neighbors_sensitivity(test_set_results_all)
    
                

best_split = determine_best_split()
train_model(0.3)