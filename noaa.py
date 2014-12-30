__author__ = 'jwoodard'

from lxml import etree
from tabulate import tabulate

root = etree.parse("http://forecast.weather.gov/MapClick.php"
                   "?lat=35.8916&lon=-90.65833299999997&unit=0&lg=english&FcstType=dwml")

current =[]
current.append(root.xpath('/dwml/data[2]/location/area-description')[0].text)
for x in root.xpath('/dwml/data[2]/location/point')[0].values():
    current.append(x)
current.append(root.xpath('/dwml/data[2]/location/height')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/weather[1]/weather-conditions[1]')[0].get('weather-summary'))
current.append(root.xpath('/dwml/data[2]/parameters[1]/temperature[1]/value[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/temperature[2]/value[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/humidity[1]/value[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/weather[1]/weather-conditions[2]/value[1]/visibility[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/pressure[1]/value[1]')[0].text)

weather = {}
currently = root.xpath('/dwml/data[1]/location[1]/area-description')
fortnight = root.xpath("/dwml/data[1]/time-layout[1]/layout-key[1]")[0].text

for x in root.xpath('/dwml/data[1]/time-layout[1]'):
    weather[x.find('layout-key').text] = []

    for y in x.findall('start-valid-time'):
        z = [y.get('period-name')]
        weather[x.find('layout-key').text].append(z)

for x in root.xpath('/dwml/data[1]/parameters[1]/temperature'):
    i = 0 if x.get("time-layout")[-1] == '1' else 1

    for y in x.findall("value"):
        weather[fortnight][i].append(y.text)
        i += 2

for x in root.findall('.//probability-of-precipitation'):
    i = 0

    for y in x.findall('value'):
        if y.text is not None:
            weather[x.get('time-layout')][i].append(y.text)
        else:
            weather[x.get('time-layout')][i].append(str(0))
        i += 1

for x in root.xpath('/dwml/data[1]/parameters[1]/weather'):
    i = 0

    for y in x.findall('weather-conditions'):
        if y.get('weather-summary'):
            weather[fortnight][i].append(y.get('weather-summary'))
        i += 1

for x in root.findall('.//wordedForecast'):
    i = 0

    for y in x.findall('text'):
        weather[x.get('time-layout')][i].append(y.text)
        i += 1




# Point Forecast
print '''
{}
-----------------------------------------
Lat: {} | Lon {} | Sea Level: {}

Current obervations: {}
----------------------------------------
Temp: {} | Dew Point: {} | Humidity: {}
Visibility: {} Miles | Wind: N 9
Barometer: {} inches
'''.format(*current)
print '\n'
print "7-Day Weather      "
print '-------------------'

headers = ["Time", "Temp", "Precip", "Overall", "Forecast"]
for k, v in weather.iteritems():
    print tabulate(v, headers, tablefmt="grid")

# ----------------------------------------------------------------------
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