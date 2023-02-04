# import numpy as np
import matplotlib.pyplot as plt
import re
import datetime

data = open("data.txt")

# remove newlines and lines starting with "#"

cleaned_data = []
for line in data:
    # remove empty lines and comments
    if not (line == "\n" or line[0] == "#"):
        # remove newline char and store
        if line[-1:] == "\n":
            cleaned_data.append(line[:-1])
        else:
            cleaned_data.append(line)

class Ride():
    def __init__(self, rideStr):
        terms = rideStr.split(",")
        self.distance = float(terms[0].split(" ")[0])
        self.duration = terms[1].split(" ")[1]
        self.time = terms[2].split(" ")[1] + " " + terms[2].split(" ")[2]
        self.maxTemp = terms[3].split(" ")[1]
    
    def __str__(self):
        return "Ride at " + str(self.time) + " for " + str(self.distance) + "km, which took " + str(self.duration) + " while the max temp reached " + str(self.maxTemp) + "C."

# store rides in dict
# key is date, value is array of rides
rides = {}

current_date = None
ride = []
for ind, line in enumerate(cleaned_data):
    # is the line a date?
    if re.search("[0-9][0-9] [0-9][0-9] 202[0-9]", line):
        # add prev date and rides to dict
        if ride != []:
            rides[current_date] = ride
        
        # set the current date to new day, empty ride list
        terms = line.split(" ")
        year = int(terms[2])
        month = int(terms[1])
        day = int(terms[0])
        current_date = datetime.date(year, month, day)
        ride = []
    else:
        ride.append(Ride(line))
    
    # catch the final ride
    if ind == len(cleaned_data) - 1 and ride != []:
        rides[current_date] = ride

date = [datetime.date(2023, 1, 1)]
dayDist = [0]

for day, rideList in rides.items():
    date.append(day)
    totalDist = 0
    for ride in rideList:
        totalDist += ride.distance
    dayDist.append(totalDist)

print(date, dayDist)

cumulativeDist = []
total = 0
for day in dayDist:
    cumulativeDist.append(total + day)
    total += day
print(cumulativeDist)

goalFromJan1Dists = [0, 3650]
goalFromJan1Dates = [datetime.date(2023, 1, 1), datetime.date(2023, 12, 31)]

goalFromJan31Dates = [datetime.date(2023, 1, 31), datetime.date(2023, 12, 31)]

fig, ax = plt.subplots()
ax.plot(date, cumulativeDist, "blue", marker="o")
ax.plot(goalFromJan1Dates, goalFromJan1Dists, "red")
ax.plot(goalFromJan31Dates, goalFromJan1Dists, "green")
ax.grid()
ax.set_xbound(datetime.date(2023, 1, 30), datetime.date(2023, 2, 6))
ax.set_ybound(0, 400)
ax.legend(["Ride Subtotal", "3650km challenge", "3650km challenge late"])
plt.show()