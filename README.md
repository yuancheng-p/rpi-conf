# rpi-conf

This fabfile script helps to configure and deploy web projects on a Raspberry Pi 2

## usage

We suppose that you have a clean [Raspbian](https://www.raspberrypi.org/downloads/) installed in your (micro-)SD card,
and you should have already expended the file system.

Dependencies:


    $> sudo pip install fabric

Clone the project on your local machine, and go into the project directory to run magic scripts:


    $> git clone https://github.com/yuancheng2013/rpi-conf.git
    $> cd rpi-conf


Also, your Raspberry pi should be in the same network as your local machine so that you can access it via SSH


### Configure hotspot

Run the folowing command, then reboot your Raspberry.
You should see a new Hotspot created with a name started with `FONDATION_ORANGE`

    $> fab config_hotspot:host=pi@RASPBERRY_IP


### Install some common packages


    $> fab install_common:host=pi@RASPBERRY_IP

### Deploy Edupi


    $> fab deploy_edupi:host=pi@RASPBERRY_IP


### TODO

    * Deploy Ka-lite
    * Deploy Kiwix
