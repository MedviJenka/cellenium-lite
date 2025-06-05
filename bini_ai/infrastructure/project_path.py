import os

# Full project path which used to strip to get a global path
abstract_dir = os.path.dirname(os.path.abspath(__file__))

# Automation
GLOBAL_PATH = abstract_dir.split('qasharedinfra')[0][:-1]
TESTS = fr'{GLOBAL_PATH}\tests'
BINI_LOGS = fr'{GLOBAL_PATH}\tests\logs\logs.log'
SAMPLES = fr'{GLOBAL_PATH}\core\data\samples.xlsx'
ps_dir = fr'{GLOBAL_PATH}\qasharedinfra\infra\smarttap\selenium\utils\powershell\run_policy.ps1'
downloads_dir = os.path.expanduser("~\\Downloads")
BINI = fr'{GLOBAL_PATH}\qasharedinfra\infra\common\services\bini_ai\.env'
BINI_RESULTS = fr'{GLOBAL_PATH}\qasharedinfra\infra\common\services\bini_ai\results'
