###########################
# IMPORT GLOBAL LIBRARIES #
###########################

import json

########################
# FUNCTION DEFINITIONS #
########################

def init(InfluxDBClient,db_host,db_port,db_name):
    print('-> Connecting to database server...')
    try:
        db_client = InfluxDBClient(host=db_host,port=db_port) # Initialise the connection to the database server
    except:
        db_client = None
    finally:
        if(db_client == None):
            print('-> [!] Connection failure. Is InfluxDB running and configured correctly?')
        else:
            print('-> Connection successful.')
            print('--> Switching to database:', db_name)
            db_client.switch_database('PVTA_master')
            print('--> Done.')
    return db_client

def intercept_feed(device,sample,table_idx):
    print('--> Intercepting feed from datalogger...')
    try:
        data = json.loads(device.get_data(table_idx,sample[0],sample[1]))
    except:
        data = None
    finally:
        if(data == None):
            print('--> [!] An error occurred.')
        else:
            print('--> Data has been intercepted and converted.')
    return data

def insert(db_client,data):
    if(db_client.write_points(data)):
        print('-> Data written to database successfully.')
    else:
        print('-> [!] Error writing data to database. Check user permissions and access control lists.')
    return
