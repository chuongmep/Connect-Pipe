import clr
import math

import sys
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)
import System

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
doc = DocumentManager.Instance.CurrentDBDocument

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

import collections
#The inputs to this node will be stored as a list in the IN variables.
if isinstance(IN[0],list):
	element = UnwrapElement(IN[0])
	toggle = 0
else:
	element = [UnwrapElement(IN[0])]
	toggle = 1
		
def nextElements(elem):
	listout = []
	try:
		connectors = elem.ConnectorManager.Connectors
	except:
		connectors = elem.MEPModel.ConnectorManager.Connectors
	for conn in connectors:
		for c in conn.AllRefs:
			if c.Owner.Id.Equals(elem.Id):
				continue
			elif c.Owner.GetType() == Mechanical.MechanicalSystem:
				continue
			else:
				newelem = c.Owner
			listout.append(newelem)
	return listout

def systemcheck(elem):
	if elem.GetType() == Mechanical.MechanicalSystem or elem.GetType() == Plumbing.PipingSystem:
		return True
	else:
		return False
	
def collector(elem):
	cont = 0
	elements = nextElements(elem)
	for x in elements:
		if x.Id in lookup:
			cont += 1
		else:
			item = doc.GetElement(x.Id)
			if systemcheck(item):
				return elem
			else:
				lookup[x.Id] = item
				collector(x)
	if cont == len(elements):
		return elem
		

listout = []
for x in element:
	lookup = collections.OrderedDict()
	collector(x)
	listout.append(lookup.Values)

#Assign your output to the OUT variable.
if toggle:
	OUT = lookup.Values
else:
	OUT = listout