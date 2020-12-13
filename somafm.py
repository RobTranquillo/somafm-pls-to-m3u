import requests
import os

#configuration
outputDir = "SomaFM"
source = "http://somafm.com/listen/index.html"
source = "http://somafm.com/listen/genre.html"
generateSonataConfig = False #to add in Sonata (~/.config/sonatarc)
sonataConfigIterator = 0   #number of the next station in config file (starts with zero)

#todo: die Config parameter in der Shell übergeben

#### Main
def main():
  stations = getStationsByFormat(source)
  print(str(len(stations['aac'])) + " AAC Listen eingelesen")
  print(str(len(stations['mp3'])) + " MP3 Listen eingelesen")

  toMultiFile(stations['mp3'], 'somafm-mp3.m3u')
  toMultiFile(stations['aac'], 'somafm-aac.m3u')

  try:
    os.mkdir(outputDir)
  except OSError:
    print ("Creation of the directory %s failed" % outputDir)
  else:
    print ("Successfully created the directory %s " % outputDir)
        


  for station in stations['mp3']:
    toFile(station, outputDir+'/somafm - '+station['name']+'.m3u')


  if generateSonataConfig:
    extendSonata(stations['mp3'], sonataConfigIterator)



'''
  Support for the good old Sonata player

  Insert the output to your sonata config to get the playlists to your Sonata
'''
def extendSonata(stations, sonataConfigIterator):
  configString = ''
  for station in stations:
    configString = configString + "names["+str(sonataConfigIterator)+"] = soma fm "+station['name']+"\nuris["+str(sonataConfigIterator)+"] = "+station['url']+"\n"
    sonataConfigIterator += 1
  print('\n\n' + 'Put the following lines to ~/.config/sonatarc for Sonata Playlist Support. (To append Sonata List edit the interator in somafm.py):\n'+configString);


'''
  getURLsByFormat

  @param: a url path of a page with links
  @return: a dict with name and url of a station
'''
def getStationsByFormat(source):
  r = requests.get(source)
  AACLinks = []
  MP3Links = []
  for line in r.text.split('\n'):
    if '<h3>' in line:
      headline = line[4:line.find('</h3>')]
    if '<a href' in line and '.pls' in line:
      if 'AAC:' in line:
        AACLinks.append({'name':headline, 'url':scrapeUrl(line)})
      if 'MP3:' in line:
        MP3Links.append({'name':headline, 'url':scrapeUrl(line)})
  return { 'aac' : AACLinks, 'mp3' : MP3Links }

def scrapeUrl(line):
  start = line.find('<a href') +9
  end = line.find('"',start)
  return 'https://somafm.com'+line[start:end]

def toFile(station, filename):
  all = open(filename, 'w')
  all.write("#EXTM3U\n\n")
  all.write("#EXTINF:1,"+station['name']+"\n")
  all.write(station['url']+ "\n\n")
  all.close()
  print('write '+filename)

def toMultiFile(stations, filename):
  success = 0
  all = open(filename, 'w')
  all.write("#EXTM3U\n\n")
  for station in stations:
    all.write("#EXTINF:"+str(success)+","+station['name']+"\n")
    all.write(station['url']+ "\n\n")
    success += 1
  all.close()
  print('write '+str(success)+' stations to '+filename)

#start main function
main()
