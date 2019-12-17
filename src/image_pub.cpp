#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Publisher image_pub_;

public:
  ImageConverter()
    : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    image_pub_ = it_.advertise("/image_converter/output_video", 1);
    int num_images = 0;
    ros::Rate LoopRate(5);
    while (ros::ok()){
      cv_bridge::CvImagePtr cv_ptr;
      cv_ptr->image = cv::imread(strcat(getenv("HOME"),"/.ros/router/map.jpg"));

      // char* gps_path = strcat(getenv("HOME"),"/.ros/router/gps.txt")
      FILE* fp = fopen(strcat(getenv("HOME"),"/.ros/router/gps.txt"), "r");
      int num = fgetc(fp) - 48;
      fclose(fp);
      if (num_images != num){
        num_images = num;
        cv_ptr->image = cv::imread(strcat(getenv("HOME"),"/.ros/router/map.jpg"));
      }

      image_pub_.publish(cv_ptr->toImageMsg());
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