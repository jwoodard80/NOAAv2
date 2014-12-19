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

print 'end'