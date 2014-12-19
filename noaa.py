__author__ = 'jwoodard'


from lxml import etree

root = etree.parse("http://forecast.weather.gov/MapClick.php"
                   "?lat=35.8916&lon=-90.65833299999997&unit=0&lg=english&FcstType=dwml")

layoutKeys = {}

for timeLayouts in root.findall('.//time-layout'):
    layoutKeys[timeLayouts.find('layout-key').text] = {}

    for StartValidTime in timeLayouts.findall('start-valid-time'):
        layoutKeys[timeLayouts.find('layout-key').text][StartValidTime.get('period-name')] = []

for times in root.findall('.//temperature/value'):
    print times.text


print ''