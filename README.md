# suricata-lightweight-gui
Because my RaspberryPi just couldn't handle anything more
## Description
This is a simple Web UI for Suricata running on Python Flask and VueJS. It binds on the eve.json file and allows to display/sort/filter the events. There are many better Suricata Web UI out there, however they are too heavy for my RaspberryPi 2B. 
## Install
```bash
git clone https://github.com/daxAKAhackerman/suricata-lightweight-gui.git
cd suricata-lightweight-gui
docker-compose up -d
```
## Pictures
![Alt text](/pictures/dashboard.png?raw=true "Dashboard")
![Alt text](/pictures/filters.png?raw=true "Filters")
![Alt text](/pictures/details.png?raw=true "Details")