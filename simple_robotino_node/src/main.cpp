
#include "ros/ros.h"
#include "rec/robotino/api2/all.h"

#include <string>
#include <iostream>
#include "nav_msgs/Odometry.h"
#include "geometry_msgs/Point.h"
#include "geometry_msgs/Twist.h"
#include "std_msgs/Int16.h"
#include "/home/wilhelm/wilhelm_ws1/devel/include/simple_robotino_messages/RobotinoDistanceArray.h"

using namespace rec::robotino::api2;



void setSpeed(float vx, float vy, float vomgea);
void pubOdom();
void pubDists();
void cmdvelCb(const geometry_msgs::Twist& msg);
void spinOnce();

double vx_, vy_, vomega_;
Com com;
OmniDrive omniD;
ros::NodeHandle* node;
ros::Publisher odomPub, distPub;
ros::Subscriber velSub;
Odometry odomreader;
DistanceSensor distancesensors[8];

char strayCount = 30;


int main(int argc, char** argv) {
    
    std::string hostname = "192.168.0.101";
    std::cout << "Connecting to: "<< hostname.c_str() << std::endl;
	com.setAddress( hostname.c_str() );
    com.connectToServer(true);
    
    if( false == com.isConnected() )
	{
		std::cout << std::endl << "Could not connect to " << com.address() << std::endl;
		rec::robotino::api2::shutdown();
		exit( 1 );
	}
	else
	{
		std::cout << "success" << std::endl;
	}

    ros::init(argc,argv, "robotino_new_node"); 
    node = new ros::NodeHandle();
    ros::Rate rate(30);
    
    for(int i = 0; i < 8; i++){
        distancesensors[i].setSensorNumber(i);
    }
    
    odomPub = node->advertise<geometry_msgs::Point>("odom", 1, false);
    distPub = node->advertise<simple_robotino_messages::RobotinoDistanceArray>("distances", 1, false);
    velSub = node->subscribe("cmd_vel", 1, cmdvelCb);
    
    
    
    while(ros::ok()){
        spinOnce();
        rate.sleep();
        
    }
    rec::robotino::api2::shutdown();
    return 0;
}


void spinOnce(){
    

    pubOdom();
    pubDists();
    ros::spinOnce();
    omniD.setVelocity(vx_, vy_, vomega_);
    com.processEvents();
    
    strayCount--;
    if (strayCount == 0){
        strayCount = 20;
        vx_ = vx_/2;
        vy_ = vy_/2;
        vomega_ = vomega_/2;
    }
    
    
}



void pubOdom(){
    double odomx, odomy, odomphi;
    unsigned int odomseq;
    odomreader.readings(&odomx, &odomy, &odomphi, &odomseq);
    geometry_msgs::Point myodom;
    myodom.x = odomx;
    myodom.y = odomy;
    myodom.z = odomphi;
    odomPub.publish(myodom);
    
    
}

void cmdvelCb(const geometry_msgs::Twist& msg){
    vx_ = msg.linear.x;
    vy_ = msg.linear.y;
    vomega_ = msg.angular.z;
    strayCount = 30;
}

void pubDists(){
    simple_robotino_messages::RobotinoDistanceArray distancemsg;

    distancemsg.distance0 = distancesensors[0].distance();
    distancemsg.distance1 = distancesensors[1].distance();
    distancemsg.distance2 = distancesensors[2].distance();
    distancemsg.distance3 = distancesensors[3].distance();
    distancemsg.distance4 = distancesensors[4].distance();
    distancemsg.distance5 = distancesensors[5].distance();
    distancemsg.distance6 = distancesensors[6].distance();
    distancemsg.distance7 = distancesensors[7].distance();
    
    distPub.publish(distancemsg);

    

}