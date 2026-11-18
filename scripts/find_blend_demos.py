import urllib.request
import re

url = "https://www.blender.org/download/demo-files/"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    links = re.findall(r'https?://[^\s"\'<>]+\.blend(?:\.gz|\.zip)?', html, re.I)
    print("Found blend links:")
    for l in set(links):
        print(l)
except Exception as e:
    print("Error:", e)
