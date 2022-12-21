# tm-clients

Project includes Python clients to services provided by [Techmo](http://techmo.pl/) exclusively for TM labs. 

## Requirements:
 - Installed packages listed in requirements.txt. To install requirements run:
 
 Linux:
 ```bash
 pip install -r requirements.txt
 ```
 
 Windows (with virtualenv):
 1. Move to the directory with the used interpreter python.exe.
 2. Run:
 ```bash
 python.exe -m pip install -r path_to_requirements.txt
 ```
 or use Linux command in Anaconda Shell.

 ## Clients

 This package provides API in Python to 3 systems:
 *   **Dictation** - Continuous speech recognition
 *   **TTS** - Text to speech synthesis
 
Original command line clients are provided with [Techmo GitHub](https://github.com/techmo-pl). 
Addresses and ports to the systems are stored in the json defined in address_provider.py.

## Final Remarks

* Client scripts has been tested with Python 3.9. For safety reasons create [virtual environment](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) for the project.
* When using PyCharm remember to mark directories *dictation* and *tts* as "Sources Root".  

 Contact: witkow at agh.edu.pl
