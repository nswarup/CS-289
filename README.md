# Lane Dynamics in Traffic Flow

A simulator by Nisha Swarup and Billy Cox.

## Installation

1. Clone the repo and navigate to its directory
2. Make sure you have python, pip, and virtualenv installed (`pip install virtualenv`).
3. Create and activate a virtual environment with `virtualenv env` and then `source env/bin/activate`.
4. With the virtual environment activated, run `pip install -r requirements.txt` to install the dependencies.
5. When you're done, don't forget to deactivate the environment by running `deactivate`.

## Usage

There are several different simulation models, which are described in detail in the paper. These include `SingleLaneIDM`, `MultiLaneIDM`, `LaneSwitchIDM`, and `SinglePerturbation`. `main.py` takes the name of the simulation as a command line argument, so to run `MultiLaneIDM` (for example):

`python main.py MultiLaneIDM`

At the end of the simulation, this will collect data on various metrics in `out.csv`. The simulation will take a while, but to run it without the visualization for speed purposes, you can open `constants.py` and change `VISUALIZING` from `True` to `False`.
