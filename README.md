# delivery-truck-package-sorting-application

This project was designed to simulate a package delivery sorting system where certain packages had special instructions that needed to be heeded, the special instructions are listed in the Package_File.csv. The goal of the project was to follow all instructions and deliver packages in the least distance travelled, with a max of 150 miles total. The user interface is a command line that askes the user to input a time and then prints a list of all packages with delivery info for each as well as miles travelled.

Assumptions:
•  Each truck can carry a maximum of 16 packages.

•  Trucks travel at an average speed of 18 miles per hour.

•  Trucks have a “infinite amount of gas” with no need to stop.

•  Each driver stays with the same truck as long as that truck is in service.

•  Drivers leave the hub at 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed. 
The day ends when all 40 packages have been delivered.

•  Delivery time is instantaneous, i.e., no time passes while at a delivery 
(that time is factored into the average speed of the trucks).

•  There is up to one special note for each package.

•  The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m. The correct 
address is 410 S State St., Salt Lake City, UT 84111.

•  The package ID is unique; there are no collisions.

•  No further assumptions exist or are allowed.

Language: Python

Usage: download zip file and run in your favorite IDE
