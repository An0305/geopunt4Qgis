#!/usr/bin/env python
import os, glob
import zipfile

prjname = "geopunt4Qgis"
source = os.path.abspath( os.path.dirname( __file__ ) + "/.." )
print source
target = os.path.join( source , "build/geopunt4Qgis.zip" )
includeFile = ["*.py", "*.txt", "*.qrc", "*.ui", "*.md","*.gif", "*.jpg", "*.png","*.html", "*.qm", "*.ts","*.json","*.xml" ] 
includeDir = ["images","i18n","data"]

def makeList( src ):
  fileList = []
  for incl in includeFile: 
    for idir in includeDir:
      fileList = fileList + glob.glob( os.path.join(  src , idir , incl ))
    fileList = fileList + glob.glob(os.path.join( src , incl )) 
  return fileList

def zipdir(path, zip):
  files = makeList(path)
  for zfile in files: 
    sbase = os.path.dirname(source)
    arcName = zfile.replace( sbase ,prjname)
    zip.write( zfile , arcName)

if __name__ == '__main__':
    if os.path.exists( target ):
      os.remove(target)
    zipf = zipfile.ZipFile( target , 'w')
    zipdir( source , zipf)
    zipf.close()