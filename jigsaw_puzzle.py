#!/usr/bin/env python 

import inkex
import simplestyle
import random

from simpletransform import computePointInNode

def randomBool():
    return random.random() > .5

def addPath(parent, style, name, data):
    line_attribs = {'style':simplestyle.formatStyle(style),
            inkex.addNS('label','inkscape'):name,
            'd':data}
    inkex.etree.SubElement(parent, inkex.addNS('path','svg'), line_attribs )

class Intersection:
    def __init__(self, row, column):
        self.row = row
        self.column = column
    
class JigsawPuzzle(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--random_seed", action="store", type="int", dest="random_seed", default=0, help="Seed for randomness") 
        self.OptionParser.add_option("--puzzle_width", action="store", type="int", dest="puzzle_width", default=300, help="Width of the puzzle")
        self.OptionParser.add_option("--puzzle_height", action="store", type="int", dest="puzzle_height", default=200, help="Height of the puzzle")
        self.OptionParser.add_option("--tiles_width", action="store", type="int", dest="tiles_width", default=15, help="Number of tiles across")
        self.OptionParser.add_option("--tiles_height", action="store", type="int", dest="tiles_height", default=10, help="Number of tiles high")
        self.OptionParser.add_option("--tab_size", action="store", type="float", dest="tab_size", default=15.0, help="Size of the tabs in %")
        self.OptionParser.add_option("--jitter", action="store", type="float", dest="jitter", default=4.0, help="Random factor (jitter)")

    def effect(self):

        # Processing of the options
        self.options.halfTabSizePct = self.options.tab_size / 200.0
        self.options.jitterPct = self.options.jitter / 100.0

        # Put in in the center of the current view
        view_center = computePointInNode(list(self.view_center), self.current_layer)
        t = 'translate(' + str( view_center[0]- self.options.puzzle_width/2.0) + ',' + \
                           str( view_center[1]- self.options.puzzle_height/2.0) + ')'

        # Create group for entire puzzle and each of the horizontal and vertical cuts
        g_attribs = {inkex.addNS('label','inkscape'):'Puzzle','transform':t }
        puzzle_group = inkex.etree.SubElement(self.current_layer, 'g', g_attribs)
        g_attribs = {inkex.addNS('label','inkscape'):'Rows' }
        rows_group = inkex.etree.SubElement(puzzle_group, 'g', g_attribs)
        g_attribs = {inkex.addNS('label','inkscape'):'Columns' }
        columns_group = inkex.etree.SubElement(puzzle_group, 'g', g_attribs)

        # Styles for the lines
        outline_style = { 'stroke': '#FF0000', 'stroke-width':str(0.1), 'fill': 'none'}
        horizontal_style = { 'stroke': '#00ba00', 'stroke-width':str(0.1), 'fill': 'none'}
        vertical_style = { 'stroke': '#0000ff', 'stroke-width':str(0.1), 'fill': 'none'}

        # Puzzle border
        rect_attribs = {'style':simplestyle.formatStyle(outline_style),
                        inkex.addNS('label','inkscape'):'PuzzleBorder',
                        'x':str(0), 'y':str(0), 'width':str(self.options.puzzle_width), 'height':str(self.options.puzzle_height)}
        inkex.etree.SubElement(puzzle_group, inkex.addNS('rect','svg'), rect_attribs )

        # Seed random, if appropriate
        if self.options.random_seed > 0:
            random.seed(self.options.random_seed)

        # Generate some values to use in initial setup
        # Note: routine will call this regularly even if no random values are needed.  This ensures that when more options are added
        #   that require random values, we won't add new calls and breaks seed values resulting in the same puzzle.  Still likely to
        #   break seeds sometimes but this should hopefully minimize that
        self.generateRandomValues()

        columnWidth = float(self.options.puzzle_width) / float(self.options.tiles_width)
        rowWidth = float(self.options.puzzle_height) / float(self.options.tiles_height)

        # Build array of intersection points
        intersections = list()
        for row in range(0, self.options.tiles_height + 1):
            intersections.append(list())
            for column in range(0, self.options.tiles_width + 1):
                self.generateRandomValues()
                intersections[row].append(Intersection(row * rowWidth, column * columnWidth))

        # Horizontal Lines - go through each row and make connections between the column points
        for row in range(1, self.options.tiles_height):
            self.generateRandomValues()
            # Paths should alternate which side they start on, set up the column range appropriately
            columnRange = range(0, self.options.tiles_width)
            nextColumnDirection = 1
            if (row % 2) == 0:
                columnRange = range(self.options.tiles_width, 0, -1)
                nextColumnDirection = -1

            firstColumn = True
            for column in columnRange:
                self.generateRandomValues()
                if firstColumn:
                    pathData = "M" + str(intersections[row][column].column) + "," + str(intersections[row][column].row) + " "

                pathData += self.pathDataForLineWithOneTab(firstColumn, 
                    intersections[row][column], # Starting point 
                    intersections[row][column + nextColumnDirection]) # Ending point

                firstColumn = False
    
            addPath(rows_group, horizontal_style, 'row'+str(row), pathData)

        # Vertical Lines - go through each column and make connections between the row points
        for column in range(1, self.options.tiles_width):
            self.generateRandomValues()
            # Paths should alternate which side they start on, set up the row range appropriately
            rowRange = range(0, self.options.tiles_height)
            nextRowDirection = 1
            if (row % 2) == 0:
                rowRange = range(self.options.tiles_height, 0, -1)
                nextRowDirection = -1

            firstRow = True
            for row in rowRange:
                self.generateRandomValues()
                if firstRow:
                    pathData = "M" + str(intersections[row][column].column) + "," + str(intersections[row][column].row) + " "

                pathData += self.pathDataForLineWithOneTab(firstRow, 
                    intersections[row][column], # Starting point 
                    intersections[row + nextRowDirection][column]) # Ending point

                firstRow = False

            addPath(columns_group, vertical_style, 'column'+str(column), pathData)

    # Generates a path between start and end with a single tab in a random direction
    # Uses self.randomJitter12-15 and self.randomBool9
    def pathDataForLineWithOneTab(self, firstTile, intersectionStart, intersectionEnd):
        jitter1 = self.randomJitter15
        jitter2 = self.randomJitter14
        jitter3 = self.randomJitter13
        jitter4 = self.randomJitter12

        if self.randomBool9:
            direction = -1
        else:
            direction = 1

        if firstTile: # first tile needs a control point, others can just continue the previous one
            pathData = "C"
            # control point 1 - 20% along the line, with a jitter1 off the line
            pathData += self.pointAlongLine(intersectionStart, intersectionEnd, .2, direction * jitter1)
            pathData += ","
        else:
            pathData = "S"

        # control point 2 - 50% + jitter2 + jitter4 along the line, -half tab size + jitter3 off the line 
        pathData += self.pointAlongLine(intersectionStart, intersectionEnd, 
            .5 + jitter2 + jitter4, direction * (-self.options.halfTabSizePct + jitter3))
        pathData += ","
        # Tab point 1 - 50% - half tab + jitter2 along the line, half tab + jitter3 off the line
        pathData += self.pointAlongLine(intersectionStart, intersectionEnd, 
            .5 - self.options.halfTabSizePct + jitter2, direction * (self.options.halfTabSizePct + jitter3))
        pathData += " "

        pathData += "C"
        # control point 3 - 50% - tab + jitter2 - jitter4 along the line, 1.5 * tab + jitter3 off the line
        pathData += self.pointAlongLine(intersectionStart, intersectionEnd, 
            .5 - 2.0 * self.options.halfTabSizePct + jitter2 - jitter4, direction * (3.0 * self.options.halfTabSizePct + jitter3))
        pathData += ","
        # control point 4 - 50% + tab + jitter2 - jitter4 along the line, 1.5 * tab + jitter3 off the line
        pathData += self.pointAlongLine(intersectionStart, intersectionEnd, 
            .5 + 2.0 * self.options.halfTabSizePct + jitter2 - jitter4, direction * (3.0 * self.options.halfTabSizePct + jitter3))
        pathData += ","
        # Tab point 2 - 50% + half tab + jitter2 along the line, half tab + jitter3 off the line
        pathData += self.pointAlongLine(intersectionStart, intersectionEnd, 
            .5 + self.options.halfTabSizePct + jitter2, direction * (self.options.halfTabSizePct + jitter3))
        pathData += " "

        pathData += "C"
        # control point 5 - 50% + jitter2 + jitter4 along the line, -half tab size + jitter3 off the line 
        pathData += self.pointAlongLine(intersectionStart, intersectionEnd, 
            .5 + jitter2 + jitter4, direction * (-self.options.halfTabSizePct + jitter3))
        pathData += ","
        # control point 6 - 80% along the line, with a jitterE (related to jitter1) off the line
        pathData += self.pointAlongLine(intersectionStart, intersectionEnd, .8, direction * (jitter1))
        pathData += ","
        # End point - 100% along the line
        pathData += str(intersectionEnd.column) + "," + str(intersectionEnd.row) 
        pathData += " "

        return pathData

    def pointAlongLine(self, intersectionStart, intersectionEnd, percentAlong, percentOff):
        # return a point along and off the line provided
        diffX = intersectionEnd.column - intersectionStart.column
        diffY = intersectionEnd.row - intersectionStart.row
        returnX = intersectionStart.column + diffX * percentAlong + diffY * percentOff
        returnY = intersectionStart.row + diffY * percentAlong + diffX * percentOff
        return str(returnX) + "," + str(returnY)

    def generateRandomValues(self):
        # Generate a set of random values to use in each section of path generation
        # These are pregenerated these so that as things are tweaked new random values don't break a seed... hopefully
        # In general, specific path generation will use the high numbers, core routines to build tiles will use the low numbers
        self.randomJitter1 = self.randomJitter()
        self.randomJitter2 = self.randomJitter()
        self.randomJitter3 = self.randomJitter()
        self.randomJitter4 = self.randomJitter()
        self.randomJitter5 = self.randomJitter()
        self.randomJitter6 = self.randomJitter()
        self.randomJitter7 = self.randomJitter()
        self.randomJitter8 = self.randomJitter()
        self.randomJitter9 = self.randomJitter()
        self.randomJitter10 = self.randomJitter()
        self.randomJitter11 = self.randomJitter()
        self.randomJitter12 = self.randomJitter()
        self.randomJitter13 = self.randomJitter()
        self.randomJitter14 = self.randomJitter()
        self.randomJitter15 = self.randomJitter()
        self.randomBool1 = randomBool()
        self.randomBool2 = randomBool()
        self.randomBool3 = randomBool()
        self.randomBool4 = randomBool()
        self.randomBool5 = randomBool()
        self.randomBool6 = randomBool()
        self.randomBool7 = randomBool()
        self.randomBool8 = randomBool()
        self.randomBool9 = randomBool()

    def randomJitter(self):
        return random.uniform(-self.options.jitterPct, self.options.jitterPct)

if __name__ == '__main__':
    e = JigsawPuzzle()
    e.affect()
