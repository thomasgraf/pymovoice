import requests
import sys

###
#
# http://opengtindb.org/?ean=4002468182799&cmd=query&queryid=492934365
#
###

def get_ean(eancode):
    #r = requests.get('http://opengtindb.org/?ean='+eancode+'&cmd=query&queryid=492934365')
    r = requests.get('http://opengtindb.org/?ean='+eancode+'&cmd=query&queryid=400000000')
    data = r.text
    data_dict = {}
    for line in data.split('\n'):
        line = line.strip()
        if not len(line.split('='))==2:
            continue
        data_dict[line.split('=')[0].strip()]=line.split('=')[1].strip()
    return data_dict


if __name__=='__main__':
    print get_ean(sys.argv[1])
