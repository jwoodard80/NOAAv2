__author__ = 'jwoodard'


from lxml import etree

root = etree.parse("http://forecast.weather.gov/MapClick.php"
                   "?lat=35.8916&lon=-90.65833299999997&unit=0&lg=english&FcstType=dwml")

# root = etree.parse('forecast_sample.xml')

layoutKeys = {}

test1 = root.xpath('/dwml/data[1]/location[1]/area-description')


for timeLayouts in root.findall('.//time-layout'):
    layoutKeys[timeLayouts.find('layout-key').text] = []

    for StartValidTime in timeLayouts.findall('start-valid-time'):
        test = [StartValidTime.get('period-name')]
        layoutKeys[timeLayouts.find('layout-key').text].append(test)

temps1 = {}
for temps in root.findall('.//temperature'):
    i = 0
    for test in temps.findall("value"):
        layoutKeys[temps.get('time-layout')][i].append(test.text)
        i += 1

    # print test

# re-format this as a function

for precip in root.findall('.//probability-of-precipitation'):
    i = 0
    for rain in precip.findall('value'):
        if rain.text is not None:
            layoutKeys[precip.get('time-layout')][i].append(rain.text)
        else:
            layoutKeys[precip.get('time-layout')][i].append(str(0))
        i += 1

for x in root.findall('.//weather'):
    i = 0
    for conditions in x.findall('weather-conditions'):
        if conditions.get('weather-summary'):
            layoutKeys[x.get('time-layout')][i].append(conditions.get('weather-summary'))
        i += 1

for x in root.findall('.//wordedForecast'):
    i = 0
    for forecast in x.findall('text'):
        layoutKeys[x.get('time-layout')][i].append(forecast.text)
        i += 1


for k, v in layoutKeys.iteritems():
    for l in v:
        print l[0] + ' | ',



print ''

'''
Knots * 1.15 = MPH



Wind Direction Conversion Table

<conversion-table>
 <conversion-key>wind-direction</conversion-key>
 <start-value>23</start-value>
 <end-value>67</end-value>
 <equivalent-value>NE</equivalent-value>
 <start-value>68</start-value>
 <end-value>112</end-value>
 <equivalent-value>E</equivalent-value>
 <start-value>113</start-value>
 <end-value>157</end-value>
 <equivalent-value>SE</equivalent-value>
 <start-value>158</start-value>
 <end-value>202</end-value>
 <equivalent-value>SE</equivalent-value>
 <start-value>203</start-value>
 <end-value>247</end-value>
 <equivalent-value>SW</equivalent-value>
 <start-value>248</start-value>
 <end-value>292</end-value>
 <equivalent-value>W</equivalent-value>
 <start-value>293</start-value>
 <end-value>337</end-value>
 <equivalent-value>NW</equivalent-value>
 <start-value>338</start-value>
 <end-value>22</end-value>
 <equivalent-value>N</equivalent-value>
 </conversion-table>
'''
