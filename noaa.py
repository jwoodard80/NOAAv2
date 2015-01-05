__author__ = 'jwoodard'

# TODO: Error Checking
# TODO: Argparse for "all, current, week, week-ext, curr and 7-day *default

from lxml import etree
from tabulate import tabulate
import requests
import argparse
import textwrap


def degree2direction(deg):
    if 23 <= deg <= 67:
        return "NorthEast"
    elif 68 <= deg <= 112:
        return "East"
    elif 113 <= deg <= 157:
        return "SouthEast"
    elif 158 <= deg <= 202:
        return "South"
    elif 203 <= deg <= 247:
        return "SouthWest"
    elif 248 <= deg <= 292:
        return "West"
    elif 293 <= deg <= 337:
        return "NorthWest"
    elif 338 <= deg <= 360 or deg <= 22:
        return "North"

parser = argparse.ArgumentParser()
parser.add_argument("zipcode", help="Zipcode", type=str)
parser.add_argument("-a", action='store_true', help="Full forecast (Current & 7day)")
parser.add_argument("-c", action='store_true', help="Current Conditions")
parser.add_argument("-f", action='store_true', help="7 day forecast")
parser.add_argument("-e", action='store_true', help="7 day Extended")
args = parser.parse_args()

url = "http://graphical.weather.gov/xml/sample_products/browser_interface/ndfdXMLclient.php"
query = {'listZipCodeList': args.zipcode}


try:
    root = etree.fromstring(requests.get(url, params=query, timeout=2).text)

except (requests.Timeout, requests.ConnectionError, etree.XMLSyntaxError), e:
    print "Lat/Lon ERROR:" + str(e)
    exit()


location = root.xpath('/dwml/latLonList[1]')[0].text
LatLonList = location.split(',')

try:
    root = etree.parse("http://forecast.weather.gov/MapClick.php"
                    "?lat="+LatLonList[0]+"&lon="+LatLonList[1]+"&unit=0&lg=english&FcstType=dwml")
except (requests.Timeout, requests.ConnectionError, etree.XMLSyntaxError), e:
    print "Forecast ERROR:" + str(e)
    exit()

current = []
current.append(root.xpath('/dwml/data[2]/location/area-description')[0].text)
for x in root.xpath('/dwml/data[2]/location/point')[0].values():
    current.append(x)
current.append(root.xpath('/dwml/data[2]/location/height')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/weather[1]/weather-conditions[1]')[0].get('weather-summary'))
current.append(root.xpath('/dwml/data[2]/parameters[1]/temperature[1]/value[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/temperature[2]/value[1]')[0].text)
current.append(root.xpath('/dwml/data[2]/parameters[1]/humidity[1]/value[1]')[0].text)
current.append(degree2direction(int(root.xpath('/dwml/data[2]/parameters[1]/direction[1]/value')[0].text)))
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
        forecasts.append(textwrap.fill(y.text, width=120))
        i += 1

wordedForecasts = zip(periods, forecasts)


if args.a or args.c:
    print '''
    ======================
    Current Observations
    ======================\n
    {}
    -----------------------------------------
    Lat: {} | Lon {} | Sea Level: {}

    Currently: {}
    ----------------------------------------
    Temp: {} | Dew Point: {} | Humidity: {}
    Wind Direction: {} | Speed: {} Mph
    Visibility: {} Miles | Barometer: {} Inches
    '''.format(*current)

if args.a or args.f:
    print '\n'
    print '==============='
    print "7-Day Weather      "
    print '==============='

    headers = ["Time", "Temp", "Precip", "Overall"]
    for k, v in weather.iteritems():
        print tabulate(v, headers, tablefmt="grid")

if args.a or args.e:
    print '\n'
    print '========================='
    print '7-day Extended Forecast'
    print '=========================\n'

    for item in wordedForecasts:
        y = ''
        print item[0]
        for x in item[0] + '   ':
            y += '-'
        print y
        print item[1] + "\n"
