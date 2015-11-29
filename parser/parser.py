import sys
import argparse
import re
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup

if __name__ == '__main__':
    directory = ""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory')
    args = parser.parse_args()
if None == args.directory:
    print "Please provide an input directory with -d or --directory options."
    sys.exit(0)
if "irectory" == args.directory:
    print "Did you mean --directory by any chance?"
    sys.exit(0)
print "The directory is " + args.directory

files = [f for f in listdir(args.directory) if isfile(join(args.directory, f))]
statuses = {}
for filename in files:
    print "\n\n%s" % filename
    #http://aktiv.quart.hu/quart/archiv/cikk.html?id=
    #cikk-1004.html
    id = re.search('(cikk-([0-9]+))\.html', filename)
    originalUrl = 'http://aktiv.quart.hu/quart/archiv/cikk.html?id=' + id.group(2)
    print(originalUrl)
    statuses[filename] = "started"
    file = open(args.directory + "\\" + filename, 'r')
    soup = BeautifulSoup(file, 'html.parser')
    #print(soup.prettify().encode('UTF-8'))
    leades = soup.find("div", {"id": "leades"})
    if None == leades:
	    print "No leades found in here"
    if None == leades:
        statuses[filename] = " #noleades"
        leadesText = ""
    else:
        statuses[filename] = " #gotleades"
        leadesText = leades.getText()
        print(leadesText)
    print("-  .  -  .  -  .  -")
    author = soup.find("a", {"class": "cikk-szerzo"})
    if None == author:
        print "No author found"
        statuses[filename] += " #noauthor"
        authorText = ""
    else:
        authorText = author.getText()
        statuses[filename] += " #gotauthor"
        print(authorText)
    print("-  .  -  .  -  .  -")
    title = soup.find("h1", {"class": "cikk-cim"})
    if None == title:
        print "No author found"
        statuses[filename] += " #notitle"
        titleText = ""
    else:
        titleText = title.getText()
        statuses[filename] += " #gottitle"
        print(titleText)
    print("-  .  -  .  -  .  -")
    content = soup.find("div", {"id": "kenyer-szov"})
    if None == content:
        print "No content found"
        statuses[filename] += " #nocontent"
        contentText = ""
    else:
        contentText = content.getText()
        statuses[filename] += " #gotcontent"
        try:
            print(contentText)
        except UnicodeEncodeError:
            print "Exceptioning"
            print(contentText.encode('UTF-8', 'ignore'))
    outfile = open(id.group(1) + '.json', 'w')
    outfile.write('{\n"author": "' + '",\n')
    
    
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
for keys,values in statuses.items():
    print("  {} - {}".format(keys,values))

    
