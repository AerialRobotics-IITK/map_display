# map_display
This is a ROS package written in C++ and python that is used for publishing a dynamically marked map on image stream. 

### Working
There are two nodes (both are launched by the included launch file) image_update and image_converter. The work of the image_update node is to constantly keep checking the file ~/.ros/router/gps.txt. If a change in the number of coordinates is detected (given on the first line in gps.txt), it marks the new coordinate(s) and updates the image map.jpg locally on the machine, located in ~/.ros/router. After doing this it calls a service update_image. This service is advertised by the image_converter node. The job of the image_converter node is to keep displaying the map image on the topic /image_converter/output_video. When the service it called, it replaces the image it was publishing with the new map.jpg written by the image_update node, and starts publishing that instead.

The marked image consists of squares of green color, of width 30 pixels, at positions of the GPS coordinates.
