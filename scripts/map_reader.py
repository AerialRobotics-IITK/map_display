import rospy
import numpy
import os
import requests
import cv2
from std_srvs.srv import Trigger, TriggerRequest, TriggerResponse

if __name__ == "__main__":
  rospy.init_node('image_update')
  rospy.wait_for_service('/update_image')
  image_service = rospy.ServiceProxy('/update_image', Trigger)
  api_key = "your-api-key-goes-here"
  url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial/"
  center = "26.519608,80.232266"
  pin_style = "50"
  zoom = "19"
  size = "2000,1500"
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
        lat,lon = list_words[i].split(' ')
        final_url = final_url + "&pushpin=" + lat + "," + lon + ";" + pin_style + ";B" + str(i)
       
      final_url = final_url + "&key=" + api_key
      final_img = requests.get(final_url)
      img = open (os.path.expanduser('~')+'/.ros/router/map.jpg', 'wb')
      img.write(final_img.content)
      img.close()
      trigger_req = TriggerRequest()
      result = image_service(trigger_req)
      print(result)
      print("")
    rate.sleep()

