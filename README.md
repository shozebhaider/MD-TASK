# MD-RIN
Tool suite for analysing molecular dynamics trajectories using network analysis and PRS

##1. Introduction

MD-RIN consists of a suite of Python scripts that have been developed to analyze molecular dynamics trajectories.

Detailed documentation can be found readthedocs.

## Installation

### Download the project
```bash
git clone https://github.com/RUBi-ZA/JMS.git
cd MD-RIN
```
### Install dependencies and set up Python virtual environment
```bash
sudo apt-get install virtualenvwrapper python-dev libblas-dev liblapack-dev libatlas-base-dev gfortran libpng12-dev libfreetype6-dev python-tk
virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install numpy 
pip install scipy 
pip install matplotlib cython networkx natsort
pip install mdtraj
```


