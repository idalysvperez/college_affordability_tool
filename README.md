# college_affordability_tool  - SI 507 Final Project by Idalys Perez
SI 507 Final: CA College Affordability Tool

## Project: CA Public College Affordability Tool

This is the list of the items you need to run the code:
1. College Scorecard API key
2. ACS Census 2018 API key
3. Download required python packages to run code

## How users should interact with this program file

Welcome to the CA public college affordability tool! This tool is designed for students who are interested in college. The student can use this program that takes in their school type preferences and their household income to produce a list of viable public universities/colleges in the state that meets their needs.

When interacting with this program, students should load the python file labeled "Idalys_Perez_Final_Project" then select the run python file bottom at the top right corner. This allows the python interpreter to run the file so the student can begin using the tool. Students should then receive an output of a question asking them if they want to earn a 4 year bachelor's degree or a 2 year associates degree. The student should answer "yes" for bachelor's degree or "no" for associate's degree.

The student will then be prompted to respond with their preference of whether they want to attend a college that has over 15,000 students. The student should answer "yes" if they want to go to a school with a large student population or "no" if they do not want to attend a large school.

Then the student will be asked a series of questions related to their financial background/ household income as well as their home zip code and how far they want to commute or relocate for college. Students should answer the questions in the format that the question is asking them to respond in.

At the end, the program will either tell the student a list of their top public colleges or ask them to re-enter their search criteria because no schools were found based on their original preferences. Once the student receives a list of their schools, they will then be directed to a new browser that opens up and contains four bar graphs. Each bar graph will detail the top school matches for the student based on net price, school population size, earnings after graduation, and cost for a one bedroom in the area. The student can then exit the program or restart it again to undergo a new search.

## Where can you retrieve required items to run code
To retrieve the College Scorecard API Key the student or user should log onto "https://collegescorecard.ed.gov/data/documentation/" and scroll down to the "Register for an API key" section and complete the required information to receive a key. The student should receive an email with their key then go onto the final project python file onto line 103 to enter their individualized key in the URL section that says key.

url = f"https://api.data.gov/ed/collegescorecard/v1/schools?zip={zipcode}&distance={str(distance)}mi&api_key={replace this with the key}"

To retrieve the ACS Census API Key the student or user should log onto "https://api.census.gov/data/key_signup.html" then register for the key. The student should receive an email with their key then go onto the final project python file onto line 330 and 379 to enter their individualized key in the URL section that says key.

url_census = "https://api.census.gov/data/2018/acs/acs5?get=B25031_003E&for=tract:*&in=state:06&key={ENTER KEY IN HERE}"

The user will also have to go to the HUD site to retrieve the excel sheet for the Zip code to Census Zip Crosswalk. They should select the file that says Quarter 4 2021. They should use this site to log on at https://www.huduser.gov/portal/datasets/usps_crosswalk.html. The user should then download the excel file then save the file as a CSV on their desktop. The user will need to alter the directory of their CSV file but they can replace their file directory link to the CSV on lines 330 and 382.

Here is an example where they should substitute their link below.
    zip_tract_df = pd.read_csv("/Users/idalysperez/Documents/umich/courses/SI 507/Final Project/ZIP_TRACT_122021.csv", dtype={"tract":"string"})
    THey only need to replace the first argument that says "/Users/idalysperez/Documents/umich/courses/SI 507/Final Project/ZIP_TRACT_122021.csv" with their own directory link to the CSV.

The user will also need to install and import the following python packages including:
1. import csv
2. import json
3. import requests
4. import pandas as pd
5. import plotly.graph_objects as go


### How to understand the data structure of the College Question Tree

To understand the data structure of the College Question Tree, the user will need to first answer the question of whether they want a bachelor's or associates degree. This first question is the node of the tree since it will tailor the college list by providing either community colleges or public universities. They will then be asked if the student wants to attend a college or university that has over 15,000 students. Finally, the leaf of the tree is the function that asks the student about their financial data and distance preferences. This function will then send the student to a new webbrowser with four graphs that shows the top choice colleges for the student that meets their needs.

The data is organized in the tree so it can narrow down the results of schools based on the students preferences. The first question narrows it down by degree attainment goals and the second question narrows it further down by campus population size. The function at the end will give a list of colleges that are tailored to the student's responses and pair those schools with the college net price, student population number, cost of a one bedroom in the area, and median earnings after graduation.

Reference the file that says "idalys_perez_college_tool_tree.json" to see more information about the details and structure of the tree.

### Feel free to email me at idalys@umich.edu if you have any questions about my work.
