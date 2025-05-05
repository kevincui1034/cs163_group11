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

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv .venv
   source ./.venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Pipeline Overview

1. **Data Collection:**
   - Sourced Pokémon data from Pokémon tournaments and gameplay
   - Obtained general Pokémon data such as generation, stats, type etc.
   - Stored data as CSV and JSON

2. **Data Preprocessing:**
   - Clean and normalize data to ensure consistency.
   - Handle missing values and correct data types.

3. **Data Analysis:**
   - Perform statistical analyses to uncover patterns and insights.
   - Generate visualizations to represent data distributions and relationships.

4. **Web Application Development:**
   - Utilize Flask framework to build the backend.
   - Frontend interfaces to display analyses and visualizations.
   - Deploy the application using Google App Engine.

## Directory Structure

- `/pokemon_analysis/`: Contains scripts and notebooks for data preprocessing and analysis.
- `/appengine/`: Houses the web app functionality, components, data, routes.
   - `/assets/`: For custom CSS styling.
   - `/components/`: Functions used for page callbacks.
      - `/data/`: Data for local deployment and testing.
   - `/pages/`: Routes for each page of the website.

## 🔗 Live Website

Access the deployed web application here: [https://cs163-group11.uw.r.appspot.com/](https://cs163-group11.uw.r.appspot.com/)