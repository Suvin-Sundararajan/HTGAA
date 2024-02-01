from opentrons import protocol_api
import opentrons.execute
from enum import Enum
from opentrons.types import Location, Point, LocationLabware
import turtle
import math

# Draw ribose molecule atom positions using colored Fluorescent proteins expressing colonies
# the size of the colonies depict realistic sizes of the actual atoms
# the colors of the atoms matches the usual color scheme used in publications

metadata = {
    'apiLevel': '2.13',
    'protocolName': ' Petri Ribose',
    'description': ''' Petri Ribose''',
    'author': 'Adrian'
    }

draw=False
drawCellSize=30 # !!! it will be overwritten later
#standard colors except for base where we arbitrarily choose green

#BASE=GREEN=,OXYGEN=RED=, HYDROGEN=WHITE, CARBON Black, PHOSPHOROUS_PURPLE, CARBON_BLACK_COLOR="A6"#BLUE_COLOR*100+OXYGEN_RED_COLOR*10+BASE_GREEN_COLOR
class MoleculeColors(Enum):
    green= "A1"
    blue = "A2"
    red = "A3"
    white ="A4" 
    yellow="A5"
    black="A6"

#picometer radius
class MoleculeSizes(Enum):
    OXYGEN_SIZE = 60
    HYDROGEN_SIZE = 53
    CARBON_SIZE = 70
    PHOSPHOROUS_SIZE=100 #real value is 195 but we cheat so it's not enourmous
    BASE_SIZE = 100

#Here we add our own design
phosphorous = {
  "name":"p",
  "wells": [(-5,5)],
  "color": [MoleculeColors.red, MoleculeColors.blue],
  "size": MoleculeSizes.PHOSPHOROUS_SIZE
}

base = {
  "name":"base",    
  "wells": [(6,3)],
  "color": [MoleculeColors.green],
  "size": MoleculeSizes.BASE_SIZE
}
# Rows are letters, columns are numbers like G1
oxygen = {
  "name":"o",
  "wells": [
    (-6,6),(-6,4),(-4,6),(-4,4),(-2,-5),(2,4)],
  "color": [MoleculeColors.red],
  "size": MoleculeSizes.OXYGEN_SIZE
}
# Rows are letters, columns are numbers like G1
carbon = {
  "name":"c",
  "wells": [(-3,3),(-1,2),(-1,-4),(5,2),(5,-4)],
  "color":[MoleculeColors.black],
  "size": MoleculeSizes.CARBON_SIZE
}
hydrogen = {
  "name":"h",
  "wells": [(-4,2),(-3,-6),(-2,4),(-2,1),(0,-3),(4,1),(4,-3),(6,-5)],
  "color": [MoleculeColors.white],
  "size": MoleculeSizes.HYDROGEN_SIZE
}
#End Here we add our own design

def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware('opentrons_96_filtertiprack_20ul', 1) 
    reservoir = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 2, label='Falcon Tube Rack')
    plate = protocol.load_labware('sally_htgaa_agar', 3, 'Adrian Agar Plate')  
    p20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[tips])
    p20.starting_tip = tips.well('A1')  
    rows=18 
    drawPlateOrigin=(0,0) # that's CENTER
    realCenterLocation = plate['A1'].top()
    drawSetup(drawPlateOrigin,rows)
    print("realCenterLocation",realCenterLocation)
    mmPerRow=int(80/rows) # here is where we set the diameter of the Petri in mm
    print("mmPerRow",mmPerRow)
    tran(phosphorous, p20, reservoir, plate, realCenterLocation,drawPlateOrigin,rows,mmPerRow) 
    tran(carbon, p20, reservoir, plate, realCenterLocation,drawPlateOrigin,rows,mmPerRow)          
    tran(oxygen, p20, reservoir, plate, realCenterLocation,drawPlateOrigin, rows,mmPerRow)
    tran(hydrogen, p20, reservoir, plate, realCenterLocation, drawPlateOrigin, rows,mmPerRow)  
    tran(base, p20, reservoir, plate, realCenterLocation,drawPlateOrigin, rows,mmPerRow)  
    if draw:
        turtle.exitonclick()

