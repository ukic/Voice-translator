# Python implementation of Techmo TTS gRPC client.


## How to prepare virtual environment and run Dictation Client on Windows 10


### Prerequisites

If Python is not installed on your system, download the Python 3.10 installer from: https://www.python.org/downloads/windows/ and install.
Remember to mark checkbox:
```
Add Python 3.10 to PATH
```


Start the PowerShell with `Run as Administrator`.

Temporarily change the PowerShell's execution policy to allow scripting:

```
Set-ExecutionPolicy RemoteSigned
```
then confirm your choice.

Navigate into the project root directory, eg.:

```
cd C:\Users\Jan_Kowalski\Desktop\techmo-tts-client-python\
```

Create virtual environment for project:

```
python -m venv .venv
```

Activate newly created virtual environment:
```
.\.venv\Scripts\activate
```

Install required packages:
```
pip install -r requirements.txt
```


To switch back PowerShell's execution policy to the default, use command:

```
Set-ExecutionPolicy Restricted
```




## Usage

Basic request:

```
python tts_client.py --service-address ADDRESS --text TEXT
```


For example:

```
python tts_client.py --service-address "demo.devtechmo.pl:25515" --text "Polski tekst do syntezy"
```


To get list of all available options, use:
```
python tts_client.py --help
```
