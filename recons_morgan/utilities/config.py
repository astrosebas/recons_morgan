# use dictionary to store config, makes it easier to grep for config usage
config_data = {}
config_type = {}
# find daily folder
# root folder to look in.
# pipeline looks for folder with data as YYYYMMDD (e.g. 20180723) to find
# folder with daily exposure. Exposures folder should have the date of beggining of
# exposure
#config_data['dataset_root'] = "datasets/"
config_data['dataset_root'] = "/nfs/morgan/chiron/tous/mir7/fitspec"
config_type['dataset_root'] = str
config_data['working_directory'] = "datasets/"
config_type['working_directory'] = str
# execution Log level, controls how much is printed and saved to log.
# 'debug' for full log (is pretty heavy)
# anything else for normal warning and debug log
config_data['log_level'] = 'warn'
config_type['log_level'] = str
# target file
# get targets list from this file
config_data['targets_file'] = "./templates/targets.json"
config_type['targets_file'] = str
config_data['secondary_targets_file'] = ""
config_type['secondary_targets_file'] = str