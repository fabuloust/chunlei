import hashlib
import time


def get_basic_data():
    atime = int(time.time())
    username = 'test'
    partner_key = 'ABjs4yGIdEmN7HZi'
    partner_name = 'chunleiyiwentong'
    total = partner_key + str(atime) + username
    sign = hashlib.md5(total.encode('utf-8')).hexdigest()[8:-8]
    return {'partner': partner_name, 'sign': sign, 'atime': atime, 'user_id': username}

