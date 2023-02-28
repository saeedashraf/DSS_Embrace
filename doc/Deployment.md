# Deployment

The parent environment should contain git and the requirements from [README](../README.md) and the repo.

```bash
# create a conda environment
$ conda create --name dss_embrace -c conda-forge python=3.10 git pipenv

# activate the environment
$ conda activate dss_embrace

# clone the repo
(dss_embrace) $ git clone https://github.com/saeedashraf/DSS_Embrace.git

# go into the main directory
(dss_embrace) $ cd DSS_Embrace
```

Next we have to install the application and start it

```bash
# make sure you are in the DSS_Embrace directory where Pipfile is needed
$ cat Pipfile

# install a pipenv environment using the Pipfile from the project
$ pipenv install

# activate the pipenv environment
$ pipenv shell

# start the application allowing the websockets
$ panel serve src/app.py --allow-websocket-origin=<ORIGIN>

```

To keep the job live can be run in the background or in live session using `screen` (where you can reconnect later).

One can check the app alone doing an ssh tunneling from the local machine

```bash
$ ssh -L localhost:5006:localhost:5006 -N <SERVER>
```

and opening locally http://localhost:5006/app .
