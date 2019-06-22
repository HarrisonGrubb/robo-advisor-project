# RoboAdvisor

Connecting to the Alphavantage API and getting daily and weekly time series data on stock market movements

## System Requirements

* Anaconda 3.7
* Python 3.7
* Pip
* Git

## Installation

1.)  You can fork this repo into your own Github account either through the web-based GUI or through GIT commands.  Ensure that you've downloaded this repo to your local machine.

2.) Navigate to the newly created repository before proceeding with any of the following steps.
    `cd name-of-your-directory`

3.) Create a new virtual enviroment in prepration to install the third party packages.  You can use the below code as a template to get your enviroment set up.
    `conda create -n name-of-your-env`
    `conda activate name-of-your-env`

4.) Once you've activated your enviroment.  You can install the third party packages.  They're listed in the requirements.txt file if you're curious.  
    `pip install -r requirments.txt`

If you've followed along to this point you're good to go run the app.

## Runing the App

Ensure you're in the main directory of this repository.  

Once there you can run the app with following code.
    `python app/robo-advisor.py`

The app will ask you to input a ticker symbol of the stock or ETF of your choice.  

This app will print a summary output, and will launch a visualization.  Because of the visualization, you will need to hit the ENTER button when you're ready to stop running the app.  
