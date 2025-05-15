# CS163 Group 11: Pokémon Data Analysis and Web Application

## Project Overview

This repository contains a data analysis pipeline and web application focused on Pokémon data. The project encompasses data collection, preprocessing, analysis, and visualization, culminating in a user-friendly web interface that presents insights derived from the dataset.

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kevincui1034/cs163_group11.git
   cd cs163_group11
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source ./.venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   ```

3. **Run the website:**

   ```bash
   cd appengine
   python app.py
   ```

## Pipeline Overview

1. **Data Collection:**
   - Sourced Pokémon data from Pokémon datasets and Smogon website.
   - Obtained general Pokémon data such as generation, stats, type etc.
   - Obtained competetive Pokémon data such as usage rate, checks and counters, and moveset.
   - Stored data as CSV and JSON

2. **Data Preprocessing:**
   - Clean and normalize data to ensure consistency.
   - Handle missing values and correct data types.

3. **Data Analysis:**
   - Perform statistical analyses to uncover patterns and insights.
   - Generate visualizations to represent data distributions and relationships.

4. **Web Application Development:**
   - Utilizes Flask framework for web development.
   - Dash framework for styling and graphs.
   - Deploy the application using Google App Engine.

## Directory Structure

- `/pokemon_analysis/`: Contains scripts and notebooks for data preprocessing and analysis. **Not for web application**
- `/appengine/`: Houses the web app functionality, components, data, routes.
   - app.py: Sets up the Dash web application and defines the main layout of the app.
     - If you want to run the Pokemon Recommender, you have to uncomment out the link to the Pokemon Recommender, the current one is a placeholder because the model is too large.
   - app.yaml: Config file for Google App Engine.
   - `/assets/`: For custom CSS styling and pictures.
   - `/components/`: Functions used for page callbacks.
      - data_loader.py: handles loading the data for GCS or loading it for local testing.
      - pokemon_move_recommender.py: Generates optimal move given current Pokemon and opposing Pokemon. **Not for web hosting because model is too large, 8GB per every month of data**
      - train_and_save_model.py: Trains and saves the model into a pickle file.
      - visualizations.py: Handles the graphs for each page.
      - `/data/`: Data for local deployment and testing.
      ************
      - `/models/`: Not hosted on GitHub, has pretrained models for the Pokemon Recommender, 8GB model for each month of data
      ************
   - `/pages/`: Holds each page for this multi-page Dash app.

## 🔗 Live Website

Access the deployed web application here: [https://cs163-group11.uw.r.appspot.com/](https://cs163-group11.uw.r.appspot.com/)
