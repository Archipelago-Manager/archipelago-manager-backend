# Archipelago Manager Backend
Backend client for Archipelago Manager, allowing for management of [Archipelago](https://github.com/ArchipelagoMW/Archipelago) servers, giving you access to more advanced features than using [archipelago.gg](archipelago.gg)'s servers.

The project started because I wanted to have notifications in Async games.

Made to be self hosted and increase ease of use, especially for larger communities.

### The backend has(/will have) the following features:
  - [FastAPI](https://github.com/fastapi/fastapi) API that handles (create, view, change, remove, etc.):
    - Hubs (collections of users/games/files etc)
    - Games
    - Users
    - Configuration files, presets of configurations
  - Game generation
  - Configuration generation
  - Access to non-released (alpha, beta) apworlds
  - Manages actual Archipelago Servers using [Archipelago-Manager/archipelago-manager-node](https://github.com/Archipelago-Manager/archipelago-manager-node)
  - Discord connection using Archipelago-Manager/archipelago-manager-discord-bot
    - Get notifications from discord when you get items
    - Access the Archipelago server as a text client from discord
    - Create and manage games directly from discord
    - User specific notification settings (only progress items, all items etc)
  - Notification system using webhooks/popular notification systems

## How to run
### Local development
  - Create a virtual environment using python3.10 `python3.10 -m venv env && source env/bin/activate`
  - Install requirements `pip --upgrade pip && pip install -r requirements.txt`
  - Start the development FastAPI server `fastapi dev app/main.py`


### Local deployment
TODO

### Remote deployment
TODO

