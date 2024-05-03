# City Classifier 🏙️
## Description

City Classifier is a query answering machine that uses a machine learning model to classify images based on the city of origin. It uses a Convolutional Neural Network (CNN) to classify cities with over 80% accuracy.

## Installation

City Classifier requires Python 3.10 or above which can be downloaded from [the official Python webpage](https://www.python.org/downloads/).

Various python libraries are also needed to run the program (the extensive list can be found in the requirements.txt file) which can be installed in a python virtual environment or in the local python installation. The steps to install all required packages are outlined below.

You also need to have the model installed and in the same directory as the main.py file. You can download the model from [this link](https://www.kaggle.com/models/salmanhajizada/cities-classifier).

#### Installation in local python install

Run the following command: `$ pip install -r requirements.txt`

#### Installation in a virtual environment

Navigate to the directory you would like to place the virtual environment in and run the following commands:

`$ python -m venv venv`

on Windows run: `$ venv/Scripts/activate`

on Linux/Mac run: `$ venv/bin/activate`

`$ pip install -r requirements.txt`

To exit the virtual environment run: `$ deactivate`

## How to run

To run the classifier, run the python file `main.py` by running the command:

`$ python main.py`

Make sure the model is in the same directory as the main file and is named `cities_classifier.keras`

## Dataset

The dataset used to train the model was scraped from DuckDuckGo. The scraping files are included and can be found [here](https://www.kaggle.com/datasets/salmanhajizada/images-of-major-capital-cities).

## Acknowledgements

This project was a group effort with [Ravin Kumar](https://github.com/Ravin-Kumar) and [Abdulrahman Taweel](https://github.com/Aboud04).
