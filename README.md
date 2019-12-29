# map_display
This is a ROS package written in C++ and python that is used for publishing a dynamically marked map on image stream. 

### Working
There are two nodes (both are launched by the included launch file) image_update and image_converter. The work of the image_update node is to constantly keep checking the file ~/.ros/router/gps.txt. If a change in the number of coordinates is detected (given on the first line in gps.txt), it marks the new coordinate(s) and updates the image map.jpg locally on the machine, located in ~/.ros/router. After doing this it calls a service update_image. This service is advertised by the image_converter node. The job of the image_converter node is to keep displaying the map image on the topic /image_converter/output_video. When the service it called, it replaces the image it was publishing with the new map.jpg written by the image_update node, and starts publishing that instead.

The marked image consists of squares of green color, of width 30 pixels, at positions of the GPS coordinates.


### Parameters
There are certain parameters which are required by the node to display the map properly. These are:-
* Center Coordinates := The GPS coordinates of the center of the map to be displayed 
* Zoom := Zoom level of the map
* Image Dimensions := The height and width of the image in pixels
* Square Properties := Properties (such as width and color) of the square marker being used
* Type := Type of image being used. The acceptable types are - 
    * Aerial
    * AerialWithLabels
    * AerialWithLabelsOnDemand
    * Streetside
    * BirdsEye
    * BirdsEyeWithLabels
    * Road
    * CanvasDark
    * CanvasLight
    * CanvasGray
    
    Please refer to the Bing maps REST API site [here](https://docs.microsoft.com/en-us/bingmaps/rest-services/imagery/get-a-static-map) for detailed info

Please set these parameters in the params.yaml file. However do note that all settings might not work. Generally a zoom level above 19 and image dimensions above 2000x1500 doesn't work.

### Usage
Before running this node for the first time, please run the prepare.py python script using python3. This script requires the use of pyyaml, which can be installed by the command "pip3 install --user pyyaml". This script should be run everytime you change the parameters Center Coordinates, Zoom and/or Image Dimensions.
After building the package and sourcing your workspace, you should be able to run the nodes by "roslaunch map_display map_disp.launch"
