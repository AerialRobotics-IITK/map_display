import rospy
import numpy
import os
import requests
import cv2
from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse

def distance(lat1, lon1, lat2, lon2):
    earthradius = 6371

    dLat = math.radians(lat1 - lat2)
    dLon = math.radians(lon1 - lon2)

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return earthradius*c*1000

def bearing (lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    return math.atan2(math.sin(lon2 - lon1) * math.cos(lat2), math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(lon1 - lon2))



if __name__ == "__main__":
    rospy.init_node('image_update')
    rospy.wait_for_service('/update_image')
    image_service = rospy.ServiceProxy('/update_image', Trigger)
    # api_key = "your-api-key-goes-here"
    # url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/"
    center_lat = 26.519608 
    center_lon = 80.232266
    center_point = (1000,750)
    # pin_style = "50"
    # zoom = "19"
    # size = "2000,1500"
    f = open(os.path.expanduser('~') + '/.ros/router/gps.txt')
    text = f.read()
    list_words = text.split('\n')
    num_coords = (int)(list_words[0])
    f.close()
    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        final_url = url + center + "/" + zoom + "?mapSize="+size 
        f = open(os.path.expanduser('~') + '/.ros/router/gps.txt')
        text = f.read()
        f.close()
        list_words = text.split('\n')
        num = (int)(list_words[0])
        print("Hello")
        if (num != num_coords):
            num_coords = num
            for i in range (1,num_coords+1):
                map = cv2.imread (os.path.expanduser('~')+'/.ros/router/emptymap.jpg')
                lat,lon = list_words[i].split(' ')
                bearing_obj = bearing(center_lat, center_lon, obj_lat, obj_lon)
                distance_obj = distance(center_lat, center_lon, obj_lat, obj_lon)
                point_to_mark = (int(round(centre_point[0] + scaling_factor*distance_obj*math.cos(bearing_obj))),int(round(centre_point[1] + scaling_factor*distance_obj*math.sin(bearing_obj))))
                cv2.circle(map, point_to_mark, 5, (255,0,0))
                # final_url = final_url + "&pushpin=" + lat + "," + lon + ";" + pin_style + ";B" + str(i)
                
                # final_url = final_url + "&key=" + api_key
                # final_img = requests.get(final_url)
                # img = open (os.path.expanduser('~')+'/.ros/router/map.jpg', 'wb')
                # img.write(final_img.content)
                # img.close()
                trigger_req = TriggerRequest()
                result = image_service(trigger_req)
                print(result)
                print("")
            cv2.imwrite(os.path.expanduser('~')+'/.ros/router/map.jpg',map)
        rate.sleep()