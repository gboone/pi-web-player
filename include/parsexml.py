import os
from defusedxml.ElementTree import parse

def returnTrackArtist(file):
  xmlfile = os.open('file', os.O_RDONLY)
  parsedXML = parse(xmlfile)
  rootXML = parsedXML.getroot()
  return rootXML[2][0][1].text

print(returnTrackArtist())
