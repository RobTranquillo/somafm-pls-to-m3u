import requests
from bs4 import BeautifulSoup
with open("index.html") as fp:
    soup = BeautifulSoup(fp, 'lxml')

stations = []
m3uContent = ''
i=4

stations = soup.find_all('ul')

cats = soup.find_all(name='dl')
for cat in cats:
    station = cat.dd.a.get('href')
    stations.append(station)
    link = "https://somafm.com" + station + "\r\n"

    r = requests.get(link)
    link1Start = r.text.find('File1=')+6
    link1End = r.text.find('\n', link1Start)
    link2Start = r.text.find('File2=')+6
    link2End = r.text.find('\n', link2Start)
    m3uContent = r.text[ link1Start : link1End ] +'\n'+ r.text[ link2Start : link2End ]

    pl = open('somafm-'+station[1:-4]+'.m3u', 'w')
    pl.write(m3uContent)
    pl.close()

    print('wrote '+station);
