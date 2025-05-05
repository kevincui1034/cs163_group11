# CS163 Group 11: Pokémon Data Analysis and Web Application

## Project Overview

This repository contains a data analysis pipeline and web application focused on Pokémon data. The project encompasses data collection, preprocessing, analysis, and visualization, culminating in a user-friendly web interface that presents insights derived from the dataset.

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/kevincui1034/cs163_group11.git
   cd cs163_group11
   ```

2. **Create and activate a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages:**

   ```bash
   pip install -r requirements.txt
   ```

   *Note: Ensure that a `requirements.txt` file is present in the root directory listing all necessary packages.*

## Pipeline Overview

1. **Data Collection:**
   - Source Pokémon data from reputable datasets or APIs.
   - Store raw data in a structured format (e.g., CSV, JSON).

2. **Data Preprocessing:**
   - Clean and normalize data to ensure consistency.
   - Handle missing values and correct data types.

3. **Data Analysis:**
   - Perform statistical analyses to uncover patterns and insights.
   - Generate visualizations to represent data distributions and relationships.

4. **Web Application Development:**
   - Utilize frameworks like Flask or Django to build the backend.
   - Design frontend interfaces to display analyses and visualizations.
   - Deploy the application using platforms like Google App Engine.

## Directory Structure

- `/pokemon_analysis/`: Contains scripts and notebooks for data preprocessing and analysis.
- `/appengine/`: Houses the web application code, including backend and frontend components.
- `requirements.txt`: Lists all Python dependencies required to run the project.
- `.gitignore`: Specifies files and directories to be ignored by Git.

## 🔗 Live Website

Access the deployed web application here: [https://cs163-group11.uw.r.appspot.com/](https://cs163-group11.uw.r.appspot.com/)

*Replace the above URL with the actual link to your deployed application.*