def tran(molecule: dict[list[str], Enum, Enum], p20:protocol_api.InstrumentContext, reservoir,plate:protocol_api.Labware,  realCenterLocation:Location, drawPlateOrigin, rows, mmPerRow):
    for well in molecule["wells"]:    
        for c in range(0,len(molecule["color"])):
            p20.pick_up_tip()
            #command to pick up the liquid. You can choose to pick up less than 18ul but not more.
            #p20.aspirate(molecule["size"].value,  reservoir[molecule["color"][c].value])
            p20.aspirate(molecule["size"].value/50,  reservoir["A1"])
            #p20.dispense(molecule["size"].value, realCenterLocation)  dispense a microLiter in the middle
            #center_location.move(types.Point(x=5, y=3))
            newLocation=realCenterLocation.move(opentrons.types.Point(mmPerRow*well[0], y=mmPerRow*well[1]))
            print("new molecule at:",well[0],",",well[1])
            printLocation("newLocation",newLocation, " deltaXmm:", mmPerRow*well[0]," deltaYmm:", well[1]," distance from center:",math.sqrt(mmPerRow*well[0]*mmPerRow*well[0]+mmPerRow*well[1]*mmPerRow*well[1]))        
            p20.dispense(molecule["size"].value/5, newLocation )
            p20.drop_tip() 
            drawWellContent(molecule['name'], well, molecule["size"].value, drawPlateOrigin,molecule["color"][c].name, c)

def drawWellContent(moleculeName:str, well, size:int, drawPlateOrigin, color, colorNumber):
    if draw==True:
        to=well
        deltaX=drawCellSize*to[0]-drawCellSize/2
        deltaY=drawCellSize*to[1]-drawCellSize/2
        radius=int(drawCellSize/2-1)*(size/MoleculeSizes.PHOSPHOROUS_SIZE.value)
        turtle.penup()
        wellCenter=(drawPlateOrigin[0]+drawCellSize/2+deltaX,drawPlateOrigin[1]+drawCellSize/2+deltaY)
        turtle.color(color)
        turtle.goto(wellCenter[0],wellCenter[1]-radius)
        turtle.pendown()
        turtle.fillcolor(color)
        turtle.begin_fill()
        if colorNumber==0:
            turtle.circle(radius)
        else:
            turtle.circle(radius*.45*(3-colorNumber))
        turtle.end_fill()
        turtle.penup()
        if color!="black":
            turtle.color("black")
        else:
            turtle.color("white")
        turtle.goto(wellCenter[0]-radius/2,wellCenter[1]-radius/2)    
        turtle.pendown()
        turtle.write(str(well[0])+","+str(well[1])) #+" "+moleculeName.capitalize())
        turtle.penup()

def setGrid(drawPlateOrigin, rows):
    halfCell=drawCellSize/2
    writingOffset=8
    drawCircleDiam=rows*drawCellSize
    turtle.penup()
    turtle.goto(drawPlateOrigin[0],drawPlateOrigin[1]-drawCircleDiam/2)
    turtle.pendown()
    turtle.circle(drawCircleDiam/2)
    line(drawPlateOrigin[0],drawPlateOrigin[1],drawPlateOrigin[0]+10,drawPlateOrigin[1],"red")   
    line(drawPlateOrigin[0],drawPlateOrigin[1],drawPlateOrigin[0],drawPlateOrigin[1]+10,"red")   
    turtle.penup()
    startX=drawPlateOrigin[0]-(rows/2)*drawCellSize+halfCell
    startY=drawPlateOrigin[1]-(rows/2)*drawCellSize+halfCell
    #Horiz
    for i in range(0,rows):
        line(startX,startY+i*drawCellSize, startX+(rows-1)*drawCellSize,startY+i*drawCellSize)
        turtle.penup()
        turtle.goto(startX-drawCellSize,startY+i*drawCellSize+writingOffset)
        if i!=rows-1:
            turtle.write(i+1-int(rows/2))

    for i in range(0,rows):
        line(startX+i*drawCellSize,startY, startX+i*drawCellSize,startY+(rows-1)*drawCellSize)
        turtle.penup()
        turtle.goto(startX+i*drawCellSize+writingOffset,startY-drawCellSize/2)
        if i!=rows-1:
            turtle.write(i+1-int(rows/2)) 

def setCoordinates(drawPlateOrigin, rows:int):
    turtle.hideturtle()
    screenSize = turtle.screensize()
    drawCellSize=int(screenSize[1]/rows) 
    turtle.setup(width = 1.0, height = 1.0)
    print("drawCellSize:", drawCellSize)
    #turtle.setworldcoordinates(drawPlateOrigin[0]-screenSize[0]/2, drawPlateOrigin[1]-screenSize[1]/2, screenSize[0], screenSize[1])  
    turtle.Screen().bgcolor("grey") 

def line(x1, y1, x2, y2, line_color="black"):
    turtle.pencolor(line_color)
    turtle.up()
    turtle.goto(x1, y1)
    turtle.down()
    turtle.goto(x2, y2,)

def drawSetup(drawPlateOrigin, rows):
    if (draw):
        setCoordinates(drawPlateOrigin,rows)
        setGrid(drawPlateOrigin, rows)

def  printLocation(name: str,  location, s1, delX, s2, delY,mess2, distToCenter):
    print(name,":",location.point.x, location.point.y, s1, delX, s2, delY,mess2, distToCenter)

# center x 328 so min is 288 and max= 368
# center y=43 so min is 3 max =83
# and a realPlateCell is 4 mm wide