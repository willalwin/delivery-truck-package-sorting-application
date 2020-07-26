# William Alwin, StudentID #: 001100213
import csv
import datetime as Dt

# non-class variables and arrays used in program
hub = '4001 South 700 East'
packages = 0
package_data = []
distance_data = []
truck1 = []
truck2 = []


# Package class
class Package:
    total_mileage = 0

    # constructor
    def __init__(self, num, address, city, state, zip, deadline, weight, special_note=''):
        self.num = num
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note
        self.distance = 0.0
        self.package_status = "At warehouse hub"

    # getters
    def get_num(self): return self.num

    def get_address(self): return self.address

    def get_city(self): return self.city

    def get_state(self): return self.state

    def get_zip(self): return self.zip

    def get_deadline(self): return self.deadline

    def get_weight(self): return self.weight

    def get_special_note(self): return self.special_note

    def get_distance(self): return self.distance

    def get_package_status(self): return self.package_status

    # setters
    def set_num(self, num): self.num = num

    def set_address(self, address): self.address = address

    def set_city(self, city): self.city = city

    def set_state(self, state): self.state = state

    def set_zip(self, zip): self.zip = zip

    def set_deadline(self, deadline): self.deadline = deadline

    def set_weight(self, weight): self.weight = weight

    def set_special_note(self, special_note): self.special_note = special_note

    def set_distance(self, distance): self.distance = distance

    def set_package_status(self, package_status): self.package_status = package_status

    # print statement for packages
    def print(self):
        print("%2s) %-38s %-17s %-3s %-6s %-10s %-20s %s" % (self.num, self.address, self.city, self.state, self.zip,
                                                             self.deadline, self.package_status, self.special_note))

    # print mileage for packages
    def print_mileage(self):
        print("\nTotal mileage: %2.1f" % self.total_mileage)


# hash table class
class HashTable:
    # constructor
    def __init__(self, size):
        # initialize with empty list the size of package list
        self.hash_table = []
        for i in range(size):
            self.hash_table.append([])

    # insert into hash_table
    def insert(self, item):
        # find bucket for selected item
        bucket = item % len(self.hash_table)
        bucket_list = self.hash_table[bucket]
        # insert at end of bucket
        bucket_list.append(item)

    # search for item using key value, returns item if found or None if not
    def search(self, key):
        # get bucket list
        bucket = key % len(self.hash_table)
        bucket_list = self.hash_table[bucket]
        # search for key in bucket
        if key in bucket_list:
            # find items index and return item
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            return None


# calculates and returns distances from distance table using addresses sent from truck_sort function
# space-time complexity is O(n)
def get_distance(address1, address2):
    # for loops find matching addresses in row and column of distance data matrix
    for i in range(0, len(distance_data)):
        if address1 in distance_data[0][i]:
            break
    for j in range(0, len(distance_data)):
        if address2 in distance_data[j][0]:
            break
    # since matrix is not fully populated if row > column, [row][column] is returned
    if j > i:
        return distance_data[j][i]
    # else [column][row] returned
    else:
        return distance_data[i][j]


''' Package sorting algorithm, packages will be sorted based on minimum distance to previous package
    starting with distance from hub, the for loop terminates when the package list has been searched once,
    the lowest distance package is moved to index position then the function calls itself using index's
    address and advancing the index by one, when index == len(truck) get_distance is called one last time
    to get the distance back to hub.
    Space-time complexity is O(n*m)'''


def truck_sort(truck, current_stop, index):
    # local variables
    val1 = 0.0
    val2 = 0.0
    if index < len(truck):
        for i in range(index, len(truck)):
            if index == i:
                val1 = float(get_distance(current_stop, truck[i].get_address()))
            else:
                val2 = float(get_distance(current_stop, truck[i].get_address()))
                if val2 < val1:
                    val1 = val2
                    temp1 = truck[i]
                    truck[i] = truck[index]
                    truck[index] = temp1
        truck[index].set_distance(val1)
        truck_sort(truck, truck[index].get_address(), index + 1)
    else:
        val1 = float(get_distance(current_stop, hub))


