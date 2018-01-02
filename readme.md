# Something Awesome PI and Sensor

Our housing area has a common integrated heating with recuperator in each house. These have an issue now after ten years that they start to leak. To help the other owners I created this detector tool.

## Getting Started

You need a Raspberry PI3 and an E-Mail Address to setup your own detector

### Prerequisites

Install NOOBS on your Raspberry and check out this Repo onto your device. 

https://www.raspberrypi.org/help/noobs-setup/2/

Change to your folder where you checked out this repo and run the following command. 

```
sh watersensor.py
```

This will fail as you need to setup a config.py with the secret of your IFTTT.com service and the need to define the house where the PI will be installed. The watersensor.py expects the config in the same folder.

```
secret = '{{your IFTTT key}}'
sensor = 'uniqueID'
```

### Installing

After setting up the above make sure that your script is running automated. You can do so, by adding your /home/pi/.config/autostart/ folder and adding the script path that needs to start automated there.

autostart.desktop contents:

```
[Desktop Entry]
Exec=lxterminal -e '/bin/sh' -c ' sudo /home/pi/watersensor/watersensor.py ; exec /bin/sh'
Type=Applcation
```

This will run the script on startup - with below you can execute it also alone. 

```
sh watersensor.py
```

## Authors

* **Holger hellinger** - *Initial work* - [POlent](https://github.com/polent)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to Marco for the inspiration ;) 

