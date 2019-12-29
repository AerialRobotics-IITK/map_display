#!/usr/bin/env python

import rospy
import numpy
import os
import cv2
from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse
import math

# Function for calculating distance between two points having GPS coordinates lat1,lon1 and lat2,lon2 respectively
def distance(lat1, lon1, lat2, lon2):
    earthradius = 6371

    #Converting the difference in latitudes and longitudes to radians
    dLat = math.radians(lat1 - lat2)
    dLon = math.radians(lon1 - lon2)

    #Converting the latitudes to radians
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    #Formula for calculating angle between the radii of earth joining the two points
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    deltaTheta = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    #Return distance
    return earthradius*deltaTheta*1000

#Function for calculating bearing (clockwise angle from the North direction) of vector from point1(GPS coordinates lat1,lon1) to point2(GPS coordinates lat2,lon2)
def bearing (lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    return math.atan2(math.sin(lon2 - lon1) * math.cos(lat2), math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon1 - lon2))



if __name__ == "__main__":
    #ROS variables and initializations
    rospy.init_node('image_update')
    rospy.wait_for_service('/update_image')
    image_service = rospy.ServiceProxy('/update_image', Trigger)
    rate = rospy.Rate(10)

    #Essential Parameters:-
    #center_lat, center_lon := GPS coordinates of the point corresponding to the center pixel on the map
    #center_point := Pixel coordinates of the center point (width/2,height/2)
    #zoom := Zoom level of the bing maps being used
    #square_width := Width of the square to be used as a marker
    #square_color := Color of the square to be used as a marker
    center_lat = rospy.get_param("/center_coordinates/latitude")
    center_lon = rospy.get_param("/center_coordinates/longitude")
    center_point = (rospy.get_param("/image_dimensions/image_height")/2,rospy.get_param("/image_dimensions/image_width")/2)
    zoom = rospy.get_param("/zoom")
    square_width = rospy.get_param("/square_properties/square_width")
    square_color = rospy.get_param("/square_properties/square_color")
    
    #num_coords stores the number of coordinate points currently in the gps.txt file
    num_coords = 0

    #scaling_factor calculates the pixels/meter ratio of the given map
    scaling_factor = (2**zoom)/(156543.04 * math.cos(math.radians(center_lat)))
    
    while not rospy.is_shutdown():
        #This block reads the gps.txt and stores each line in a list called list_words
        f = open(os.path.expanduser('~') + '/.ros/router/gps.txt')
        text = f.read()
        f.close()
        list_words = text.split('\n')

        #If the number of coordinates (stored in num) is different than the previous number of coordinates
        #(stored in num_coords) change num_coords to num, write the new image and call service to update 
        #image
        num = (int)(list_words[0])
        if (num != num_coords):
            num_coords = num
            map = cv2.imread (os.path.expanduser('~')+'/.ros/router/emptymap.jpg')

            for i in range (1,num_coords+1):
                #get latitude and longitude of each point, calculate bearing and distance of that point from the center, and pixel coordinates of the point
                #to be marked on the image                
                lat,lon = list_words[i].split(' ')
                bearing_obj = bearing(center_lat, center_lon, float(lat), float(lon))
                distance_obj = distance(center_lat, center_lon, float(lat), float(lon))
                point_to_mark = (int(round(center_point[0] + scaling_factor*distance_obj*math.sin(bearing_obj))),int(round(center_point[1] - scaling_factor*distance_obj*math.cos(bearing_obj))))
                
                #Print point to be marked and draw a rectangle around it
                print (point_to_mark)
                cv2.rectangle(map, (point_to_mark[0] - square_width/2,point_to_mark[1] - square_width/2),(point_to_mark[0] + square_width/2,point_to_mark[1] + square_width/2), (square_color['b'],square_color['g'],square_color['r']), -1)

            #Write the image, call the service, and print the result     
            cv2.imwrite(os.path.expanduser('~')+'/.ros/router/map.jpg',map)
            trigger_req = TriggerRequest()
            result = image_service(trigger_req)
            print(result)
            print("")
        rate.sleep()