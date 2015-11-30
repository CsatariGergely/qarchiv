import sys
import argparse
import re
import codecs
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
    if None == id:
        continue
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
        statuses[filename] = " #_noleades"
        leadesText = ""
    else:
        statuses[filename] = " #gotleades"
        leadesText = leades.getText()
        print(leadesText)
    print("-  .  -  .  -  .  -")
    author = soup.find("a", {"class": "cikk-szerzo"})
    if None == author:
        print "No author found"
        statuses[filename] += " #_noauthor"
        authorText = ""
    else:
        authorText = author.getText()
        statuses[filename] += " #gotauthor"
        print(authorText)
    print("-  .  -  .  -  .  -")
    title = soup.find("h1", {"class": "cikk-cim"})
    if None == title:
        print "No author found"
        statuses[filename] += " #_notitle"
        titleText = ""
    else:
        titleText = title.getText()
        statuses[filename] += " #gottitle"
        print(titleText)
    print("-  .  -  .  -  .  -")
    content = soup.find("div", {"id": "kenyer-szov"})
    if None == content:
        print "No content found"
        statuses[filename] += " #_nocontent"
        contentText = ""
    else:
        [x.extract() for x in content.findAll('script')]
        contentText = content.getText()
        statuses[filename] += " #gotcontent"
        try:
            print(contentText)
        except UnicodeEncodeError:
            print "Exceptioning"
            print(contentText.encode('UTF-8', 'ignore'))
    outfile = codecs.open(id.group(1) + '.json', 'w', 'utf-8')
    outfile.write('{\n "author": "' + authorText + '",\n')
    outfile.write(' "title": "' + titleText.replace("\"", "\'") + '",\n')
    outfile.write(' "original": "' + originalUrl + '",\n')
    outfile.write(' "lead": "' + leadesText.replace("\"", "\'") + '",\n')
    outfile.write(' "content": "' + contentText.replace("\"", "\'") + '"\n')
    outfile.write('}\n')
    outfile.close()
    
    
print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
for keys,values in statuses.items():
    print("  {} - {}".format(keys,values))

    
