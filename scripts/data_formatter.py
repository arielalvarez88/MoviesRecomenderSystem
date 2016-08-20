import ConfigParser
import copy
import json

configParser = ConfigParser.ConfigParser()
configParser.read("./config.txt")
break_after = 1000
break_after_limit = False

k_neighbors = configParser.get("config", 'k_neighbors')


rating_file_path = "{}/{}".format(configParser.get("config", "data_folder"), configParser.get("config", "original_rating_file") )
output_movies_folder = "{}/{}".format(configParser.get("config", "data_folder"), configParser.get("config", "output_movies_folder"))
output_users_folder = "{}/{}".format(configParser.get("config", "data_folder"), configParser.get("config", "output_users_folder"))

rating_file_order = ["user_id","movie_id","rating","timestamp"]

movieFileTpl = {
                
    "mean_rating" : "3.3",

    "ratings" : {
             
                "user_id" : "3.3"
    },
                
    "k_neighbors": {
            "movie_id" : "3.3 (weight)"
    }
                
}



userFileTpl = {
    "ratings": {
        "movie-id" : 2.2
    }
}

all_movie_data = {
              
}

all_user_data = {

}


def read_original_data(all_movie_data, all_user_data):    
    with open(rating_file_path) as infile:
        for i, line in enumerate(infile):
            vals = line.split("::")
            
            vals = dict( zip(rating_file_order, vals) )
            user_id = vals['user_id']
            movie_id = vals['movie_id']
                    
            movie_data =   all_movie_data[movie_id] if movie_id in all_movie_data else copy.deepcopy(movieFileTpl) 
            user_data = all_user_data[user_id] if user_id in all_user_data else copy.deepcopy(userFileTpl) 
            
                   
            movie_data['ratings'][user_id] = vals['rating']
            
            user_data['ratings'] [movie_id] = vals['rating']
            
            all_user_data[user_id] = user_data
            all_movie_data[movie_id] = movie_data       
            if(i >= break_after and break_after_limit):
                break;


def write_to_file (data_dict, output_folder):
    print(data_dict)
    for key, value in data_dict.iteritems():
        file = open("{}/{}.{}".format(output_folder, key, 'json'),'w+')
        json.dump(value, file)
        file.close()
        
            
read_original_data(all_movie_data, all_user_data)
write_to_file(all_user_data, output_users_folder)
write_to_file(all_movie_data, output_movies_folder)

                
print all_movie_data
print all_user_data
            
