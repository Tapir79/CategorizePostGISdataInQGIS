from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

uri = QgsDataSourceURI()
# set host name, port, database name, username and password
uri.setConnection("localhost", "5432", "testqgis", "postgres", "postgres")
uri.setDataSource("public","buildings_espoo", "the_geom", "")
#create a new layer from a datasource uri
lyr = QgsVectorLayer(uri.uri(), "buildings_espoo", "postgres")
if not lyr.isValid():
    print "Layer %s did not load" % lyr.name()
#########classify###########################
#value,symbol,legend
buildings = {
    "Apt build":("yellow","Apartment building"),
    "Fire station":("red","Fire station"),
    "greenhouse":("green","greenhouse"),
    "Industrial":("grey","Industrial"),
    "Kindergarten":("pink","Kindergarten"),
    "Office":("brown","Office"),
    "outbuilding":("yellow","outbuilding"),
    "power plant":("lightblue","power plant"),
    "Recreational":("darkgreen","Recreational"),
    "Rowhouse":("darkcyan","Rowhouse"),
    "School":("pink","School"),
    "Vehicle shelter":("darkcyan","Vehicle shelter")}
categories = []
# btype = buildingtype, buildings = list of classes
for btype, (value,legend) in buildings.items():
    sym = QgsSymbolV2.defaultSymbol(lyr.geometryType())
    sym.setColor(QColor(value))
    category = QgsRendererCategoryV2(btype, sym, legend)
    categories.append(category)
 # the field we use to classify the data
field = "usetype"
renderer = QgsCategorizedSymbolRendererV2(field, categories)
lyr.setRendererV2(renderer)
########Add layer###################
reg = QgsMapLayerRegistry.instance()
reg.addMapLayer(lyr)
