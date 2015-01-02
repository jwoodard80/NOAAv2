__author__ = 'jonathan'

'''
23  - 67  NE
68  - 112 E
113 - 157 SE
158 - 202 S
203 - 247 SW
248 - 292 W
293 - 337 NW
338 - 22  N
'''


deg = 68

if 23 <= deg <= 67:
    print "NorthEast"
elif 68 <= deg <= 112:
    print "East"
elif 113 <= deg <= 157:
    print "SouthEast"
elif 158 <= deg <= 202:
    print "South"
elif 203 <= deg <= 247:
    print "SouthWest"
elif 248 <= deg <= 292:
    print "West"
elif 293 <= deg <= 337:
    print "NorthWest"
elif 338 <= deg <= 360 or deg <= 22:
    print "North"