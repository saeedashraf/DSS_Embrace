# Deployment
## Preparation (done just once)

Go to `project-data` directory, clone the repo, create the conda environment and next the pipenv environment.  
The conda environment should contain git and the requirements from [README](../README.md), i.e., pipenv and python=10.
The pipenv environment is built based on the Pipfile.

```bash
$ cd /project-data

# create a conda environment
$ conda create --prefix /project-data/conda-envs/dss_embrace -c conda-forge python=3.10 git pipenv

# clone the repo
$ git clone https://github.com/saeedashraf/DSS_Embrace.git

# go into the main directory
$ cd DSS_Embrace

# make sure you are in the DSS_Embrace directory where Pipfile is needed
$ cat Pipfile


# Custom Virtual Environment Location https://pipenv-fork.readthedocs.io/en/latest/advanced.html#custom-virtual-environment-location
$ export PIPENV_VENV_IN_PROJECT=1
# create the .venv directory for the pipenv virtual environment
$ mkdir .venv

# install a pipenv environment using the Pipfile from the project
$ conda run --prefix /project-data/conda-envs/dss_embrace pipenv install --python=/project-data/conda-envs/dss_embrace/bin/python
```

## Start Panel

```
Last but not least we start the application (no need to be in the conda environment)
# make sure you are in the project directory
$ cd /project-data/DSS_Embrace/

# start the application allowing the websockets
# see /etc/systemd/system/dss-embrace.service 
```

## For Testing only

To keep the job live can be run in the background or in live session using `screen` (where you can reconnect later).

One can check the app alone doing an ssh tunneling from the local machine

```bash
$ ssh -L localhost:5006:localhost:5006 -N <SERVER>
```

and opening locally http://localhost:5006/app .
