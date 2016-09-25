from ConfigParser import ConfigParser
class Config(object):
    
    def __init__(self):
        configParser = ConfigParser()
        configParser.readfp(open('config.txt'))
        self.__data_folder = configParser.get('config', 'data_folder')
        self.__rating_file_path = "{}/{}".format(configParser.get("config", "data_folder"), configParser.get("config", "original_rating_file") )
        self.__output_movies_folder = "{}/{}".format(configParser.get("config", "data_folder"), configParser.get("config",'output_movies_folder'))
        self.__output_users_folder = "{}/{}".format(configParser.get("config", "data_folder"), configParser.get("config",'output_users_folder'))
        self.__users_folder_path = configParser.get("config",'users_folder_path')
        self.__items_folder_path= configParser.get('config', 'items_folder_path')
        self.__ratings_file = configParser.get('config', 'original_rating_file')
        self.__ratings_file_path = '{}/{}'.format(self.__data_folder, configParser.get('config', 'original_rating_file') )

    def get_users_folder_path(self):
        return self.__users_folder_path


    def set_users_folder_path(self, value):
        self.__users_folder_path = value


    def del_users_folder_path(self):
        del self.__users_folder_path


    def get_rating_file_path(self):
        return self.__rating_file_path


    def get_output_movies_folder(self):
        return self.__output_movies_folder


    def get_output_users_folder(self):
        return self.__output_users_folder


    def get_data_folder(self):
        return self.__data_folder


    def get_items_folder_path(self):
        return self.__items_folder_path


    def get_ratings_file(self):
        return self.__ratings_file


    def get_ratings_file_path(self):
        return self.__ratings_file_path


    def set_rating_file_path(self, value):
        self.__rating_file_path = value


    def set_output_movies_folder(self, value):
        self.__output_movies_folder = value


    def set_output_users_folder(self, value):
        self.__output_users_folder = value


    def set_data_folder(self, value):
        self.__data_folder = value


    def set_items_folder_path(self, value):
        self.__items_folder_path = value


    def set_ratings_file(self, value):
        self.__ratings_file = value


    def set_ratings_file_path(self, value):
        self.__ratings_file_path = value


    def del_rating_file_path(self):
        del self.__rating_file_path


    def del_output_movies_folder(self):
        del self.__output_movies_folder


    def del_output_users_folder(self):
        del self.__output_users_folder


    def del_data_folder(self):
        del self.__data_folder


    def del_items_folder_path(self):
        del self.__items_folder_path


    def del_ratings_file(self):
        del self.__ratings_file


    def del_ratings_file_path(self):
        del self.__ratings_file_path

    rating_file_path = property(get_rating_file_path, set_rating_file_path, del_rating_file_path, "rating_file_path's docstring")
    output_movies_folder = property(get_output_movies_folder, set_output_movies_folder, del_output_movies_folder, "output_movies_folder's docstring")
    output_users_folder = property(get_output_users_folder, set_output_users_folder, del_output_users_folder, "output_users_folder's docstring")
    data_folder = property(get_data_folder, set_data_folder, del_data_folder, "data_folder's docstring")
    items_folder_path = property(get_items_folder_path, set_items_folder_path, del_items_folder_path, "items_folder_path's docstring")
    ratings_file = property(get_ratings_file, set_ratings_file, del_ratings_file, "ratings_file's docstring")
    ratings_file_path = property(get_ratings_file_path, set_ratings_file_path, del_ratings_file_path, "ratings_file_path's docstring")
    users_folder_path = property(get_users_folder_path, set_users_folder_path, del_users_folder_path, "users_folder_path's docstring")
       