# read csv files and store in package arrays
# space-time for both reads is O(n)
with open('.\data\WGUPS_Package_File.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader, None)
    for line in csv_reader:
        # update packages variable to use for hashing function
        packages += 1
        package_data.append(Package(line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]))
    # calling hash_insert on package_data array, space-time is O(n)
    # also created hash_table here so that the size could be adjusted to suit data size via packages variable
    hashed = HashTable(packages)
    for i in range(0, len(package_data)):
        hashed.insert(i)

with open('.\data\WGUPS_Distance_Table.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    index = 0
    for line in csv_reader:
        distance_data.append(line)

''' Delivery simulation function: runs through package delivery routine using manually sorted truck loads which
    were chosen based on general vicinity from map provided as well as special_note instructions. For this function
    a user specified time is provided as a stopping point and the function appends packages and calls truck_sort to
    sort packages before delivering them. Each packages distance is checked to make sure it will be delivered on or
    before specified time, and if so distance is added to individual truck distance as well as total mileage for day,
    and package status is updated including delivery time. If time is after 9:05 truck 2 is loaded, sorted and 
    delivered using same criteria. Finally if truck 2 trip 1 is delivered and returns to hub before time expires,
    truck 2 trip 2 is loaded and sent out, also there is a check during truck 2 trip 1 to see if package 9's address
    is updated and trip 2 doesn't depart until it has been
    Space-time is O(n*m) owing to the truck_sort function '''


def delivery_sim(time):
    # variables for tracking truck/trip mileage
    truck1_mileage = 0
    truck2_mileage = 0
    trip2_mileage = 0

    # check to see if specified time is after start time 8:00 in min
    if time >= 480:
        # loading truck1 trip manually in constant time O(1)
        truck1.append(package_data[hashed.search(0)])
        truck1.append(package_data[hashed.search(4)])
        truck1.append(package_data[hashed.search(12)])
        truck1.append(package_data[hashed.search(13)])
        truck1.append(package_data[hashed.search(14)])
        truck1.append(package_data[hashed.search(15)])
        truck1.append(package_data[hashed.search(18)])
        truck1.append(package_data[hashed.search(19)])
        truck1.append(package_data[hashed.search(20)])
        truck1.append(package_data[hashed.search(26)])
        truck1.append(package_data[hashed.search(28)])
        truck1.append(package_data[hashed.search(29)])
        truck1.append(package_data[hashed.search(33)])
        truck1.append(package_data[hashed.search(34)])
        truck1.append(package_data[hashed.search(36)])
        truck1.append(package_data[hashed.search(38)])
        # calling sorting algorithm for truck1 truck_sort runs in O(n*m)
        truck_sort(truck1, hub, 0)
        # updating package status, space-time is O(n)
        for i in range(0, len(truck1)):
            truck1[i].set_package_status("Out for delivery")
        # loop through sorted packages checking to see if their delivery time is before specified time
        # space-time is O(n + m)
        for i in range(0, len(truck1)):
            # if distance to next package will be delivered before input time update mileage and package status
            if (((truck1[i].get_distance() + truck1_mileage) * 60 / 18) + 480) <= time:
                truck1_mileage += truck1[i].get_distance()
                Package.total_mileage += truck1[i].get_distance()
                delivery_time = '{:02.0f}:{:02.0f}'.format(*divmod(((truck1_mileage * 60 / 18) + 480), 60))
                truck1[i].set_package_status("Delivered at %s" % delivery_time)
            # if truck travel time goes past input time break
            else:
                break
            # if last package in truck delivered calculate distance back to hub
            if i + 1 == len(truck1):
                # call get_distance() and assign value
                distance_to_hub = float(get_distance(truck1[i].get_address(), hub))
                # if travel time less than specified time add mileage to truck/total mileage
                if (((distance_to_hub + truck1_mileage) * 60 / 18) + 480) <= time:
                    truck1_mileage += distance_to_hub
                    Package.total_mileage += distance_to_hub
        # print truck trip data
        print("Truck 1 departed from hub at {:02.0f}:{:02.0f}".format(*divmod(480, 60)))
        # runs in O(n)
        for i in truck1:
            i.print()
        print("Truck 1 total mileage: %.1f" % truck1_mileage)
        # checks to see if anymore packages will be loaded and if not prints list of packages at warehouse
        # runs in O(n)
        if time < 545:
            for i in range(0, len(package_data)):
                if package_data[i].get_package_status() == "At warehouse hub":
                    package_data[i].print()
        else:
            # variable used to signal whether truck2 makes it back to the hub
            switch = 0
            package_count = 0
            # manually loading truck2 load 1
            truck2.append(package_data[hashed.search(3)])
            truck2.append(package_data[hashed.search(5)])
            truck2.append(package_data[hashed.search(10)])
            truck2.append(package_data[hashed.search(11)])
            truck2.append(package_data[hashed.search(16)])
            truck2.append(package_data[hashed.search(17)])
            truck2.append(package_data[hashed.search(21)])
            truck2.append(package_data[hashed.search(22)])
            truck2.append(package_data[hashed.search(23)])
            truck2.append(package_data[hashed.search(24)])
            truck2.append(package_data[hashed.search(25)])
            truck2.append(package_data[hashed.search(30)])
            truck2.append(package_data[hashed.search(31)])
            truck2.append(package_data[hashed.search(35)])
            truck2.append(package_data[hashed.search(39)])
            # calling sorting algorithm for truck2 truck_sort runs in O(n*m)
            truck_sort(truck2, hub, 0)
            # update package status, runs in O(n)
            for i in range(0, len(truck2)):
                truck2[i].set_package_status("Out for delivery")
            # loop through sorted packages checking to see if their delivery time is before specified time
            # space-time is O(n)
            for i in range(0, len(truck2)):
                # if distance to next package will be delivered before input time update mileage and package status
                if (((truck2[i].get_distance() + truck2_mileage) * 60 / 18) + 545) <= time:
                    package_count += 1
                    truck2_mileage += truck2[i].get_distance()
                    Package.total_mileage += truck2[i].get_distance()
                    delivery_time = '{:02.0f}:{:02.0f}'.format(*divmod(((truck2_mileage * 60 / 18) + 545), 60))
                    truck2[i].set_package_status("Delivered at %s" % delivery_time)
                else:
                    break
            # if end of truck load not reached print truck list as well as undelivered package list
            # Space-time is O(n*m)
            if package_count < len(truck2):
                # print truck2 list with timestamp
                print("Truck 2 departed from hub at {:02.0f}:{:02.0f}".format(*divmod(545, 60)))
                for i in truck2:
                    i.print()
                print("Truck 2 trip 1 total mileage: %.1f" % truck2_mileage)
                # if after 10:20 update package 9 address
                if time >= 620:
                    package_data[8].set_address('410 S State St')
                    package_data[8].set_zip('84111')
                # print package list of unloaded packages
                for i in range(0, len(package_data)):
                    if package_data[i].get_package_status() == "At warehouse hub":
                        package_data[i].print()
            # if all packages delivered find distance back to hub and if within time add to truck/total distance and
            # print truck list, else print truck list then print remaining packages at hub as well as check to see if
            # package 9 address is updated. Space-time is O(n*m)
            if package_count == len(truck2):
                # get distance back to hub
                distance_to_hub = float(get_distance(truck2[package_count - 1].get_address(), hub))
                # if distance can be driven within specified time add to totals
                if (((distance_to_hub + truck2_mileage) * 60 / 18) + 545) <= time:
                    truck2_mileage += distance_to_hub
                    Package.total_mileage += distance_to_hub
                    # set switch to 1 let truck2 trip2 know the truck will make it to hub in time
                    switch = 1
                    # print truck2 list
                    print("Truck 2 departed from hub at {:02.0f}:{:02.0f}".format(*divmod(545, 60)))
                    for i in truck2:
                        i.print()
                    print("Truck 2 trip 1 total mileage: %.1f" % truck2_mileage)
                # else print truck2 list as well as undelivered package list
                else:
                    print("Truck 2 departed from hub at {:02.0f}:{:02.0f}".format(*divmod(545, 60)))
                    for i in truck2:
                        i.print()
                    print("Truck 2 trip 1 total mileage: %.1f" % truck2_mileage)
                    if time >= 620:
                        package_data[8].set_address('410 S State St')
                        package_data[8].set_zip('84111')
                    for i in range(0, len(package_data)):
                        if package_data[i].get_package_status() == "At warehouse hub":
                            package_data[i].print()

            if switch == 1 and time >= 620:
                # counter variable
                trip2_count = 0
                # update package 9 info since time is after 10:20
                package_data[8].set_address('410 S State St')
                package_data[8].set_zip('84111')
                # clear and manually loading truck2 load 2
                truck2.clear()
                truck2.append(package_data[hashed.search(1)])
                truck2.append(package_data[hashed.search(2)])
                truck2.append(package_data[hashed.search(6)])
                truck2.append(package_data[hashed.search(7)])
                truck2.append(package_data[hashed.search(8)])
                truck2.append(package_data[hashed.search(9)])
                truck2.append(package_data[hashed.search(27)])
                truck2.append(package_data[hashed.search(32)])
                truck2.append(package_data[hashed.search(37)])
                # calling sorting algorithm for truck2 truck_sort runs in O(n*m)
                truck_sort(truck2, hub, 0)
                # update package status in O(n)
                for i in range(0, len(truck2)):
                    truck2[i].set_package_status("Out for delivery")
                # loop through sorted packages checking to see if their delivery time is before specified time
                # space-time is O(n)
                for i in range(0, len(truck2)):
                    if (((truck2[i].get_distance() + truck2_mileage + trip2_mileage) * 60 / 18) + 545) <= time:
                        trip2_count += 1
                        trip2_mileage += truck2[i].get_distance()
                        Package.total_mileage += truck2[i].get_distance()
                        delivery_time = '{:02.0f}:{:02.0f}'.format(
                            *divmod((((truck2_mileage + trip2_mileage) * 60 / 18) + 545), 60))
                        truck2[i].set_package_status("Delivered at %s" % delivery_time)
                    else:
                        break
                # if last packge delivered get distance back to hub and add to totals if time allows
                # Space-time is O(n)
                if trip2_count == len(truck2):
                    distance_to_hub = float(get_distance(truck2[trip2_count - 1].get_address(), hub))
                    if (((distance_to_hub + truck2_mileage + trip2_mileage) * 60 / 18) + 545) <= time:
                        trip2_mileage += distance_to_hub
                        Package.total_mileage += distance_to_hub
                print("Truck 2 trip 2 departed from hub at {:02.0f}:{:02.0f}".format(
                    *divmod(((truck2_mileage * 60 / 18) + 545), 60)))
                # final print statement for truck2 trip 2, runs in O(n)
                for i in truck2:
                    i.print()
                print("Truck 2 trip 2 total mileage: %.1f" % trip2_mileage)
    # print if specified time is before 8:00
    else:
        print("Time specified is before 8:00 AM start time.")


# output to screen for user prompt
print("----------------------------------------------------------")
print("                Package Delivery Simulator")
print("----------------------------------------------------------")
# a simple try catch that loops until a correct time is given
while True:
    try:
        t1 = input("Enter a time on a 24hr clock(must be formatted as- 00:00):")
        t1 = Dt.datetime.strptime(t1, '%H:%M')
        break
    except ValueError:
        print("You have entered an invalid time.")
# converts time given to minutes in O(1)
t2 = (t1.hour * 60) + (t1.minute)
# function call
delivery_sim(t2)
print("total miles in loop: %.02f" % Package.total_mileage)
