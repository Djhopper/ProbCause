import numpy as np
import pandas as pd
from enum import Enum
import random
import csv

column_names = ["VehicleType", "SecondVehicleType", "Date", "Time", "RoadHasPavement", "DistanceToNearestTrafficLight",
                "Speed Limit", "EstimatedSpeedOfCollision",  "SeatBeltUsed", "InjurySustained", "Lethal", "LandUse",
                "City"]


def weighted_random_choice(choices):
    maximum = sum(choices.values())
    pick = random.uniform(0, maximum)
    current = 0
    for key, value in choices.items():
        current += value
        if current > pick:
            return key


class Vehicle(Enum):
    Car = "Car"
    Bicycle = "Bicycle"
    Pedestrian = "Pedestrian"
    Motorbike = "Motorbike"


probability_vehicle_given_speed_limit = {
    20: {Vehicle.Car: 5, Vehicle.Motorbike: 8, Vehicle.Pedestrian: 20, Vehicle.Bicycle: 15},
    30: {Vehicle.Car: 5, Vehicle.Motorbike: 3, Vehicle.Pedestrian: 10, Vehicle.Bicycle: 15},
    40: {Vehicle.Car: 10, Vehicle.Motorbike: 6, Vehicle.Pedestrian: 4, Vehicle.Bicycle: 3},
    50: {Vehicle.Car: 5, Vehicle.Motorbike: 1, Vehicle.Pedestrian: 0.1, Vehicle.Bicycle: 0.15},
    60: {Vehicle.Car: 5, Vehicle.Motorbike: 1, Vehicle.Pedestrian: 0, Vehicle.Bicycle: 0},
    70: {Vehicle.Car: 5, Vehicle.Motorbike: 1, Vehicle.Pedestrian: 0, Vehicle.Bicycle: 0},
}
vehicle_lethality_multiplier = {
    (Vehicle.Car, Vehicle.Car): 2,
    (Vehicle.Car, Vehicle.Bicycle): 1,
    (Vehicle.Car, Vehicle.Pedestrian): 0.8,
    (Vehicle.Car, Vehicle.Motorbike): 4,
    (Vehicle.Bicycle, Vehicle.Bicycle): 0,
    (Vehicle.Bicycle, Vehicle.Pedestrian): 0,
    (Vehicle.Bicycle, Vehicle.Motorbike): 2.8,
    (Vehicle.Pedestrian, Vehicle.Pedestrian): 0,
    (Vehicle.Pedestrian, Vehicle.Motorbike): 2.3,
    (Vehicle.Motorbike, Vehicle.Motorbike): 3,
}
vehicle_injury_multiplier = {
    (Vehicle.Car, Vehicle.Car): 1.5,
    (Vehicle.Car, Vehicle.Bicycle): 1,
    (Vehicle.Car, Vehicle.Pedestrian): 0.8,
    (Vehicle.Car, Vehicle.Motorbike): 7,
    (Vehicle.Bicycle, Vehicle.Bicycle): 0.4,
    (Vehicle.Bicycle, Vehicle.Pedestrian): 0.3,
    (Vehicle.Bicycle, Vehicle.Motorbike): 2.8,
    (Vehicle.Pedestrian, Vehicle.Pedestrian): 0.1,
    (Vehicle.Pedestrian, Vehicle.Motorbike): 2.3,
    (Vehicle.Motorbike, Vehicle.Motorbike): 3,
}


class LandUse(Enum):
    a = "Residential"
    b = "Commercial"
    c = "Industrial"
    d = "Agricultural"
    e = "Transport"


probability_land_use = {LandUse.a: 0.41, LandUse.b: 0.17, LandUse.c: 0.06, LandUse.d: 0.28, LandUse.e: 0.08}
probability_pavement_given_land_use = {LandUse.a: 0.45, LandUse.b: 0.62, LandUse.c: 0.23, LandUse.d: 0.03, LandUse.e: 0.31}
land_use_lethality_multiplier = {LandUse.a: 1, LandUse.b: 0.94, LandUse.c: 1.06, LandUse.d: 0.98, LandUse.e: 1.10}


class City(Enum):
    a = "Nairobi"
    b = "Mombasa"
    c = "Kisumu"
    d = "Nakuru"
    e = "Eldoret"
    f = "Kehancha"
    g = "Ruiru"
    h = "Kikuyu"


probability_city = {City.a: 33, City.b: 12, City.c: 3, City.d: 3, City.e: 2.8, City.f: 2.7, City.h: 2.6}
probability_seat_belt_given_city = {City.a: 0.83, City.b: 0.76, City.c: 0.45, City.d: 0.56, City.e: 0.23, City.f: 0.51, City.h: 0.41}
city_lethality_multiplier = {City.a: 1.03, City.b: 1.02, City.c: 0.97, City.d: 0.98,
                             City.e: 0.99, City.f: 1.01, City.h: 1.00}


def time_lethality_multiplier(h):
    if 0 <= h < 2:
        return 1.9
    elif 2 <= h < 6:
        return 0.4
    elif 6 <= h < 10:
        return 1.2
    elif 10 <= h < 17:
        return 1
    elif 17 <= h < 19:
        return 0.2
    elif 19 <= h < 23:
        return 1
    elif 23 <= h < 24:
        return 1.9


def pavement_lethality_multiplier(pavement, vehicle1, vehicle2):
    if pavement:
        return 1
    if Vehicle.Car in (vehicle1, vehicle2) or Vehicle.Motorbike in (vehicle1, vehicle2):
        return 1.3
    else:
        return 1


