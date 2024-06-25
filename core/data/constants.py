import os


# Full project path which used to strip to get global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))


GLOBAL_PATH = abstract_dir.split('core')[0][:-1]
TESTS = fr'{GLOBAL_PATH}\tests'
LOGS = fr'{GLOBAL_PATH}\core\logs\data.log'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
IMAGES = fr'{GLOBAL_PATH}\core\data\images'

