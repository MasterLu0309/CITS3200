# Installation
## Prerequisites
- [*Python 3*](https://python.org/) (tested working with Python 3.11.8)
- [*Ultraleap Gemini* hand tracking software](https://developer.leapmotion.com/tracking-software-download) (installed to it's default location)
    - *Ultraleap Tracking* service must be running
- [*Polhemus Liberty* USB driver](https://ftp.polhemus1.com/pub/Trackers/Liberty/)
    - *Note:* This driver is **old** and not compatible with the *Core Isolation* feature of Windows 11. Please disable this feature to use *Polhemus* tracking.
- [*SteamVR*](https://store.steampowered.com/app/250820/SteamVR/)

## Compatibility
- Tested and working Windows 10 and Windows 11*
    - Due to its age, the *Polhemus Liberty USB driver* is **not compatible** with the *Microsoft Vulnerable Driver Blocklist* feature of *Core Isolation* in Windows 11. If run while enabled, only zeroes will be captured by *Polhemus* tracking.
- Tested and working with Python 3.11.8

## Install Instructions
> *Ensure the above [prerequisites](#prerequisites) are installed **before** proceeding.*
1. Download this repository as a *zip* file.
    - Hit the green 'Code' button at the top of the page, then 'Download ZIP'.
2. Extract the *zip* file to the desired directory.
3. Double-click `initialise.py` (run with *Python*) and wait while the environment is setup.
    - This process requires an internet connection.
    - This process should only be completed **once** and can take quite a while, but no user interaction is required, so feel free to walk away from the computer.
    - A message saying, `Initialisation complete. Run 'start.py' to start the application` should be shown once the process is complete.
5. Double-click `start.py` to start the program.
    - This should be used each time you wish to start the program.

### *"`start.py` isn't working!"*
> *If `start.py` isn't working, please check the following.*
- Ensure the listed [*prerequisites*](#prerequisites) are met.
- Ensure no errors occurred during the running of `initialise.py`.
