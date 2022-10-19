
# from http.client import HTTPSConnection
# from base64 import b64encode
# import requests
# #This sets up the https connection
# c = HTTPSConnection("100.26.110.188:9200")
# #we need to base 64 encode it
# #and then decode it to acsii as python 3 stores it as a byte string
# userAndPass = b64encode(b"elastic:_VVwXtRyQtvvZ9Hz7h89").decode("ascii")
# headers = { 'Authorization' : 'Basic %s' %  userAndPass }
# #then connect
# # c.request('GET', '/', headers=headers,verify=False)
#
#
# #get the response back
# res = c.getresponse()
# # at this point you could check the status etc
# # this gets the page text
# data = res.read()

import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# userAndPass = b64encode(b"elastic:_VVwXtRyQtvvZ9Hz7h89").decode("ascii")
# headers = { 'Authorization' : 'Basic %s' %  userAndPass }
# r = requests.get('https://100.26.110.188:9200', auth=('elastic', '_VVwXtRyQtvvZ9Hz7h89'),verify=False)
# r = requests.put('https://100.26.110.188:9200/my_test_index', auth=('elastic', '_VVwXtRyQtvvZ9Hz7h89'),verify=False)
r = requests.get('https://100.26.110.188:9200/content', auth=('elastic', '_VVwXtRyQtvvZ9Hz7h89'),verify=False)
# r = requests.delete('https://100.26.110.188:9200/my_test_index', auth=('elastic', '_VVwXtRyQtvvZ9Hz7h89'),verify=False)
data=r.json()
print(type(data))
print(data)