def traffic_light_lethality_multiplier(traffic_light_distance, vehicle1, vehicle2):
    if traffic_light_distance < 5:
        if Vehicle.Motorbike in (vehicle1, vehicle2):
            return 1.7
        else:
            return 0.2
    elif 5 <= traffic_light_distance < 10:
        return 0.7
    elif 10 <= traffic_light_distance < 20:
        return 1
    else:
        return 1.3


def speed_limit_lethality_multiplier(speed):
    if speed == 20:
        return 0.2
    elif speed == 30:
        return 0.8
    elif speed == 40:
        return 1
    elif speed == 50:
        return 2.3
    elif speed == 60 or speed == 70:
        return 3.4
    else:
        return speed_limit_lethality_multiplier(int(speed*5/8))  # speed 'accidentally' in kph rather than mph


def speed_limit_injury_multiplier(speed):
    if speed == 20:
        return 0.8
    elif speed == 30:
        return 1
    elif speed == 40:
        return 1.1
    elif speed == 50:
        return 1.2
    elif speed == 60 or speed == 70:
        return 1.3
    else:
        return speed_limit_injury_multiplier(int(speed*5/8))  # speed 'accidentally' in kph rather than mph


def speed_lethality_multiplier(speed):
    return 0.5 + ((speed-15)*(speed-15)/1500)


def seat_belt_lethality_multiplier(seat_belt, vehicle1, vehicle2):
    if Vehicle.Car in (vehicle1, vehicle2):
        if seat_belt:
            return 0.8
        else:
            return 1.25
    else:
        return 1


def main(n, file):
    data = [column_names]
    for rowNumber in range(n):
        speed_limit = -1
        while not 20 <= speed_limit <= 70:
            speed_limit = int(random.normalvariate(4, 2)) * 10
        true_speed_limit = speed_limit
        if random.uniform(0, 1) < 20 / n:
            speed_limit = speed_limit * 8 / 5

        speed = -20
        while not -15 <= speed <= 15:
            speed = int(random.normalvariate(0, 8))
        speed += speed_limit

        vehicle1 = weighted_random_choice(probability_vehicle_given_speed_limit[true_speed_limit])

        vehicle2 = weighted_random_choice(probability_vehicle_given_speed_limit[true_speed_limit])

        land_use = weighted_random_choice(probability_land_use)

        city = weighted_random_choice(probability_city)

        hour = random.randint(0, 23) if random.randint(0, 2) == 0 else random.randint(8, 10) if random.randint(0, 2) == 0 else random.randint(17, 20)
        minute = random.randint(0, 59)
        time = format(hour, '02d')+":"+format(minute, '02d')

        month = random.randint(1, 12)
        day = random.randint(1, 28)
        date = format(day, '02d')+"/"+format(month, '02d')+"/18"

        pavement = 1 if random.uniform(0, 1) < probability_pavement_given_land_use[land_use] else 0

        distance_to_nearest_traffic_light = -1
        while distance_to_nearest_traffic_light < 0:
            distance_to_nearest_traffic_light = int(random.normalvariate(15, 10))+1

        seat_belt = "N/A" if Vehicle.Car not in (vehicle1, vehicle2) else \
            1 if random.uniform(0, 1) < probability_seat_belt_given_city[city] else 0

        vehicle_multiplier = vehicle_lethality_multiplier[(vehicle1, vehicle2)] if (vehicle1, vehicle2) in vehicle_lethality_multiplier \
            else vehicle_lethality_multiplier[(vehicle2, vehicle1)]
        lethal_prob = \
            vehicle_multiplier *\
            time_lethality_multiplier(hour) *\
            pavement_lethality_multiplier(pavement, vehicle1, vehicle2) *\
            traffic_light_lethality_multiplier(distance_to_nearest_traffic_light, vehicle1, vehicle2) *\
            speed_limit_lethality_multiplier(speed_limit) *\
            speed_lethality_multiplier(speed) *\
            seat_belt_lethality_multiplier(seat_belt, vehicle1, vehicle2) *\
            land_use_lethality_multiplier[land_use] *\
            city_lethality_multiplier[city] *\
            0.02
        lethal = 1 if random.uniform(0, 1) < lethal_prob else 0

        vehicle_multiplier = vehicle_injury_multiplier[(vehicle1, vehicle2)] if (vehicle1, vehicle2) in vehicle_injury_multiplier \
            else vehicle_injury_multiplier[(vehicle2, vehicle1)]
        injury_prob = \
            vehicle_multiplier *\
            time_lethality_multiplier(hour) *\
            pavement_lethality_multiplier(pavement, vehicle1, vehicle2) *\
            traffic_light_lethality_multiplier(distance_to_nearest_traffic_light, vehicle1, vehicle2) *\
            speed_limit_injury_multiplier(speed_limit) *\
            speed_lethality_multiplier(speed) *\
            seat_belt_lethality_multiplier(seat_belt, vehicle1, vehicle2) *\
            land_use_lethality_multiplier[land_use] *\
            city_lethality_multiplier[city] *\
            5
        injury = 1 if lethal or random.uniform(0, 1) < injury_prob else 0

        row = [
            vehicle1.value,
            vehicle2.value,
            date,
            time,
            pavement,
            distance_to_nearest_traffic_light,
            speed_limit,
            speed,
            seat_belt,
            injury,
            lethal,
            land_use.value,
            city.value
        ]
        row = [str(x) for x in row]
        data.append(row)

    print("dead ", sum(int(row[10]) for row in data[1:]))
    print("injured ", sum(int(row[9])-int(row[10]) for row in data[1:]))
    with open(file, "w", newline='') as my_csv:
        csv_writer = csv.writer(my_csv)
        csv_writer.writerows(data)


if __name__ == "__main__":
    main(10000, "data.csv")
