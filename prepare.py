import os
import subprocess
import shlex
import time
import requests
import json
try:
    import yaml
except (ImportError):
    print ("yaml module was not found. This module is required to read the params.yaml file for required parameters.")
    print ("Please install it using 'pip3 install --user pyyaml' or update your PYTHONPATH, and try again")
    print ("Aborting.")
    sys.exit()
import sys

def createMap (img_type,api_key, zoom, center_lat, center_lon, image_height, image_width):
    url = "https://dev.virtualearth.net/REST/v1/Imagery/Map/" + img_type + "/" + str(center_lat) + "," + str(center_lon) + "/" + str(zoom) + "?mapSize=" + str(image_height) + "," + str(image_width) + "&key=" + api_key
    final_img = requests.get(url)
    img = open (os.path.expanduser('~')+'/.ros/router/emptymap.jpg', 'wb+')
    img.write(final_img.content)
    img.close()
    img = open (os.path.expanduser('~')+'/.ros/router/emptymap.jpg', 'r')
    try:
        data = json.load(img)
        data.close()
    except(UnicodeDecodeError):
        os.chdir(os.path.expanduser('~')+'/.ros/router')
        subprocess.Popen(shlex.split("cp emptymap.jpg map.jpg"))
        return
    else:
        if (data['errorDetails'][0]) == "Access was denied. You may have entered your credentials incorrectly, or you might not have access to the requested resource or operation.":
            error = "Creation of map failed. You seem to have entered an incorrect/invalid API key. Please enter a valid API key and try again."
        else:
            error = "Creation of map failed. The map specified by the parameters in the params.yaml file does not exist. Please adjust those values and try again."
        print(error, 'Aborting.', sep='\n')
        sys.exit()

if __name__ == "__main__":
    print ("This script will prepare your PC for the map_display ROS package to run.")
    print ("This script will rewrite map.jpg, emptymap.jpg and gps.txt in ~/.ros/router, please back these up if you don't want to lose them.")
    print ("\nThese are the parameters that you have set for your map:-")

    paramsfile = open(sys.argv[0][:-10]+"../cfg/params.yaml")
    paramslist = yaml.load(paramsfile, Loader=yaml.FullLoader)
    
    zoom = paramslist['zoom']
    center_lat = (paramslist['center_coordinates'])['latitude']
    center_lon = (paramslist['center_coordinates'])['longitude']
    image_height = (paramslist['image_dimensions'])['image_height']
    image_width = (paramslist['image_dimensions'])['image_width']
    img_type = paramslist['type']

    print ("Zoom: ",zoom,sep='')
    print ("Map center GPS coordinates in latitude,longitude: ",center_lat,',',center_lon,sep='')
    print ("Image dimensions in pixels: ",image_height,'x',image_width,sep='')
    print ("Image type is: ",img_type,sep='')
    paramsfile.close()
    
    print ("Please abort and make changes to the params.yaml file in cfg folder if these aren't the desired parameters.")
    opt = input("\nDo you want to proceed? (y/N) ")
    if opt == 'Y' or opt == 'y':
        try:
            os.chdir(os.path.expanduser('~')+'/.ros')
        except:
            subprocess.Popen(shlex.split("mkdir -p " + os.path.expanduser("~") + "/.ros/router"))
            print ("Made .ros and router folder.")
        else:
            try:
                os.chdir(os.path.expanduser('~')+'/.ros/router')
            except:
                subprocess.Popen(shlex.split("mkdir " + os.path.expanduser("~") + "/.ros/router"))
                print ("Made router folder.")
        time.sleep(1)
        gpstxt = open(os.path.expanduser('~')+'/.ros/router/gps.txt','w+')            
        gpstxt.write('0\n')
        gpstxt.close()
        print ("Prepared the gps.txt file.")
        api = input("Please enter your Bing Maps REST API key for empty map generation: ")
        createMap(img_type,api,zoom,center_lat,center_lon,image_height,image_width)
        print ("Created an empty map.")
        print ("Great! Your are now ready to use the map_display package. Run this script again if you want to use a different starting map.")

    elif opt == '' or opt == 'N' or opt == 'n':
        print ("Operation cancelled. Aborting.")
    else:
        print ("Invalid option. Aborting.")