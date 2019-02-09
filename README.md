# Inkscape Jigsaw Puzzle
A jigsaw puzzle generator extension for Inkscape

## Prior Art
The initial code and logic is based on this gist: https://gist.github.com/Draradech/35d36347312ca6d0887aa7d55f366e30

## Overview
First version is basically just a rewrite of that logic to understand how that code works and to get a working Inkscape extension up and running.  There are a few tweaks to things done to be slightly optimized for my [Glowforge](https://glowforge.us/BHZAKLOU) laser:
- Rows/Columns/Bounding box are each a different color to be a different job in the [Glowforge](https://glowforge.us/BHZAKLOU)
- Row and Column paths alternate directions which, if I understand it correctly, will cause the laser to cut back and forth reducing the cutting time slightly.

## Installation
Save the inx and py file into your local extensions directory for Inkscape (the directory is listed at Edit > Preferences > System: User extensions).

## Usage
After restarting Inkscape, it can be run via Extensions > Render > Jigsaw Puzzle Generator...

![Options dialog](/images/Options.png?raw=true)

Quick descriptions of the options:
- Seed: if not 0, used as the seed of the random number generator so a puzzle with the same settings should result in the same design.  Potentially will break between versions during development.
- Width/Height: size of puzzle in millimeters.
- Tiles across/high: number of puzzle pieces.
- Size of tabs (%): size of the tabs as a percentage of the tile size.
- Randomeness factor (%): maximum amount to randomize the design - again as a percent of the tile
- Randomness factor for intersections: This is a multiplier on the randomness factor (so 0 is no effect, 2 is twice the effect) for moving the path intersections around.  The bigger the number here, the more irregular the pieces will be.  NOTE: This can easily go horribly wrong. A randomness % of 10% and multiplier of 5 will make a mess.  The more you use this, the more you need to look closely at the resulting paths to watch for overlaps.

## Example
![Sample Puzzle Part](/images/PuzzlePart.png?raw=true)

## Future
My hope is to update and add options to this to create more unique puzzle styles, suggestions and pull requests welcome!