#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <std_srvs/Trigger.h>

//Variable for storing image and home directory
cv::Mat img;
std::string home_dir;

class ImageConverter
{
  //Declaring essential ROS variables
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Publisher image_pub_;
  ros::ServiceServer server;

  public:
  //Callback function for image update service, which loads and updates the image in the node when called
  static bool imageupdateCallback(std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &resp){
    img = cv::imread(home_dir + "/.ros/router/map.jpg");
    resp.success = true;
    resp.message = "The image was succesfully read";
    return true;
  }  
  
  ImageConverter()
    : it_(nh_)
  {
    //Storing the address of the home directory as a string
    home_dir = std::string(getenv("HOME"));

    image_pub_ = it_.advertise("/image_converter/output_video", 1);
    server = nh_.advertiseService ("update_image",imageupdateCallback);
    ros::Rate LoopRate(5);
    
    //Try catch block to display exceptions in reading image
    try{
      img = cv::imread(home_dir + "/.ros/router/map.jpg");
    }

    catch (cv::Exception& e) {
      const char* err_msg = e.what();
      std::cout << "Problem in reading image: " << err_msg << std::endl;
      return;
    }

    while (ros::ok()){
      //Publishing image stream
      sensor_msgs::ImagePtr map_image = cv_bridge::CvImage(std_msgs::Header(), "bgr8", img).toImageMsg();
      image_pub_.publish(map_image);
      ros::spinOnce();
      LoopRate.sleep();
    }
  }
};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "image_converter");
  ImageConverter ic;
  return 0;
}