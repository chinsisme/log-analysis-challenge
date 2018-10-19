import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
from shutil import copy
from pygtail import Pygtail

file_source = '/tmp/me/out.log'
file_destination = os.getcwd()

# Function generate new column


def datetime(row):
    return row.Date + ' ' + row.Time


# Copy file to current folder
copy(file_source, file_destination)

# Set columns for the dataframe
columns_log = ['LogType', 'Date', 'Time', 'PID', 'ResponseTime', 'UID', 'URL']

# Create dataframe
df_logs = pd.DataFrame(columns=columns_log)

# Load and transform log data into dataframe
for line in Pygtail(file_destination + 'out.log'):
    sys.stdout.write(line)
# Remove file from current folder
os.remove('out.log')


# """
# Generating visualization for number of errors per hour
# """
# # Create dataframe containing only errors
# df_only_error = df_logs[df_logs.LogType == 'ERROR']

# df_error_group_by_date_time = df_only_error['ResponseTime'].groupby(
#     [df_only_error['Date'], df_only_error['Time'].str.slice(start=0, stop=2)])
# series_error_count = df_error_group_by_date_time.count()
# series_error_count = series_error_count.reset_index(name='ErrorCount')
# df_error_count = pd.DataFrame(series_error_count)

# df_error_count['Datetime'] = df_error_count.apply(
#     lambda row: datetime(row), axis=1)

# # Plot graph for error count per hour
# plt.plot(df_error_count['Datetime'], df_error_count['ErrorCount'])
# plt.show()


# """
# Generating percentile stats for response times of successful responses
# """
# # Create dataframe containing only successful responses
# df_non_error = df_logs[df_logs.LogType != 'ERROR']

# df_non_error_average_response = pd.to_numeric(df_non_error['ResponseTime']).groupby(
#     [df_non_error['Date'], df_non_error['Time'].str.slice(start=0, stop=2)]).mean().reset_index()

# df_non_error_average_response['Datetime'] = df_non_error_average_response.apply(
#     lambda row: datetime(row), axis=1)

# # Plot graph for response time for successful requests
# plt.plot(df_non_error_average_response['Datetime'],
#          df_non_error_average_response['ResponseTime'])
# plt.show()
