import requests
from bs4 import BeautifulSoup


#configuration
source = "http://somafm.com/listen/index.html"
generateSonataConfig = True #to add in Sonata (~/.config/sonatarc)
sonataConfigIterator = 13   #number of the next station in config file (starts with zero)


# main func
configString = ''
r = requests.get(source)
soup = BeautifulSoup(r.text, 'lxml')

cats = soup.find_all(name='dl')
for cat in cats:
    station = cat.dd.a.get('href')
    link = "https://somafm.com" + station + "\r\n"

    r = requests.get(link)
    link1Start = r.text.find('File1=')+6
    link1End = r.text.find('\n', link1Start)
    link2Start = r.text.find('File2=')+6
    link2End = r.text.find('\n', link2Start)
    m3uContent = r.text[ link1Start : link1End ] +'\n'+ r.text[ link2Start : link2End ]

    titleStart = r.text.find('Title1=SomaFM:') + 15
    titleEnd =  r.text.find('(', titleStart)
    stationTitle = r.text[titleStart : titleEnd].strip()

    if generateSonataConfig:
      configString = configString + "names["+str(sonataConfigIterator)+"] = soma fm "+stationTitle+"\nuris["+str(sonataConfigIterator)+"] = "+r.text[ link1Start : link1End ]+"\n"
      sonataConfigIterator += 1

    pl = open('soma fm - '+stationTitle+'.m3u', 'w')
    pl.write(m3uContent)
    pl.close()

    print('wrote '+stationTitle);

print('\n\n' + 'for Sonata Config (edit the interator in the brackets):\n'+configString);
