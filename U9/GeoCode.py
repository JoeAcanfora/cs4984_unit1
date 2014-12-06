__author__ = 'joeacanfora'


from pygeocoder import Geocoder
from nltk import *


def main():
    # locations = ['China', 'Zhejiang', 'Hubei', 'Shaanxi', 'Beijing', 'Wuhan', 'Hunan', 'Seconds', 'Bangladesh', 'Lanxi']
    locations = ['China', 'Zhejiang', 'Hubei', 'Shaanxi', 'Beijing', 'Wuhan', 'Hunan', 'Seconds', 'Bangladesh', 'Lanxi', 'Wangmo', 'Robertsons' 'Guizhou', 'Chinese', 'Europe', 'Africa',  'Sichuan', 'Harbin', 'India',  'Liaoning', 'Fujian', 'Shanghai', 'New York', 'Imminent', 'Piaohe', 'Western', 'USTroy', 'Washington', 'HomeAtheists', 'Commission', 'Singapore', 'Hell SECTIONSChurch', 'San Quentin', 'Libya', 'Pays Almost', 'Hangzhou', 'Fuzhou', 'March', 'Guangdong', 'Jiangxi', 'HomeFacebook', 'Xikou', 'Ohio Primary', 'Loudi', 'Taipei', 'Xinhua', 'Sikkim', 'Zhouqu', 'Linxiang', 'Chauvet']
    cities = []
    provinces = []
    states = []
    for place in locations:
        result
        try:
            result = Geocoder.geocode(place)
        catch ZERO_RESULTS:
            continue
        # print(str(result[0]))
        rArray = str(result).split(',')
        # print(rArray)

        if rArray.__len__() >= 3 :
            states.append(rArray[rArray.__len__() - 1])
            provinces.append(rArray[rArray.__len__() - 2])
            cities.append(rArray[rArray.__len__() - 3])
        elif rArray.__len__() == 2:
            states.append(rArray[1])
            provinces.append(rArray[0])
        else:
            states.append(rArray[0])

    fdistCities = FreqDist(cities)
    print(fdistCities.most_common(3))
    fdistProvinces = FreqDist(provinces)
    print(fdistProvinces.most_common(5))
    fdistState = FreqDist(states)
    print(fdistState.most_common(1))



def getCoords(coords):

    xy = str(coords).split(",", 2)
    x = xy[0][1:]
    y = xy[1][:-1]
    result = [float(x), float(y)]
    return result

if __name__ == "__main__":
    main()



