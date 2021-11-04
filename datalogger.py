###########################
# IMPORT LOCAL LIBRARIES #
###########################

from database import intercept_feed

#######################
# FUNCTION DEFINTIONS #
#######################

def init(CR1000,serial_id):
    print('-> Attempting connection on:', serial_id)
    try:
        device = CR1000.from_url(serial_id)
    except:
        device = None
    finally:
        if(device == None):
            print('-> [!] Connection failure. Is the serial address correct?')
        else:
            print('-> Connection successful.')
    return device

def poll_tables(device):
    return device.list_tables()

def get_data(device,sample,table_idx):
    print('-> Downloading data...')
    sample_data = intercept_feed(device,sample,table_idx)
    print('-> Checking data integrity...')
    if(sample_data == None):
        print('-> [!] A null response has been received.')
    else:
        print('-> Data is integral.')
    return sample_data

def close(device):
    device.bye()
    print('-> Done.')
    return
