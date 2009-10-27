##from Bittorrent.bencode import *
from bencode import *
metainfo_file = open("example.torrent", 'rb')
metainfo = bdecode(metainfo_file.read())
metainfo_file.close()
for key in metainfo :
   val = metainfo[key]
   print type(val),key

