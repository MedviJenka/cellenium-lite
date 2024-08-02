import os


# Full project path which used to strip to get global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))


GLOBAL_PATH = abstract_dir.split('core')[0][:-1]
TESTS = fr'{GLOBAL_PATH}\tests'
BINI_LOGS = fr'{GLOBAL_PATH}\logs\logs.log'
SAMPLES = fr'{GLOBAL_PATH}\core\data\samples.xlsx'
