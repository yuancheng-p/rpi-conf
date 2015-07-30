# Images hierarchy

          raspbian.img
            |
          basepi.img (8GB)
            |
        integrated-base.img (8 GB)
         ___|________
        |           |
    frbase.img    enbase.img  (128GB)
        |           |
     country-specified-images (128GB Production) ...


* `raspbian.img` is a clean raspbian image.
* `basepi.img` adds Hotspot and some standard Linux packages.
* `integrated-base.img` has Web applications installed, but no data added.
* `frbase.img` adds standard French content, `enbase.img` adds standard English content (i.e. wikipedia).
* `country-specified-images` have specific content in EduPi for different countries.


Note: we use 8GB SD card to create `basepi.img` and `integrated-base.img`, which can avoid the long process of copying
image file.


================== I. Base Images ================== 

# 2015-06-08-basepi.img

This image is based on raspbian-2015-05-05

You can download the latest raspbian on https://www.raspberrypi.org/downloads/


## Additionally installed packages

### Hotspot

    * hostapd
    * dnsmasq
    
    config_files = [
        '/etc/network/interfaces',
        '/etc/dnsmasq.conf',
        '/etc/resolvconf.conf',
        '/etc/hostapd/hostapd.conf.orig',
        '/etc/rc.local',
    ]

### Web server

    * nginx

### Python

    * python3-pip
    * python3.4
    * virtualenv

### js

    * nodejs
    * npm
    * bower

### others

    * libmagickwand-dev
    * upstart

**TEST**

1. Plug the Raspberry, it should create a hotspot.
2. Connect to the hotspot with a device, open a page in browser, you should see `Welcome to Nginx` message.


------------------------------------------------


# 2015-06-18-integrated-base.img

The objective of this image is to download all pre-installed web projects,
so that we only need to copy content files and adapt languages later on.


## Index page

Use rpi-conf to deploy an index page (with Nginx config)
Deployed index page, and it's Nginx configuration, but only EduPi and KaLite can be used.
Use `rpi-conf` to do this:

    $> fab deploy_index_page:host=pi@RASPBERRY_IP

In fact there is no content in KaLite at this point.
Edit and adapt this index page when needed. It's no more than simple HTML code.

The index page is under `/home/pi/sites/www/`
Link the Nginx's default `www` (`/usr/shared/www/`) folder to this index page folder.


## kiwix

Created site folders and downloaded kiwix server, but no content is added.
The server is not yet configured to run at boot.

kiwix folder: `/home/pi/sites/kiwix/`

! *TODO: need a bash script for running kiwix automatically*


## ka-lite

* Installed
* Run at boot
* Assessment added
* Downloaded FR local, and set French as default

*No video added*

ka-lite folder: `/home/pi/sites/kalite/`

## EduPi

* Installed a stable version via rpi-conf:


    $>  fab deploy_edupi:host=pi@RASPBERRY_IP,commit=RELEASE_COMMIT


* With no data, only a default admin account is created.
* Run at boot.


**TEST**

0. Ensure that `basepi` test suit pass.
1. Connect a device to the Raspberry's hotspot.
Open a page on the browser,  you should be redirected to a Orange Fondation index page.
(index page installed, Nginx configured)
2. Click `KaLite` to go into Ka-lite. (ka-lite auto-start, this takes ~4 minutes)
3. Click `EduPi` to go into EduPi, also make sure that we have access to custom page. (EduPi auto-start)

The hotspot is created after KaLite is started, just be patient... **TODO: what is the best solution this?**

Test the above multiple times, ensure it works.

### For Update

If this image is updated, all images inherit this one should do the same update. (A lot of work if we want latest software versions)
For example, update EduPi (only the software version).
Take notes for each update of this image !


=========================== II. BEFORE PRODUCTION ===========================

# HOW TO PREPARE CONTENT (for deployment, by developer)

With an integrated-base image, it's much simpler to create a customized image.
There is no more than copy content files into the right place.

1. Prepare image
    * Install `*-integrated-base.img` (8 GB)
    * Expand Filesystem (to all -> 128 GB) [http://elinux.org/RPi_Resize_Flash_Partitions]

It's preferred to resize the partition directly in raspberry.


2. Index Page
    * Adapt its index page (HTML code) if needed.

3. kiwix content
    * Copy kiwix data: wikipedia (with it's index file), wiktionary, gutenberg, 
    * Copy / generate kiwix library
    * Run kiwix at boot. Append in `rc.local`: // *TODO: remove this step if we have a bash script

        ```
        # run kiwix
        sudo /home/pi/sites/kiwix/bin/kiwix-serve --port=4201 --library /home/pi/sites/kiwix/data/library/all.zim.xml --daemon
        ```

4. KaLite content
    * Copy all KaLite content to the proper folder

**TEST**

0. Ensure that integrated-base tests works.
1. Click all kiwix service to ensure that works.
2. KA-lite videos should work.


------------------------------------------------

# 2015-06-18-frbase.img

## kiwix

* Add wikipedia, wiktionaire, gutenberg.
* Add library for all projects.
* Run kiwix at boot.

## ka-lite

* Copied All French version videos


**TEST**

Run all tests mentioned above.


------------------------------------------------

# EnglishBase.img

*TODO*

## kiwix

* Add wikipedia, wiktionary.
* Generate / add library for all projects. (use `kiwix-manage`)
* Run kiwix at boot.


## ka-lite

* Go to admin page, set English as default language.
* Download English version videos.

**TEST**

Run all test suites mentioned above.


=========================== III. PRODUCTION ===========================

**TODO**

# French based

* France (default)
* Madagascar
* Senegal
* Niger
* Cameroon
* Tunisia


# English based

* Cameroon-EN


=========================== IV. EduPi Data Migration ===========================

**TODO**

For all sd-cards in production, KaLite, Kiwix will not change.
Only EduPi data can be changed.

With EduPi, we can:

  * Add/delete/modify the data directly via EduPi admin page.
  * Export data from EduPi
  * Import data to EduPi

Therefore, it's very easy to customize data for different countries.
There is no need to create an image for each country.

Just use French / English image, then import different EduPi data for for different use.

For the moment, EduPi does not support Export/Import data with its' admin interface.
However, since EduPi uses Sqlite, we only need to copy/paste the database file and media files.
