'''
VISION
-- IDENTIFICATION: 
    - identifies: player, resource, water, land, forests, relics
-- INITIAL SCORING:
    - score a player's map based on proximity of resource, relics and forest/gaps/terrain
    - score reflect how challenging/bad the map is
    - may be also use it to detect bugged resource? (ex: gold bloacked on 4 sides by wood)
-- MAP CONTROL
    - as game progresses, reflects player control based on color distribution
'''


# Notes about color interference from UI elements
# -- UI buttons, minimap borders, panel background etc
# -- the interefecnt also depends on DIFF value (i.e TOLERANCE) in compare_rgb function
# -- the points gained in pie chart are relative to the total number of colors we identify, since its a percentage