# somafm-pls-to-m3u
gets all somaFM channels and creates m3u playlists for each with both station sources

# now with Sonata support
you can generate entrys for your Sonata config file (commonly: ~/.config/sonata/sonatarc)

feature activation:
- generateSonataConfig = True

extend your existing streams list
- sonataConfigIterator = 13   #number of the next station in your config file (starts with zero)

# requirements
- python3
- python3 -> requests
- python3 -> os

# how to run
```
 First git clone this repository and  step into it..
 
 $ pip install -r requirements.txt
 $ python3 somafm.py
```
