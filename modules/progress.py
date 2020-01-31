# Deep Learning Pipeline
# HYPE Industries
import sys;

# Progress Bar # Vladimir Ignatyev <ya.na.pochte@gmail.com>
def display(count, total, status=''):
    bar_len = 60;
    filled_len = int( round( bar_len * count / float( total ) ) );
    percents = round( 100.0 * count / float( total ), 1 );
    bar = '=' * filled_len + '-' * ( bar_len - filled_len );
    sys.stdout.write( '[%s] %s%s ...%s\r' % ( bar, percents, '%', status ) );
    sys.stdout.flush();
