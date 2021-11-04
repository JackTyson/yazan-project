###########################
# IMPORT GLOBAL LIBRARIES #
###########################

import datetime
from influxdb import InfluxDBClient
import json
from pycampbellcr1000 import CR1000

##########################
# IMPORT LOCAL LIBRARIES #
##########################

import database
import datalogger

###################################
# INITIALISE DATALOGGER INTERFACE #
###################################

serial_id = 'serial:/dev/serial/by-id/usb-Campbell_Scientific_Inc._CR1000X_1.0-if02' # Set serial address
print('Initialising CR1000X...')
device = datalogger.init(CR1000,serial_id) # Initialise the datalogger connection

#################################
# INITIALISE DATABASE INTERFACE #
#################################

db_name = 'PVTA_master'
db_host = 'localhost'
db_port = 8086
print('Initialising InfluxDB...')
db_client = database.init(InfluxDBClient,db_host,db_port,db_name) # Initialise the database client

##########################################
# POLL THE DATALOGGER FOR TRANSIENT DATA #
##########################################

print('Setting data sample time period...')
sample_end = datetime.datetime.now().replace(microseconds=0) # The start of the sample period is now
time_period = 15 # The sample period in minutes (backwards in time from now)
sample_start = sample_end - datetime.timedelta(minutes=time_period) # Start point is time_period minutes prior to end point
sample = [sample_start, sample_end] # Concatenate time points
table_idx = 'every_30_sec' # Set datalogger table name
print('Will poll', table_idx, 'for data taken between', sample_start, 'and', sample_end,'...')
sample_data = datalogger.get_data(device,sample,table_idx)

#######################################
# SAVE POLLED DATA TO ACTIVE DATABASE #
#######################################

print('Saving data to InfluxDB...')
db_client.insert(sample_data)

############
# SHUTDOWN #
############

print('Closing datalogger connection...')
datalogger.close(device)
