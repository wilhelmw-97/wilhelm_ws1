cmake_minimum_required(VERSION 2.8.3)
project(simple_robotino_messages)


find_package(catkin REQUIRED COMPONENTS
  std_msgs
  message_generation
)

 add_message_files(
DIRECTORY msg
   FILES
 RobotinoDistanceArray.msg
 )

add_service_files(
DIRECTORY srv
FILES SetField.srv
)

 generate_messages(
   DEPENDENCIES
   std_msgs
 )

## DEPENDS: system dependencies of this project that dependent projects also need
catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES simple_robotino_messages
  CATKIN_DEPENDS std_msgs message_runtime
#  DEPENDS system_lib
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

