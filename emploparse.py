#!/usr/bin/python
# -*- coding: utf-8 -*-

# pip install urllib
import urllib
# pip install html.py
import HTML
import datetime
# pip install BeautifulSoup4
from bs4 import BeautifulSoup
from collections import OrderedDict

# GET the link page from the server and create a bs4 object of it
listpage = urllib.urlopen('http://www.iff.tu-bs.de/index.php?id=878')
listsoup = BeautifulSoup(listpage.read())
linklist = []
employeelist =[]

# This class represents a single emplyee with all relevant attributes
class Employee(object):
  def __init__(self):
    self.picture = ''
    self.items = OrderedDict([('name', ['', '<b>Name:</b> ']), ('room', ['', '<b>Raum:</b> ']), ('telephone', ['', '<b>Tel.:</b> ']), ('email', ['', '<b>Email:</b> ']), ('occupation', ['', '<b>Arbeitsgebiet:</b> ']), ('addoccupation', ['', '<b>Weitere Aufgaben:</b> ']), ('fax', ['', '<b>Fax:</b> ']), ('lectures', ['', '<b>Vorlesungsbetreuung:</b> ']), ('picture', ['', ''])]) 

  def __repr__(self):
    stringb = ''
    for singleitem in self.items:
      if self.items[singleitem][0] != '':
	stringb += self.items[singleitem][1] + self.items[singleitem][0] + ' <br>'
    stringb = stringb.encode('utf8')
    return (stringb)
  def addvalue(self, value, hint, relpos):
    try:
      self.items[value][0] = currentset[currentset.index(hint)+relpos]
      if value is 'email':
	self.items[value][0] += '@tu-braunschweig.de'
    except:
      pass

# this function removed duplicate entries from a list without changing its order
def removedupes(x):
  result = []
  seen = set()
  for i in x:
    if i not in seen:
      result.append(i)
      seen.add(i)
  return result

# find all links in the linkpage and add them to our linklist, 
# then remove duplicates and false entries
for listlink in listsoup.find_all('a'):
  linklist.append(listlink.get('href'))
linklist.remove('index.php?id=867')
linklist.remove('index.php?id=925')
linklist = removedupes(linklist)

# get and parse all remaining links
for currentlink in linklist:
  currentpage = urllib.urlopen('http://www.iff.tu-bs.de/'+currentlink)
  currentsoup = BeautifulSoup(currentpage.read())
  currentset = []

# if they are real emplyee subpages, create an employee object
# and add the attributes
  if currentsoup.find(id='mitarbeiter'):
    employeelist.append(Employee())
    employeelist[-1].items['name'][0] = currentsoup.find('div', attrs={ 'id': 'name'}).get_text()
    for stringset in currentsoup.stripped_strings:
      currentset.append(stringset)
    employeelist[-1].addvalue('occupation', 'Arbeitsgebiet:', +1)
    employeelist[-1].addvalue('addoccupation', 'Weitere Aufgaben:', +1)
    employeelist[-1].addvalue('telephone', 'Tel.:', +1)
    employeelist[-1].addvalue('fax', 'Fax:', +1)
    employeelist[-1].addvalue('email', 'Email:', +1)
    employeelist[-1].addvalue('lectures', 'Vorlesungsbetreuung:', +1)
    employeelist[-1].addvalue('room', 'Raum:', +1)
    employeelist[-1].picture = 'http://www.iff.tu-bs.de/' + str([image["src"] for image in currentsoup.find('div', attrs={ 'id': 'fotoMitarbeiter'})][0])

# create and print a simple HTML-table from the extracted data
for currentemp in employeelist:
  image = '<IMG SRC="' + currentemp.picture + '">'
  try:
    table.rows.append([image, str(currentemp)])
  except:
    firstrow = [[image, str(currentemp)]]
    table = HTML.Table(firstrow)
    pass
htmlcode = '<!DOCTYPE HTML>\n<html>\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n<title>Test</title>\n<style type="text/css"> \n\ttable { page-break-inside:auto }\n\ttr    { page-break-inside:avoid; page-break-after:auto }\n</style>\n</head>\n<body>\n'
htmlcode += str(table)
htmlcode += '\n</body>\n</html>'
date = datetime.datetime.now().strftime('%Y-%m-%d')
f = open('mitarbeiter-' + date + '.html', 'w')
print 'Writing current HTML file. \n'
f.write(htmlcode)
f.close()
