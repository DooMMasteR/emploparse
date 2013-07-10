#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
from bs4 import BeautifulSoup
from collections import OrderedDict

listpage = urllib.urlopen('http://www.iff.tu-bs.de/index.php?id=878')
listsoup = BeautifulSoup(listpage.read())
linklist = []
employeelist =[]

class Employee(object):
  def __init__(self):
    self.items = OrderedDict([('name', ['', 'Name: ']), ('room', ['', 'Raum: ']), ('telephone', ['', 'Tel.: ']), ('email', ['', 'Email: ']), ('occupation', ['', 'Arbeitsgebiet: ']), ('addoccupation', ['', 'Weitere Aufgaben: ']), ('fax', ['', 'Fax: ']), ('lectures', ['', 'Vorlesungsbetreuung: ']), ('picture', ['', ''])]) 
  def __repr__(self):
    stringb = ''
    for singleitem in self.items:
      if self.items[singleitem][0] != '':
	stringb += self.items[singleitem][1] + self.items[singleitem][0] + '\n'
    stringb = stringb.encode('utf8')
    return (stringb)
  def addvalue(self, value, hint, relpos):
    try:
      self.items[value][0] = currentset[currentset.index(hint)+relpos]
      if value is 'email':
	self.items[value][0] += '@tu-braunschweig.de'
    except:
      pass

for listlink in listsoup.find_all('a'):
  linklist.append(listlink.get('href'))
linklist.remove('index.php?id=867')
linklist.remove('index.php?id=925')

for currentlink in linklist:
  currentpage = urllib.urlopen('http://www.iff.tu-bs.de/'+currentlink)
  currentsoup = BeautifulSoup(currentpage.read())
  currentset = []
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
    employeelist[-1].items['picture'][0] = 'http://www.iff.tu-bs.de/' + str([image["src"] for image in currentsoup.find('div', attrs={ 'id': 'fotoMitarbeiter'})][0])
    print employeelist[-1]
