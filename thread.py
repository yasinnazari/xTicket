import requests
import time

def fetch_url(url):
   resp = requests.get(url)
   print(f'URL: [{url}] *** Length -> {len(resp.text)}')

start = time.time()

urls = [
   'https://www.arzypto.com/',
   'https://www.varzesh3.com/'
]

for url in urls:
   result = fetch_url(url)

end = time.time()
execution_time = end - start

print('--------------------------------------')
print(execution_time, "[X] Without Threading [X]")
print('--------------------------------------')
