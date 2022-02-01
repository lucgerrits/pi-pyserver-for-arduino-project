# pi-pyserver-for-arduino-project

A Python web server aims to receive and display Arduino messages.

**Note**: All POST request to the API need to be formated (examples bellow) AND the http content type requires to be "binary". The data is the concatenation of the parameters data.

## 1 ) Send messages

A message is a **fixed length binary** that follows this rule:
```text
[_____angle_____][_____distance_____]

|____parameter___|____Bytes____|_____example________|______________usage note_________________|
| angle          | 1 bytes     |  0x05              |  min=000.00 ; max=255                   |
| distance       | 4 bytes     |  0x04950000        |  min=-1.17549e-38 ; max=3.40282e+38     |

************************** BASIC EXAMPLE   ************************************
To send the following:
angle=0x05
distance=0x04950000

You'll have to send an API request to POST an HTTP request to: 
http://192.168.1.10:8080
With data equal to:
"0x0504950000"
```

Graphical representation:

```text
                                              __________________
                                              |  Raspberry Pi  |
                                              |                |
 _________     http://192.168.1.10:8080/api   |                |
|         |     POST: "0x0504950000"          |                |
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

## 2 ) Send messages with images

A message is a **variable length binary** that follows this rule:
```text
[_____angle_____][_____distance_____][_____image_____]

|____parameter___|____Bytes____|_____example________|______________usage note_________________|
| angle          | 1 bytes     |  0x05              |  min=000.00 ; max=255                   |
| distance       | 4 bytes     |  0x04950000        |  min=-1.17549e-38 ; max=3.40282e+38     |
| image          | X bytes     |       -            |  image file raw jpg bytes               |

************************** BASIC EXAMPLE   ************************************
To send the following:
angle=0x05
distance=0x04950000
image=image file raw jpg bytes

You'll have to send an API request to POST an HTTP request to: 
http://192.168.1.10:8080
With data equal to:
"0x0504950000xxxx[...]xxx"
```

Graphical representation:

```text
                                                  __________________
                                                  |  Raspberry Pi  |
                                                  |                |
 _________     http://192.168.1.10:8080/api       |                |
|         |   POST: "0x0504950000xxxx[...]xxx"    |                |
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


## Installation

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


## On raspberry

The Pi is already containing the nessesary program and conf (using [this](https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md)).

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
