#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <stdlib.h>
#include <signal.h>
using namespace rec::robotino::api2;


MyCom com;
OmniDrive omniDrive;


void init( const std::string& hostname )
{
	// Initialize the actors

	// Connect
	std::cout << "Connecting...";
	com.setAddress( hostname.c_str() );

	com.connectToServer( true );

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
}