__author__ = 'jwoodard'


from lxml import etree

root = etree.parse("http://forecast.weather.gov/MapClick.php"
                   "?lat=35.8916&lon=-90.65833299999997&unit=0&lg=english&FcstType=dwml")

# root = etree.parse('forecast_sample.xml')

layoutKeys = {}


for timeLayouts in root.findall('.//time-layout'):
    layoutKeys[timeLayouts.find('layout-key').text] = []

    for StartValidTime in timeLayouts.findall('start-valid-time'):
        test = [StartValidTime.get('period-name')]
        layoutKeys[timeLayouts.find('layout-key').text].append(test)

temps1 = {}
for temps in root.findall('.//temperature'):
    i = 0
    for test in temps.findall("value"):
        print layoutKeys[temps.get('time-layout')][i].append(test.text)
        print str(i) + ' ' + test.text
        #print test.text
        i += 1
    print temps.get('time-layout')
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

for x in root.findall('wordedForecast'):
    i = 0
    for forecast in x.findall('text'):
        layoutKeys[x.get('time-layout')][i].append(forecast.text)
        i += 1


print 'end'