This decoder works with btshowmetainfo.py
The rest dunno if is necessary

Also:mybencoder.py give info about the variables


Example:

jaume@fcb:~/Dropbox/docs/TPB-Visualizar09/thepiratepieGoogleCode/thepiratepie/code/util/TORRENTdecoder/python$ python mybencoder.py 
<type 'str'> comment
<type 'dict'> info
<type 'str'> encoding
<type 'int'> creation date
<type 'list'> announce-list
<type 'str'> created by
<type 'str'> announce


jaume@fcb:~/Dropbox/docs/TPB-Visualizar09/thepiratepieGoogleCode/thepiratepie/code/util/TORRENTdecoder/python$ python btshowmetainfo.py  example.torrent 
btshowmetainfo.py:12: DeprecationWarning: the sha module is deprecated; use the hashlib module instead
  from sha import *
btshowmetainfo 20030621 - decode BitTorrent metainfo files
###
###
metainfo file.: example.torrent
info hash.....: e238281a8b7614e9337402d44e3544e922159024
###
directory name: G.I. Joe - The Rise of Cobra 2009 ENG DIVX-ELiTE
files.........: 
###
   G.I. Joe - The Rise of Cobra 2009 ENG DIVX-ELiTE.avi (1489288244)
###
archive size..: 1489288244 (5681 * 262144 + 48180)
###
announce url..: http://tracker.thepiratebay.org/announce
###
announce-list.: http://tracker.thepiratebay.org/announce|udp://tracker.thepiratebay.org:80/announce|http://tracker.publicbt.com/announce|udp://tracker.publicbt.com:80/announce|udp://tracker.openbittorrent.com:80/announce|http://tracker.openbittorrent.com/announce
###
comment.......: Torrent downloaded from http://thepiratebay.org
#########################



