/*
#include "ros/ros.h"
#include "rec/robotino/api2/all.h"

#include <string>
#include <iostream>
#include "nav_msgs/Odometry.h"
#include "geometry_msgs/Point.h"
#include "geometry_msgs/Twist.h"
#include "std_msgs/Int16.h"

using namespace rec::robotino::api2;


const int digitalInCount = 3;
const int digitalin[3] = {1, 2, 3};
const int analogInCount  = 3;
const int analogIn[3] = {1, 2, 3};


void digitalPinCallback(const std_msgs::Int16& msg)
{
    if(msg.data > 49999) // write: high at msg - 50000
    {
        
    }
    else // write: low
    {
        
    }
}

void analogPinCallback(const std_msgs::Int16& msg)
{
    // write 0-255 at msg % 100 (msg < 65536 -> 65 analog pins max)
}

void publishDigitalPins()
{
    
}
void publishAnalogPins()
{
    
}

class spD
{
public:
    void publishDigitalPins();
    void publishAnalogPins();
    sendPinDummy();
private:    
    
    
};

spd sendPinDummy();

*/