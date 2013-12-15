#!/bin/bash
pylupdate4 ../i18n/geopunt4qgis_ts.pro
lrelease ../i18n/*.ts

OLD='images\/logogeopunt4Q.png'
NEW='..\/images\/logogeopunt4Q.png'

TEMPNL=$RANDOM
TEMPEN=$RANDOM

markdown ../README.md > ../i18n/$TEMPEN
markdown ../README_NL.md > ../i18n/$TEMPNL

rm ../i18n/about-en.html 
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; } </style></head> <body style=" font-size:9pt; font-weight:400; font-style:normal;">' > ../i18n/about-en.html 
sed "s/$OLD/$NEW/g" ../i18n/$TEMPEN >> ../i18n/about-en.html
echo '</body></html>' >> ../i18n/about-en.html
rm ../i18n/$TEMPEN

rm ../i18n/about-nl.html
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; } </style></head> <body style=" font-size:9pt; font-weight:400; font-style:normal;">' > ../i18n/about-nl.html 
sed "s/$OLD/$NEW/g" ../i18n/$TEMPNL >> ../i18n/about-nl.html
echo '</body></html>' >> ../i18n/about-nl.html
rm ../i18n/$TEMPNL