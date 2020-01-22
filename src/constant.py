# TODO: check RAM use
# TODO: cash out automatically
# TODO: argv - [alex|boris]

from datetime import datetime as dt
from os.path import join, dirname

PROJECT_ROOT = dirname(dirname(__file__))

def read_credentials():
    user = ''
    password = ''
    with open(join(PROJECT_ROOT, 'resources', 'credentials.txt'), 'r', encoding='utf-8') as file:
        for line in file:
            pair = line.strip().split(':')
            if pair[0].strip() == 'user':
                user = pair[1]
            if pair[0].strip() == 'pass':
                password = pair[1]
    return user, password

BET_HOME         = 'https://www.bet365.com/bg'
STATISTICS_URL   = 'https://www.bet365.com/extra/bg/?FixtureId=0&CompetitionId=20120653&SearchPath=fixture&SportDesc=%25d0%2592%25d0%25b8%25d1%2580%25d1%2582%25d1%2583%25d0%25b0%25d0%25bb%25d0%25b5%25d0%25bd%2b%25d1%2584%25d1%2583%25d1%2582%25d0%25b1%25d0%25be%25d0%25bb&Teamid=&LanguageId=19&Todate=12%2f05%2f2019+23%3a59&Fromdate=05%2f05%2f2019+00%3a00&Period=3&ChallengeId=0&SportId=146&Zoneid=33'
credentials      = read_credentials()
USER             = credentials[0]
PASS             = credentials[1]
WINDOW_WAIT_TIME = 20
PROFIT           = 0.25

# --paths--
LOG_PATH  = join(PROJECT_ROOT, 'log', 'log_{}.log'.format(str(dt.now().date())))
LOG_DIR   = join(PROJECT_ROOT, 'log')
STATS_LOG = join(PROJECT_ROOT, 'src', 'statistics', 'output', 'stats.log')
INFO      = join(PROJECT_ROOT, 'src', 'statistics', 'output', 'info.txt')
X12       = join(PROJECT_ROOT, 'src', 'statistics', 'output', 'x12.txt')
