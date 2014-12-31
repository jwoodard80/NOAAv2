__author__ = 'jwoodard'

# TODO: Implement degrees to Compass direction
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

from lxml import etree
from tabulate import tabulate
import requests
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("zipcode", help="Zipcode",
                    type=str)
args = parser.parse_args()

url = "http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"
query = {'listZipCodeList': args.zipcode}
root = etree.fromstring(requests.get(url, params=query).text)
location = root.xpath('/dwml/latLonList[1]')[0].text
LatLonList = location.split(',')

root = etree.parse("http://forecast.weather.gov/MapClick.php"
                   "?lat="+LatLonList[0]+"&lon="+LatLonList[1]+"&unit=0&lg=english&FcstType=dwml")
current = []
current.append(root.xpath('/dwml/data[2]/location/area-description')[0].text)
for x in root.xpath('/dwml/data[2]/location/point')[0].values():
    current.append(x)
current.append(root.xpath('/dwml/data[2]/location/height')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/weather[1]/weather-conditions[1]')[0].get('weather-summary'))
current.append(root.xpath('/dwml/data[2]/parameters[1]/temperature[1]/value[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/temperature[2]/value[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/humidity[1]/value[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/direction[1]/value')[0].text)
current.append(int(root.xpath('/dwml/data[2]/parameters[1]/wind-speed[2]/value[1]')[0].text) * 1.15)
current.append(
    root.xpath('/dwml/data[2]/parameters[1]/weather[1]/weather-conditions[2]/value[1]/visibility[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/pressure[1]/value[1]')[0].text)

weather = {}

fortnight = root.xpath("/dwml/data[1]/time-layout[1]/layout-key[1]")[0].text

for x in root.xpath('/dwml/data[1]/time-layout[1]'):
    weather[x.find('layout-key').text] = []
    periods = []
    for y in x.findall('start-valid-time'):
        z = [y.get('period-name')]
        periods.append(z[0])
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
    forecasts = []
    for y in x.findall('text'):
        forecasts.append(y.text)
        # weather[x.get('time-layout')][i].append(y.text)
        i += 1

wordedForecasts = zip(periods, forecasts)

print '''
{}
-----------------------------------------
Lat: {} | Lon {} | Sea Level: {}

Current obervations: {}
----------------------------------------
Temp: {} | Dew Point: {} | Humidity: {}
Wind Direction: {} Degrees | Speed: {} Mph
Visibility: {} Miles | Barometer: {} Inches
'''.format(*current)

print '\n'
print "7-Day Weather      "
print '-------------------'

headers = ["Time", "Temp", "Precip", "Overall"]
for k, v in weather.iteritems():
    print tabulate(v, headers, tablefmt="grid")

print '\n'
print '7-day Extended Forecast'
print '-------------------------'
headers = ['Time Period', 'Forecast']
print tabulate(wordedForecasts, headers, tablefmt='grid')