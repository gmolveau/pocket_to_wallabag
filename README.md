# Pocket to wallabag exporter

Use this script to export your [pocket](https://getpocket.com) items to [wallabag](https://www.wallabag.it).

## Getting started

### API Keys

You first need to create an application on pocket : [https://getpocket.com/developer/apps/](https://getpocket.com/developer/apps/).

Pocket will give you a `Consumer Key`.

Next in wallabag, `create a new client` in `API clients management`. This will give you a `Client ID` and a `Client secret`.

Edit all those informations in `env.py`.

### Requirements

The only dependency is `requests` so you can either install it globally with `pip3 install --user requests` or use a `virtualenv`.

To create the virtualenv : `python3 -m venv venv`.

Activate it : `source venv/bin/activate`

And install the necessary libraries : `pip3 install -r requirements.txt`

### Execution

Then, execute the script : `python3 pocket_to_wallabag.py`

Done :)

---

PS: to import 382 items here's the time result : `5.97s user 0.26s system 1% cpu 10:20.49 total` so 10 minutes.

PSS : you can change the line `"state": "unread",` to `"state": "all",` in `pocket_to_wallabag.py` if you want to export ALL your pocket items (archived ones included).