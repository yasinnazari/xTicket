import threading
import requests
import time

def fetch_url(url):
   resp = requests.get(url)
   print(f'URL: {url} Length -> {len(resp.text)}')

start = time.time()

urls = [
   'https://arzypto.com',
   'https://varzesh3.com'
]

threads = []

for url in urls:
   thread = threading.Thread(target=fetch_url, args=(url,))
   threads.append(thread)
   thread.start()

for thread in threads:
   thread.join()

end = time.time()
execution_time = end - start

print('--------------------------------------')
print(execution_time, "| With Threading |")
print('--------------------------------------')
