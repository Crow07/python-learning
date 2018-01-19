import requests
r = requests.get('https://www.github.com')
print r.status_code
print r.headers

r_para = requests.get('http://www.tap4fun.com')
print r_para.content