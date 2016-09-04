import copy


class DataFormatter(object):
    
    def __init__(self, break_after = 1000, break_after_limit=False):
        self.break_after = self.break_after
        self.break_after_limit = self.break_after_limit
        
        
       
        
        self.rating_file_order = ["user_id","movie_id","rating","timestamp"]
        
        self.movie_file_tpl = {
                        
            "mean_rating" : "3.3",
        
            "ratings" : {
                     
                        "user_id" : "3.3"
            },
                        
            "k_neighbors": {
                    "movie_id" : "3.3 (weight)"
            }
                        
        }
        
        
        
        self.movie_file_tpl = {
            "ratings": {
                "movie-id" : 2.2
            }
        }
        
        self.all_movie_data = {
                      
        }
        
        self.all_user_data = {
        
        }
    
        
    
    def read_original_data(self):    
        with open(self.rating_file_path) as infile:
            for i, line in enumerate(infile):
                vals = line.split("::")
                
                vals = dict( zip(self.rating_file_order, vals) )
                user_id = vals['user_id']
                movie_id = vals['movie_id']
                        
                movie_data =   self.all_movie_data[movie_id] if movie_id in self.all_movie_data else copy.deepcopy(self.movie_file_tpl) 
                user_data = self.all_user_data[user_id] if user_id in self.all_user_data else copy.deepcopy(self.movie_file_tpl) 
                
                       
                movie_data['ratings'][user_id] = vals['rating']
                
                user_data['ratings'] [movie_id] = vals['rating']
                
                self.all_user_data[user_id] = user_data
                self.all_movie_data[movie_id] = movie_data       
                if(i >= self.break_after and self.break_after_limit):
                    break;
    
   
    def ori_data_to_json_files(self):
        self.read_original_data()
        self.write_to_json_files(self.all_user_data, self.output_users_folder)
        self.write_to_json_files(self.all_movie_data, self.output_movies_folder)      
                
    
    
                
