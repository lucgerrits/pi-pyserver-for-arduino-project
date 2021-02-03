# pi-pyserver-for-arduino-project

A Python web server aims to receive and display Arduino messages.

**Note**: All POST request to the API need to be formated (examples bellow) AND the http content type requires to be "binary".

## 1) Send messages
A message is a **fixed length binary** that follows this rule:
```text
[_____id_____][_____angle_____][_____distance_____]

|____parameter___|____Bytes____|_____example____|_________usage note___________|
| id             | 6 bytes     |  luc123        |  use ascii char [a-Z0-9]     |
| angle          | 6 bytes     |  110.10        |  min=000.00 ; max=360.00     |
| distance       | 6 bytes     |  000.50        |  min=000.00 ; max=999.99     |

************************** BASIC EXAMPLE   ************************************
To send the following:
id=luc123
angle=110.10
distance=000.50

You'll have to send an API request to POST an HTTP request to: 
http://192.168.1.10:8080
With data equal to:
"luc123110.10000.50"
```

Graphical representation:

 ```text                                             __________________
                                              |  Raspberry Pi  |
                                              |                |
 _________     http://192.168.1.10:8080/api   |                |
|         |     POST: "luc123110.10000.50"    |                |
| Arduino |  -------------------------------> |      API       |
|         |  <------------------------------- |                |
| sensors |              200 / OK             |       |        |
|  data   |                                   |       |        |
|_________|                                   |       |        |
 _________     http://192.168.1.10:8080/      |       ↓        |
|         |                GET                |                |
| Browser |  -------------------------------> |     Website    |
|         |  <------------------------------- |                |
|  List   |              200 / OK             |                |
|  data   |                                   |                |
|  ----   |                                   |                |
|  ----   |                                   |                |
|  ----   |                                   |________________|
|_________|

```

## 2) Send messages with images

A message is a **fixed length binary** (variable length **only** for image)that follows this rule:

```text
************************** IMAGE EXAMPLE   ************************************

[_____id_____][_____angle_____][_____distance_____][_____image_____]

|____parameter___|____Bytes____|_____example____|_________usage note___________|
| id             | 6 bytes     |  luc123        |  use ascii char [a-Z0-9]     |
| angle          | 6 bytes     |  110.10        |  min=000.00 ; max=360.00     |
| distance       | 6 bytes     |  000.50        |  min=000.00 ; max=999.99     |
| image          | 0-oo bytes  |       -        |  image file untouched bytes  |

************************** BASIC EXAMPLE   ************************************
To send the following:
id=luc123
angle=110.10
distance=000.50
image=image file untouched bytes

You'll have to send an API request to POST an HTTP request to: 
http://192.168.1.10:8080
With data equal to:
"luc123110.10000.50xxxx..."
```

Graphical representation:

```text
                                                  __________________
                                                  |  Raspberry Pi  |
                                                  |                |
 _________     http://192.168.1.10:8080/api       |                |
|         |   POST: "luc123110.10000.50xxxx..."   |                |
| Arduino |  ------------------------------->     |      API       |
|         |  <-------------------------------     |                |
| sensors |              200 / OK                 |       |        |
|  data   |                                       |       |        |
|_________|                                       |       |        |
 _________     http://192.168.1.10:8080/          |       ↓        |
|         |                GET                    |                |
| Browser |  ------------------------------->     |     Website    |
|         |  <-------------------------------     |                |
|  List   |              200 / OK                 |                |
|  data   |                                       |                |
|  ----   |                                       |                |
|  ----   |                                       |                |
|  ----   |                                       |________________|
|_________|

```


## Installation

**Note**: This is only for the teacher.

### 1) Requirements

* Python 3
* Pip package manager

### 1) Requirements

Type these commands in the terminal:

.. code-block:: bash

    $ git clone https://github.com/lucgerrits/pi-pyserver-for-arduino-project.git
    $ pip install -r requirements.txt
    $ flask run --host=0.0.0.0 -p 8080

Local mode: http://127.0.0.1:8080/.
In AP mode: http://192.168.1.10:8080/.


## On raspberry

The Pi is already containing the nessesary program and conf.

### Mode: normal wifi
edit:
```bash
sudo nano /etc/dhcpcd.conf
# then comment last lines of file


sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.accesspoint
sudo mv /etc/dnsmasq.conf.orig /etc/dnsmasq.conf 

sudo systemctrl stop hostapd
sudo systemctrl disable hostapd
sudo reboot
```



### Mode: access point wifi

Be sure you are currently in normal wifi mode !

```bash
sudo nano /etc/dhcpcd.conf
# then uncomment last lines of file

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo mv /etc/dnsmasq.conf.accesspoint /etc/dnsmasq.conf 

sudo systemctrl stop hostapd
sudo systemctrl enable hostapd
sudo reboot
```