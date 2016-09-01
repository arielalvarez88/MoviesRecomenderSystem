

""" Folder data\raw\recipes_reviews has files with the recipe_id as the name of the file.
Inside each files are the reviews for that particular recipe. That is the data I got from the BigOven.com. """


import ConfigParser
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as pl
from datetime import datetime

from scipy.stats import pearsonr
from rope.refactor import similarfinder
import random

configParser = ConfigParser.ConfigParser()
configParser.read("./config.txt")
data_folder = configParser.get("config", "data_folder")
ratings_file = configParser.get("config", "original_rating_file")
ratings_file_path = "{}/{}".format(data_folder, ratings_file)

all_data = pd.read_table(ratings_file_path, sep="::", skiprows=0, header=None, names=["user_id", "movie_id", "rating", "timestamp"])

train_percentages = [0.3, 0.5, 0.7, 1]
k_vals = [10, 20, 30, 40]
test_columns = ['Train', 'K' , 'MAE', 'Neighbors Time', '' , 'Throughput']
all_movies_ids = all_data['movie_id'].unique()

results = pd.DataFrame(columns=test_columns)

matrix_J_U = all_data.pivot(columns="user_id", index="movie_id", values="rating")
movies_ids = matrix_J_U.index.values 

matrix_J_U = matrix_J_U.values

time_neighbors = 0
user_count = matrix_J_U.shape[1] 
product_count = matrix_J_U.shape[0]
range_of_rows = range(0, product_count)
neighbors_dict = {}

def save_to_dict(id_i,id_j,pc):
    
    id_i = str(id_i)
    id_j = str(id_j)
    
    neighbors_dict[id_i] = neighbors_dict[id_i] if id_i in neighbors_dict else {}
    neighbors_dict[id_j] = neighbors_dict[id_j] if id_j in neighbors_dict else {}
     
    neighbors_dict[id_i][id_j] = pc
    neighbors_dict[id_j][id_i] = pc 

def find_nearest_neighbors(matric_J_U):
    
    init_time = datetime.now()
    
    for i in range(0, matrix_J_U.shape[0]):
        for j in range(i+1, matrix_J_U.shape[0]):
            pearson_ij = pearsonr(matrix_J_U[i], matrix_J_U[j])
            movie_i_id = movies_ids[i]            
            movie_j_id = movies_ids[j]
            save_to_dict(movie_i_id,movie_j_id,pearson_ij)           
            
    timeDelta = init_time - datetime.now() 
    return  (neighbors_dict, timeDelta.total_seconds())      



    

for train_percentage in train_percentages:
    for k_val in k_vals:
        subset_rows = int(matrix_J_U.shape[0] * train_percentage)
                
        movies_subset = matrix_J_U[ random.sample(range_of_rows,  subset_rows) , :]
        neighbors_dict, time_neighbors  = find_nearest_neighbors(movies_subset)
        
        #write_to_files(neighbors_dict)
        results.append({"Train" : train_percentage, "Neighbors Time" : time_neighbors} , ignore_index=True)
        break
    break


print "Neighbors:",neighbors_dict
print results


        


    






def visualize_dist (df):
    # Visualization of data
    ratings_dist = df.groupby("rating")
    X = ratings_dist.groups.keys()
    Y = ratings_dist.count()['movie_id']
    
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 34}
    
    matplotlib.rc('font', **font)
    
    sub_plot = pl.subplot()
    sub_plot.bar(X, Y, align="center")
    sub_plot.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))) 
    
    
    pl.xlabel("Ratings", size=34, weight="bold")
    pl.ylabel("Frequency", size=34, weight="bold")
    
    pl.show()
    
    print(df['user_id'])
    print(df.describe())
    
        
        
    
    
