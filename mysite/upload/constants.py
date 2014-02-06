
# By default the file name will be " 'File-' + today's_date + current_time "
import datetime

FILENAME = "File-" + datetime.datetime.now().strftime('%d_%b_%Y-%H_%M_%S_%f')
