#!/bin/bash

# $1 Emse
# $2 2010
# $3 2020

# Publish or perish QUERY
# journal, keywords and years to be tailored `$1$2-$3.csv`
/pop7query --journal "Empirical+Software+Engineering" --keywords "replication+package" --gscholar --years 2010-2020 Emse2010-2020.csv

# link to the PDF on Springer
# `$1$2-$3-PDFlinks.txt`
awk -F"," '{for(i=1; i<=NF; i++) {if($i~/springer/) print $i".pdf"}}' Emse2010-2020.csv | sed 's/\.com\/article\//\.com\/content\/pdf\//g' | sed 's/pdf\".pdf/pdf/' | sed 's/\"//g' > Emse2010-2020-PDFlinks.txt

# Download the PDFs 
# mkdir $1$2-$3-PDF
mkdir -p Emse2010-2020-PDF
for i in `cat Emse2010-2020-PDFlinks.txt`; do FN=`basename $i` && wget -q -O Emse2010-2020-PDF/$FN $i && sleep 5; done

# remove false positives: no mention of "replication package"
# other papers seem eligible, put them in array
LIST_OF_PAPERS=()
for i in Emse2010-2020-PDF/*pdf; do if [ $(pdfgrep -c "replication package" $i| tr -d '\n') = 0 ]; then echo "$i" ; else LIST_OF_PAPERS+=( "$i" ); fi; done > Emse2010-2020-PDF/fp.txt

# proximity check: if link and "replication package" are on the same page
# 75% hit ratio
for i in "${LIST_OF_PAPERS[@]}"; do printf "$i: URL for Rep Pack -> " && comm -12 <(pdfgrep -n  "replication package" $i | awk -F":"  '{print $1}'|sort|uniq) <(pdfgrep -n "http" $i | awk -F":" '{print $1}'|sort|uniq) | paste -s -d, ; done > Emse2010-2020-PDF/locations_URLs.txt

for i in `grep "\s$" ../locations_URLs.txt`; do pdfgrep -C3 "replication package" < awk -F":" '{print $1}' $i; done

# proxies:
## "available at [ref]"
