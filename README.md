# Customer Order System
## **How everything Works:**

Flask handles the logic, like processing requests and backend logic.
The HTML structures the page and the CSS styles it to make it look nice.

## Project Structure:
app.py - Main Python file. You can add user inputs, database connections and stuff here. (You can create seperate python files if you want).

Templates Folder:
  Contains the HTML files 
  
      index.html  - Starting page of the app. 

Static Folder:
  Holds the CSS, images or other styling files needed
      
      styles.css - Css file to style the website

.gitignore - Tell's git which files/folders to ignore

requirements.txt - Contains list of python libraries needed for the app to work. You can install the libraries with

pip install -r requirements.txt


## Setup:
git clone https://github.com/ajali07/CSE-412-Project.git
cd CSE-412-Project

#Setting up virtual environment

## Windows

python -m venv venv

venv\Scripts\activate

## Mac
python3 -m venv venv

source venv/bin/activate

## General
Install dependencies 

pip install -r requirements.txt

python app.py - Hopefully that works






