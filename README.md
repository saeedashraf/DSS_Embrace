# DSS_Embrace

A collaborative environment to embrace deep uncertainties in decision making on climate risks

Climate change impacts will become more pronounced in the next decades. Decision on climate risks is riddled with deep uncertainties. We plan to co-design and deploy a decision support system which assist decision makers, businesses and city planners to deal with deeply uncertain problems for smart and robust adaptation planning and implementation.

## Branching scheme of the GitHub repository

[Git Feature Branch Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow) is used. `main` is the maintained and up-to-date branch.
Documentation and examples are generated from the main branch.

## Development

- used on M1 macOS
- expected to run fin on at least on Linux and MacOS

### Requirements

- Python 3.10 ([pyenv](https://github.com/pyenv/pyenv) conda-like for managing the Python version)
- [Pipenv](https://pipenv.pypa.io/en/latest/) for creating and managing a virtual environment for the project

### Instructions

- clone the repo and go in the main directory

- prepare the dev environment

```bash
# OPTIONAL and only if you use pyenv. Feel free to use a different patch version
$ pyenv local 3.10.9

# make sure you are using the desired versions
$ python --version
Python 3.10.9

$ pipenv install --dev
$ pipenv shell


$ pre-commit install
```

- start panel enabling autoreload

```bash
$ panel serve src/app.py --autoreload --show
```

- stop Panel when done
