# PFA-Reachy-mini

## Table of content

- [Description](#description)
- [Report](#report)
- [Before using the robot](#installation)
    - [Installing the requirements](#installing-the-requirements)
    - [Realoading the servers](#reloading-the-servers)
    - [Initiating the camera](#initiating-the-camera)
    - [Showing last image](#showing-last-image)
    - [Deleting pictures](#deleting-pictures)
- [Using the robot](#using-the-robot)
- [Testing the project without the robot](#testing-the-project-without-the-robot)
- [Cleaning the repository](#cleaning-the-repository)
- [Dealing with the crashes](#dealing-with-the-crashes)


## Description

This project is a 2nd year engeneering school project for a group of 7 students.
The purpose is to create a vocal assistant which can also take pictures in response to the commands that can be made by voice or codes.

## Report

You can find the report about the project in the folder **report**.

## Before using the robot

### Installing the requirements

To install all the packages used in this project, please use the command :

```bash
$ make install
```
or  
```bash
$ pip install -r ./requirements.txt
```  

+ *Note : Each time you reload the server, you have to reinitiate the camera.*

### Reloading the servers

Sometimes, you can have some errors of adress or camera. They are due to the robot servers that need to be reloaded. You can use this command to do it :

```bash
$ make reload-server
```

### Initiating the camera

The camera of reachy must be initiating to make the focus.  
In order to do so, you can use the command :  

```bash
$ make initiate-camera
```

And then you have to clic on `q` key when the focus is good.  
+ *Note : Try not to be in a room with too much light to do it.*  

### Showing last image

A python script allows you to display the last image.
You have to **open a new shell** and use the command :

```bash
$ make show-last-picture
```

Then you go back on the principal shell and you can launch the robot.

### Deleting pictures

A python script allows you to delete the oldest images. In fact, you cannot save all the pictures because of the storage of the robot. So you can use this script which will automatically delete the oldest pictures when the storage is full. This command allows you to chose how many pictures **P** you want to delete when **N** pictures have been stored.
You have to **open a new shell** and use the command :

```bash
$ make delete-pictures NB_PHOTOS=<N> NB_TO_DELETE=<P>
```

## Using the robot

You can use the reachy robot in many version (with aruco detection, without, ...). Here are the commands to launch the diferent versions of reachy :

```bash
$ make reachy-final
```

```bash
$ make reachy-only-aruco
```

## Testing the project without the robot

You can test the project without having the robot. For this, we use a fake reachy that only print what he does without doing it concerning the movements. Here are the command to use to launch the diferent versions :

```bash
$ make fake-reachy-final
```

```bash
$ make fake-reachy-only-aruco
```

## Cleaning the repository

You can delete all the pitcures and so the tmp directory using the command :

```bash
$ make clean-all
```

Or you can delete only the imported image of reachy that has been imported to create the tmp directory at the begining :

```bash
$ make clean
```

## Dealing with the crashes

Sometimes, the robot can crash and his motors and not switch-off. If you want to use it again, you can launch any command above. But if you want to switch-off his motors you can use this commands in a python3 temrinal:

```py
> from reachy_sdk import ReachySDK
> reachy = ReachySDK(host='localhost')
> reachy.turn_off('head')
```

## Authors

- [MARAIS Lucas](<Lucas.Marais@enseirb-matmeca.fr>)
- [RAIS Sylvain](<Sylvain.Rais@enseirb-matmeca.fr>)
- [DIEUDONNE Clara](<Clara.Dieudonne@enseirb-matmeca.fr>)
- [ELFANI Hamza](<Hamza.Elfani@enseirb-matmeca.fr>)
- [BOUDEAU Benjamin](<Benjamin.Boudeau@enseirb-matmeca.fr>)
- [LAMHAMDI Aymane](<Aymane.Lamhamdi@enseirb-matmeca.fr>)
- [ZIZOUAN Widad](<Widad.Zizouan@enseirb-matmeca.fr>)