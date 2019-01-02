# WIMM - Where Is My Money?

There are so many budget trackers it's just easier to code a new one
than to choose one.

(Edit: probably not)

## Where Is My UI?

This repo contains the backend code only. The reference frontend
lives here: [https://github.com/slapec/wimm-vue](https://github.com/slapec/wimm-vue)

## Setup

1.  Get a Python 3 environment

    The project is developed in 3.5.1 but I think it should work with
    any 3.x version.
    
2.  Install dependencies:

    `pip install -r requirements`
    
3.  Create the `wimm/settings.py` file and define the missing names
    in it (see the list in the example below).

    It's a good idea to import everything from `wimm/base_settings.py`
    in your settings file like this:
    
    ```
    from wimm.base_settings import *
    
    DEBUG = False
    SECRET_KEY = 'some secret'
    STATIC_ROOT = '/some_folder/'
    ```
    
    For the full list of available settings [check the Django 
    documentation](https://docs.djangoproject.com/en/1.9/ref/settings/)

4.  Start the application

    ```
    ptython manage.py runserver
    ```

## Details

WIMM is a dead simple application. I think an Excel spreadsheet
with some VBA magic could have the exact same features.

However you can host this app on your server, so you can use
your Raspberry Pi for more than just seeding Linux distros and
watching Big Buck Bunny.
