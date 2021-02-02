# pi-pyserver-for-arduino-project

A Python web server aims to receive and display Arduino messages.

A message is a **fixed length string** that follows this rule:
```text
[_____id_____][_____angle_____][_____distance_____]

|____parameter___|___Bytes___|_____example____|_______usage note_________|
| id             | 6 bytes   |  luc123        |  use ascii char [a-Z0-9] |
| angle          | 6 bytes   |  110.10        |  min=0.00 ; max=360.00   |
| distance       | 6 bytes   |  000.50        |  min=0.00 ; max=999.99   |


**************************  EXAMPLE   ************************************
To send the following:
id=luc123
angle=110.10
distance=000.50

You'll have to send an API request to POST an HTTP request to: 
http://192.168.1.1:8080
With data equal to:
"luc123110.10000.50"

Graphical representation:
                                              __________________
                                              |  Raspberry Pi  |
                                              |                |
 _________     http://192.168.1.1:8080/api    |                |
|         |     POST: "luc123110.10000.50"    |                |
| Arduino |  -------------------------------> |      API       |
|         |  <------------------------------- |                |
| sensors |              200 / OK             |       |        |
|  data   |                                   |       |        |
|_________|                                   |       |        |
 _________     http://192.168.1.1:8080/       |       ↓        |
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

Now go to http://127.0.0.1:8080.

