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

By default, the command above will install current master branch on your Raspberry,
which is actually in development mode.

If you want to install a production version (or any other version), you can get the commit SHA1 code
from Github, and append to the command.

For example, `912349ef198f8f95d9d75073da3ecf981a95c61c` is a commit for [`v1.1.0`](https://github.com/yuancheng2013/edupi/releases/tag/v1.1.0).
You can install it by running:

    $> fab deploy_edupi:host=pi@RASPBERRY_IP,commit=912349ef198f8f95d9d75073da3ecf981a95c61c


After that, you need to reboot your raspberry for the first time. EduPi will run automatically after boot.
You can then use your browser to test it:

    Normal user   : http://RASPBERRY_IP:8021/
    Administrator : http://RASPBERRY_IP:8021/custom/

There is a default super user account created with this deployment script:

    user: pi
    password: raspberry

This can be changed in the script `fabfile.py`.
