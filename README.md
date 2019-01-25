# WIMM - Where Is My Money?

WIMM is a yet-another self-hosted single user money and budget tracker.
There are so many budget trackers it's just easier to code a new one
than to choose one.

(Edit: probably not)

**This version is at pre-alpha version at the moment**

## Setup

### Using Docker

1. Prerequisites

    Install `docker` and `docker-compose`.
    See official instructions for
    [Docker](https://www.docker.com/get-started) and
    [Compose](https://docs.docker.com/compose/install/).

2. Create docker image

    - run `docker-compose up`
    - or to detach it right away to run in background `docker-compose up -d`

    For further configuration see `docker-compose.yaml` and
    `Dockerimage` files in the source root, and other configuration
    files in `docker/` folder.

### Manual setup

1. Prerequisites

    To build manually you'll need the following packages installed:

    - **Python 3.7* and **pip 18.1** (optionally within a virtual environment) for backend
    - **Node 11.7** and **NPM 6.5** for client (frontend)
    - **uWSGI** via pip for hosting the backend code
    - **nginx** for delegate it to be accessible via http

1. Build client (frontend)

    ```
    cd client
    npm i && npm build
    cd ..
    ```

2. Install server dependencies
    ```
    cd server
    pip install -r requirements.txt
    cd ..
    ```

3. Copy static files from client
    ```
    cp client/dist server/static
    ```

3. Install and Configure Nginx:

    TBD

3. Configure your server with uWSGI
    ```
    cp ./docker/uwsgi.ini /server/wusgi.ini
    ```
    See Flask's [uWSGI documentation](http://flask.pocoo.org/docs/1.0/deploying/uwsgi/) for further details

4. Run the server with uwsgi:

    *TODO: This needs to be defined and tested well*
    ```
    uwsgi -s /tmp/wimm2.sock --manage-script-name --mount /wimm=server:app
    ```

## Details

WIMM is a dead simple application. I think an Excel spreadsheet
with some VBA magic could have the exact same features.

However you can host this app on your server, so you can use
your Raspberry Pi for more than just seeding Linux distros and
watching Big Buck Bunny.

## Development stuff

Any contribution ot this project is welcomed, and appreciated, however
there isn't any developer guideline set at this moment.

- For python static code analysis an style check we use `flake8`, however it's not fully configured.

### Running tests

1. Server (backend)

    ```
    cd server/
    python tests.py
    ```

2. Client (frontend)
    - There's none ATM

### Features

TBD

### Future development

TBD
