# ThePiratePie.org metadata scraper
# Records metadata of torrents on ThePirateBay.org
# By david.stolarsky@gmail.com

import webcrawlerPiratebayLS
import time


tpb = webcrawlerPiratebayLS.webcrawlerTorrent()


tpb.debug("Started metadata filler")
tpb.fillMissingMetadata()
tpb.debug("Finished metadata filler")
