#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <std_srvs/Trigger.h>

  cv::Mat img;
  std::string home_dir;

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Publisher image_pub_;


public:
  static bool imageupdateCallback(std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &resp){
    img = cv::imread(home_dir + "/.ros/router/map.jpg");
    resp.success = true;
    resp.message = "The image was succesfully read";
    return true;
  }  
  
  ImageConverter()
    : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    home_dir = std::string(getenv("HOME"));
    std::cout << home_dir;
    image_pub_ = it_.advertise("/image_converter/output_video", 1);
    int num_images = 0;
    ros::Rate LoopRate(5);
    img = cv::imread(home_dir + "/.ros/router/map.jpg");
    if (img.empty()) {
      std::cout << "cant read image " << home_dir;

      return;
    }

    img = cv::imread(home_dir + "/.ros/router/map.jpg");
    ros::ServiceServer server = nh_.advertiseService ("update_image",imageupdateCallback);

    while (ros::ok()){
      // cv_bridge::CvImagePtr cv_ptr;
      //cv_ptr->image = cv::imread(home_dir + "/.ros/router/map.jpg");
      // sensor_msgs::ImagePtr map_image = cv_bridge::CvImage(std_msgs::Header(), "bgr8", undistImg_).toImageMsg()
      char home_dir_cpy[50];
      strcpy(home_dir_cpy,getenv("HOME"));
      sensor_msgs::ImagePtr map_image = cv_bridge::CvImage(std_msgs::Header(), "bgr8", img).toImageMsg();
      // std::cout << home_dir_cpy << std::endl;
      FILE* fp = fopen(strcat(home_dir_cpy,"/.ros/router/gps.txt"), "r");
      int num = fgetc(fp) - 48;
      fclose(fp);
      image_pub_.publish(map_image);

      // free(home_dir_cpy);
      ros::spinOnce();
      LoopRate.sleep();

    }
  }



};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "image_converter");
  ImageConverter ic;
//   ros::spin();
  return 0;
}