# Gripper Communication Package
This package allows for the communication between a host PC and a configured gripper. The aim of this package is to provide a generalised solution to communicate between different types of gripper varients with respect to input and output conditions based on user definition and the factory design method. The package has been tested in Windows (10/11) as well as Ubuntu 20.04

## Dependents
- [Python](https://www.python.org/downloads/) to be installed on your machine.
- [Docker](https://docs.docker.com/engine/install/) for a dockerised implementation (optional)

## Installation
The package can be installed locally (for manual usage) with the following instructions:
```bash
# Clone the package to a nominated directory (assumes home directory)
git clone https://github.com/REF-RAS/gripper-comms.git  

# Enter the package and install required packages
pip install -r gripper-comms/requirements.txt
```

The package can also be dockerised (for running in the background) with the following:
```bash
# Clone the package to a nominated directory (assumes home directory)
git clone https://github.com/REF-RAS/gripper-comms.git  

# LINUX: Run the docker compose command to build the image  
docker compose -f gripper-comms/docker/docker-compose.yaml build default 

# WINDOWS: Run the docker compose command to build the image  
docker compose -f gripper-comms/docker/docker-compose.yaml build default-windows
```

## Configuration and Usage
The design of the package is based on the following three (3) main abstract classes (located in [src/base](./src/base/)):
- ***The Client Object***: which handles communication to the client gripper of choice.  
- ***The Interpreter Object***: which handles translation/interpretation of input/output messages between a user interface and the client gripper. This is defined inside the [src/base/client.py](./src/base/client.py) module.
- ***The Interface Object***: which handles user communication to the gripper application from some means.

The intention with the above was to be as general as possible such that the main user entry point for the application ([gripper.py](./src/gripper.py)) remains unchanged. Users can contribute and add custom functionality based on the three classes above, which can be saved in [src/grippers](./src/grippers/) as a folder containing children classes of the defined parent abstract classes. 

As an example, this package includes a [robotiq](./src/grippers/robotiq/) extension built upon previous work (see the Acknowledgements section), which defines custom functionality to the three (3) main parent abstract classes. New implementations (or extentions) can be added in a similar way. 

Usage of the package, having designed an extension package for a gripper type, is handled via a [config](./config/gripper.yaml), which identifies the custom object types for creation via the factory method. Simply update these with updated extensions and run the package.

To run the package, simply run the following command(s) based on your preferred method of use: 
```bash
# If running locally in the package
python gripper-comms/src/gripper.py

# If running as a container (having already built as per the above)
# [LINUX/WINDOWS] Run the docker compose command to bring up the container (to run in the background)
# NOTE: the restart always flag is enabled by default so the container will start up on boot
docker compose -f gripper-comms/docker/docker-compose.yaml up default --detach

# If you wish to view the container logs when running headless - use the below command
docker logs docker-gripper-comms -f -n 100
```

## Contribution
Any new extensions are welcome; however, please ensure you have tested your updated extension prior to making a merge request. Simply fork this package, test your implementation, and, if happy to do so, open a new merge request to make available for others.

## Acknowledgements
This work is an extension of the work by [Wei Win Loy (Loy) and Baris Balci](https://github.com/DERT-research/RoboticArm-Software-EndEffectors/tree/main). Some elements of communication have been implemented based on original work by the following contributors with respect to configured grippers:
- [Robotiq](https://github.com/ros-industrial-attic/robotiq/tree/kinetic-devel/robotiq_2f_gripper_control)
