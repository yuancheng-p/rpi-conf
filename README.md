# rpi-conf

This [fabric](http://www.fabfile.org/) script helps to configure and deploy web projects on a Raspberry Pi 2

## Usage

### Installation

We suppose that you have a clean [Raspbian](https://www.raspberrypi.org/downloads/) installed in your (micro-)SD card,
and you should have already expended the file system.

Also, your Raspberry pi should be in the same network as your local machine so that you can access it via SSH.
Then run this script on your own machine, so that it will deploy configuration files on your Raspberry.

Dependencies:


    $> pip install fabric

Clone the project on your local machine, go into the project directory and you are ready to go:


    $> git clone https://github.com/yuancheng2013/rpi-conf.git
    $> cd rpi-conf


### Configure hotspot


Run the following command, then reboot your Raspberry.
You should see a new Hotspot created with a name started with `FONDATION_ORANGE`,
followed by seven characters that identify your server.
Replace the `RASPBERRY_IP` with it's real IP in your sub network.

    $> fab config_hotspot:host=pi@RASPBERRY_IP

If you want to change this name, modify the `SSID_PREFIX` in `sysconf/etc/rc.local` and re-run the command above.

### Install some common packages


    $> fab install_common:host=pi@RASPBERRY_IP

### Deploy Edupi


    $> fab deploy_edupi:host=pi@RASPBERRY_IP


### TODO

    * Deploy Ka-lite
    * Deploy Kiwix
