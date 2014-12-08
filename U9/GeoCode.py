__author__ = 'joeacanfora'


from pygeocoder import Geocoder
from nltk import *


def main():
    # locations = ['China', 'Zhejiang', 'Hubei', 'Shaanxi', 'Beijing', 'Wuhan', 'Hunan', 'Seconds', 'Bangladesh', 'Lanxi']
    #locations = ['China', 'Zhejiang', 'Hubei', 'Shaanxi', 'Beijing', 'Wuhan', 'Hunan', 'Seconds', 'Bangladesh', 'Lanxi', 'Wangmo', 'Robertsons' 'Guizhou', 'Chinese', 'Europe', 'Africa',  'Sichuan', 'Harbin', 'India',  'Liaoning', 'Fujian', 'Shanghai', 'New York', 'Imminent', 'Piaohe', 'Western', 'USTroy', 'Washington', 'HomeAtheists', 'Commission', 'Singapore', 'Hell SECTIONSChurch', 'San Quentin', 'Libya', 'Pays Almost', 'Hangzhou', 'Fuzhou', 'March', 'Guangdong', 'Jiangxi', 'HomeFacebook', 'Xikou', 'Ohio Primary', 'Loudi', 'Taipei', 'Xinhua', 'Sikkim', 'Zhouqu', 'Linxiang', 'Chauvet']
    s_locations = [('Pakistan', 1520), ('Sindh', 962), ('District', 165), ('Punjab', 159), ('Khyber', 156), ('Kotri', 155), ('Sri Lanka', 108), ('Rato Dero', 81), ('Kohat', 81), ('Nasirabad', 80), ('Guddu', 80), ('Badin', 79), ('Africa', 76), ('Nature', 72), ('China', 70), ('Karachi', 67), ('April', 67), ('India', 65), ('Peshawar', 63), ('August', 59), ('Islamabad', 57), ('Russian', 54), ('September', 50), ('South', 48), ('Balochistan', 47), ('North', 44), ('Disaster', 36), ('BANGKOK', 36), ('Infectious', 36), ('Somalia', 33), ('Valley', 32), ('January', 32), ('Russia', 29), ('Baluchistan', 29), ('Haiti', 26), ('New York', 26), ('Pakistans', 25), ('Darfur', 21), ('USAID', 20), ('Stockholm', 20), ('Geneva', 20), ('ISLAMABAD', 20), ('Singapore', 19), ('Tatta', 18), ('Manchar', 18), ('Bolan', 18), ('Kohistan', 18), ('Australian', 18), ('KARACHI', 18), ('Badalai', 18)] 
    locations = []
    for x in s_locations:
        n = 0
        while n < x[1]:
            locations.append(x[0])
            n = n+1
    cities = []
    provinces = []
    states = []
    for place in locations:
        result = None
        try:
            result = Geocoder.geocode(place)
        except:
            pass
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



