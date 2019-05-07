"""
program BestRoute.py
Author: Xingfu Zhu
Last date modified:05/06/19
The purpose of this program is to find the temperature forecasts for the next 5 days for the 5 given cities.
For each day and each city find the highest temperature, resulting in 25 value for you to work with.

"""

import requests
import json
from itertools import permutations

API_KEY = "6d1a0921393908b1741d4cb1ee1aaffc"
WS_URL = "https://api.openweathermap.org/data/2.5/forecast"

class City:
    """ representing a city incluting the forecast max temperatures  for each of the next 5 days"""
    def __init__(self,name,temperatures):
        """constructor """
        self.name = name
        self.temps = temperatures

    def get_temperature(self,day):
        return self.temps[day]

    def __str__(self):
        return self.name

class Route:
    """ a route represents a sequents of cities"""
    def __init__(self,path,avg_temp):
        self.path = path
        self.avg_temp = avg_temp

    def city_path(self):
        """ return the sequents of cities """
        return self.path

    def __str__(self):
        """ :return the average temperature """
        return self.avg_temp

# get 120 kinds of avaerage temperatures from 5 cities
def best_route(id_list):
    """getting the lowest temperature and city path"""
    cities = []
    path_cities = []
    # one of cites list in total city_id_lists
    for id in id_list:
        cities.append(fetch_weather(id))  # looking for every city and 5 days hightest temperatures list
    avg_temp = 0
    # getting 5 cities average temperature
    for i in range(len(cities)):
        avg_temp += cities[i].get_temperature(i)
        path_cities.append(cities[i].name)  # get the city list
    avg_temp = round(avg_temp / len(cities), 2)
    print("The average temperature is:" + str(avg_temp) +"   and the path of cities is: " + " ->".join(path_cities))
    return  Route(path_cities,avg_temp)

#get the five days hightest termperature for every city
def fetch_weather(id):
    """getting five cities of five days of the highest temperature """
    query_string = "?id={}&units=imperial&APIKEY={}".format(id, API_KEY)
    request_url = WS_URL + query_string
    #print("request URL:",request_url)
    response = requests.get(request_url)
    ###########################################################################
    # if response.status_code == 200:
    #     d = response.json()
    #     city_name = d["city"]['name']
    #     lst = d['list']
    #     temp_list = []
    #     for i in range(len(lst)//8):
    #         li = [x for x in range(len(lst)) if x //8 == i]
    #         temp_list.append(max([lst[j]["main"]["temp_max"] for j in li]))
    #     return City(city_name,temp_list)
    ###########################################################################
    if response.status_code == 200:
        d = response.json()
        city_name = d["city"]['name']
        city_days_temp = []
        day_temps = []
        #get the first day such as 2019-05-06
        day = d["list"][0]["dt_txt"][0:10]
        # looking for max temperatures for 5 days in one city
        for i in range(len(d["list"])):
            if day == d["list"][i]["dt_txt"][0:10]: # find out the same day
               day_temps.append(d["list"][i]["main"]["temp_max"]) # the list keeps the temp_maxs of one day

            # if the record is the next day, get the max temperature for before day and initiates list and day
            else:
               city_days_temp.append(max(day_temps))
               day_temps = [] #initiate the day_temp_list
               day = d["list"][i]["dt_txt"][0:10] #initiate the next day
               day_temps.append(d["list"][i]["main"]["temp_max"]) #get the first record for the next day
        return City(city_name, city_days_temp)

    else:
        print("How should I know?")
        return None

if __name__ == "__main__":
    #city_id_list = [5313667,5294810,5318313, 5308655,5301388]
    city_id_list = json.loads(open("cities.json").read())
    lowest_temp = 100  #initiate the lowest temperature

    lowest_temp_path_city = [] #initate the list for return of average temperature and cities list
    # permutate for total items 5*4*3*2=120
    for id_list in permutations(city_id_list):
        # call the founcation best_route and paramenter for id_list in 120
        lowest_temp_path_city.append(best_route(id_list))

    lowest_temp=100.0 # initiate the lowest temperature for 100
    #looking for the lowest temperature and record the path cities
    for i in range(len(lowest_temp_path_city)):

        if lowest_temp_path_city[i].avg_temp <lowest_temp:
            lowest_temp = lowest_temp_path_city[i].avg_temp
            best_path = lowest_temp_path_city[i].path #record the path cities
    print("**********************************************************************************************************************")
    print("The lowest average temperature high of "+str(lowest_temp)+" is forecast for this route:"+"->".join(best_path) )
    print("**********************************************************************************************************************")

