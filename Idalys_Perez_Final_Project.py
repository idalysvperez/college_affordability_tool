import csv
import json
import requests

import pandas as pd
import plotly.graph_objects as go


# from Tree_format import printTree1


#Tree Structure Functions
def isLeaf(tree): #checks if it's a leaf or a node
    if tree[1] == None and tree[2] == None:
        return True
    else:
        return False


def call_college_questions(tree): #reorganize to collect info based on their answers
    """DOCSTRING!"""
    if isLeaf(tree):
        # save_tree = tree
        # save_user_answer =
        # print(f"Here are your recommended schools: {save_tree[0]}")
        # print(tree[0])
        return tree[0]
        #return save_user_answer #CHECK
            # return True
    else:
        # new_tree = tree
        question = input({tree[0]})
        if question in ["Yes", "Yep", "yes", "y","es","ye", "YES"]:
            return call_college_questions(tree[1]) #calls question on the left #added return for each one
        else:
            return call_college_questions(tree[2]) #calls question on the right


#Helper functions to call and navigate API
def get_resource(url, params=None, timeout=10):
    if params:
        return requests.get(url, params, timeout=timeout).json()
    else:
        return requests.get(url, timeout=timeout).json()


def read_csv(filepath, encoding='utf-8', newline='', delimiter=','):
    with open(filepath, 'r', encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)

        return data


def read_csv_to_dicts(filepath, encoding='utf-8', newline='', delimiter=','):
    with open(filepath, 'r', newline=newline, encoding=encoding) as file_obj:
        data = []
        reader = csv.DictReader(file_obj, delimiter=delimiter)
        for line in reader:
            data.append(line) # OrderedDict()
            # data.append(dict(line)) # convert OrderedDict() to dict

        return data


def read_json(filepath, encoding='utf-8'):
    with open(filepath, 'r', encoding=encoding) as file_obj:
        return json.load(file_obj)


def write_json(filepath, data, encoding='utf-8', ensure_ascii=False, indent=2):
    with open(filepath, 'w', encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)



#CACHING COLLEGE SCORECARD DATA BY ZIPCODE

def open_cache(scorecache_file):
    try: #checks to see if file exists
        cache_file = open(scorecache_file, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, scorecache_file):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(scorecache_file,"w")
    fw.write(dumped_json_cache)
    fw.close()

def scorecard_with_cache(zipcode, distance, SCORECARD_CACHE, scorecache_file):
    if str(zipcode) in SCORECARD_CACHE.keys():        # is result for n already there?
        # print("CASH HIT")
        return SCORECARD_CACHE[zipcode]   # if so, look up result and return it
    else:
        url = f"https://api.data.gov/ed/collegescorecard/v1/schools?zip={zipcode}&distance={str(distance)}mi&api_key=XnOe8R0JJpXpYaDlTm5hDkSN29IfEHQlB3SasmER"
        response3 = requests.get(url)           # cache miss!
        SCORECARD_CACHE[zipcode] = json.loads(response3.text) # do the operation and save the result
        # print("CASH MISSED")
        save_cache(SCORECARD_CACHE, scorecache_file) #saves the entire dictionary.
        return SCORECARD_CACHE[zipcode] #info that user wants which is results


#CLEAN AND PARSE THE DATA

def student_info():
    begin_tool = input(f"Reply with 'start' to begin the CA Public College Affordability Tool. Reply 'exit' to close the tool.")
    if begin_tool in ["start","START","strt","start!","Start"]:
        student_zipcode = input(f"Enter student zipcode or reply 'exit' to quit tool")
        if student_zipcode.isnumeric():
            student_income = input(f"What is your household income? Enter only a numeric value or reply 'exit' to quit tool.")
            if student_income.isnumeric():
                student_distance = input(f"What is the maximum distance from home that you are willing to travel or relocate to attend college? Enter distance in miles or reply 'exit' to quit tool.")
                return [student_zipcode, student_income, student_distance]
            else:
                if student_income == "exit":
                    print('Bye!')
                quit()
        else:
            if student_zipcode == "exit":
                print('Bye!')
                quit()
    else:
        print('Bye!')
        quit()



def student_info_CC():
    begin_tool = input(f"Reply with 'start' to begin the CA Public College Affordability Tool. Reply 'exit' to close the tool.")
    if begin_tool in ["start","START","strt","start!"]:
        student_zipcode = input(f"Enter student zipcode or reply 'exit' to quit tool.")
        if student_zipcode.isnumeric():
            student_income = input(f"What is your household income? Enter only a numeric value or reply 'exit' to quit tool.")
            if student_income.isnumeric():
                student_distance = input(f"What is the maximum distance from home that you are willing to travel or relocate to attend college? Enter distance in miles or reply 'exit' to quit tool.")
                return [student_zipcode, student_income, student_distance]
            else:
                if student_income == "exit":
                    print('Bye!')
                quit()
        else:
            if student_zipcode == "exit":
                print('Bye!')
                quit()
    else:
        print('Bye!')
        quit()


public_school_list = []

def select_public_schools(schools, student_zipcode): #this should be the list of dictionaries
    for i in schools[str(student_zipcode)]["results"]:
        if i["latest"]["programs"]["cip_4_digit"][0]["school"]["type"].lower() == "public": #UCSD
            school_name = i["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
            public_school_list.append({"name": school_name}) #This adds a key value pair in the dictionary

def two_or_four_year(school, student_zipcode):
    for schl in school[str(student_zipcode)]["results"]: #HOW DO I LOOP THOUGH THIS
        if int(schl["latest"]["school"]["degrees_awarded"]["highest"]):
            school_name = schl["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
            degree_type = schl["latest"]["school"]["degrees_awarded"]["highest"]
            for x in public_school_list:
                    if x["name"] == school_name:
                        x["Degree Type"] = str(degree_type)

public_school_list2 = []

def filter_degree_type(student_answer, public_school_list):
    if student_answer in ["yes","ye","yeah","yup","Yes","YES"]:
        for school in public_school_list:
            if school["Degree Type"] == "4":
                public_school_list2.append({"name": school["name"]})
    else:
        for school in public_school_list:
            if school["Degree Type"] == "2":
                public_school_list2.append({"name": school["name"]})

def convert_zip_to_tract(df, city, zipcode):
    zipcode = int(zipcode)
    try:
        tract_df = df[df['usps_zip_pref_city']== city.upper()]
        reset_df = tract_df.reset_index()
        census_tract = reset_df['tract'][0]#index for the first census block
        census_tract = str(census_tract)
        census_tract = census_tract
        return census_tract
    except:
        tract_df = df[df['zip']== zipcode]
        reset_df = tract_df.reset_index()
        census_tract = reset_df['tract'][0]#index for the first census block
        census_tract = str(census_tract)
        census_tract = census_tract
        return census_tract

def school_size(school, student_zipcode): #Use try and except
    for schl in school[str(student_zipcode)]["results"]: #HOW DO I LOOP THOUGH THIS
        try:
            if int(schl["latest"]["student"]["size"]) > 15000:
                # over_15K_size.append(schl["latest"]["programs"]["cip_4_digit"][0]["school"]["name"])
                school_name = schl["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
                student_population = schl["latest"]["student"]["size"]
                for x in public_school_list2:
                    if x["name"] == school_name:
                        x["Student Population"] = student_population
            elif int(schl["latest"]["student"]["size"]) <= 15000:
                # under_15K_size.append(schl["latest"]["programs"]["cip_4_digit"][0]["school"]["name"])
                # return over_15K_size
                school_name = schl["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
                student_population = schl["latest"]["student"]["size"]
                for x in public_school_list2:
                    if x["name"] == school_name:
                        x["Student Population"] = student_population
        except:
            school_name = schl["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
            # population_size_not_available.append(school_name)
            student_population = "Not Available"
            for x in public_school_list2:
                if x["name"] == school_name:
                    x["Student Population"] = student_population

public_school_list3 = []
not_available_list = []

def filter_population_size(student_answer, public_school_list2):

    for school in public_school_list2:
        try:
            # print(school["name"])
            # print(school["Student Population"])
            if student_answer in ["yes","ye","yeah","yup","Yes","YES"]:
                if int(school["Student Population"]) > 15000:
                    # print(school["Student Population"])
                    public_school_list3.append({"name": school["name"]})
                    for x in public_school_list3:
                        if x["name"] == school["name"]:
                            x["Student Population"] = school["Student Population"]
            else:
                if int(school["Student Population"]) <= 15000:
                    public_school_list3.append({"name": school["name"]})
                # public_school_list3.append({"Student Population": school["Student Population"]})
                    for x in public_school_list3:
                        if x["name"] == school["name"]:
                            x["Student Population"] = school["Student Population"]
        except:
            not_available_list.append({"name": school["name"]})
            for x in not_available_list:
                if x["name"] == school["name"]:
                    x["Student Population"] = "Not Available"
            continue


def student_net_price(student_income, cached_data, student_zipcode): #ADD INPUT
    #once user inputs their income I will have income brackets set up to see which one matches their financial aid need.
    #this function will return their potential financial aid coverage along with the cost of tuition at that selected university.
    for school in cached_data[str(student_zipcode)]["results"]:
        # if school:
        if int(student_income) <= 30000:
            net_price = school["latest"]["cost"]["net_price"]["public"]["by_income_level"]["0-30000"]
            school_name = school["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
            school_zipcode = school["latest"]["school"]["zip"]
            school_zipcode = school_zipcode[0:5]
            school_city = school["latest"]["school"]["city"]
            for x in public_school_list3:
                if x["name"] == school_name:
                    x["net_price"] = net_price
                    x["School Zipcode"] = school_zipcode
                    x["School City"] = school_city
        elif 30001 <= int(student_income) <= 75000:
            net_price = school["latest"]["cost"]["net_price"]["public"]["by_income_level"]["30001-75000"]
            school_name = school["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
            school_zipcode = school["latest"]["school"]["zip"]
            school_zipcode = school_zipcode[0:5]
            school_city = school["latest"]["school"]["city"]
            for x in public_school_list3:
                if x["name"] == school_name:
                    x["net_price"] = net_price
                    x["School Zipcode"] = school_zipcode
                    x["School City"] = school_city
        elif 75001 <= int(student_income) <= 110000000:
            net_price = school["latest"]["cost"]["net_price"]["public"]["by_income_level"]["75001-110000"]
            school_name = school["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
            school_zipcode = school["latest"]["school"]["zip"]
            school_zipcode = school_zipcode[0:5]
            school_city = school["latest"]["school"]["city"]
            for x in public_school_list3:
                if x["name"] == school_name:
                    x["net_price"] = net_price
                    x["School Zipcode"] = school_zipcode
                    x["School City"] = school_city

def school_median_income(school, student_zipcode):
    for schl in school[str(student_zipcode)]["results"]:
        school_earnings1 = schl["latest"]["earnings"]["10_yrs_after_entry"]["median"]
        school_name = schl["latest"]["programs"]["cip_4_digit"][0]["school"]["name"]
        for x in public_school_list3:
                if x["name"] == school_name:
                    x["Median earnings after graduation"] = school_earnings1

#LAST TREE FUNCTIONS

def tree_function_4_year(answer_school_size): #inputs are yes and yes #may need to run student_info before this function
    user_questions = student_info()
    zipcode = int(user_questions[0])
    distance = user_questions[2]
    student_income = int(user_questions[1])
    scorecache_file = input("Please insert a new name for the file. Make sure to include .json at the end (filename.json)")
    scorecard_cache_input = open_cache(scorecache_file)
    scorecard_with_cache(zipcode, distance, scorecard_cache_input, scorecache_file) #HOW TO I EDIT JSON NAME AND CALL IT
    scorecard_cache_data = read_json(scorecache_file)
    select_public_schools(scorecard_cache_data, zipcode) #How do I narrow down the scope to this.
    two_or_four_year(scorecard_cache_data, zipcode)
    filter_degree_type("yes", public_school_list)
    # print(public_school_list2)
    school_size(scorecard_cache_data, zipcode)
    filter_population_size(answer_school_size, public_school_list2)
    # print(public_school_list3)
    student_net_price(student_income, scorecard_cache_data, zipcode)
    # print(public_school_list3)
    school_median_income(scorecard_cache_data, zipcode)
    # print(public_school_list3)
    url_census = "https://api.census.gov/data/2018/acs/acs5?get=B25031_003E&for=tract:*&in=state:06&key=b026a491bed6c8d67183bd6b61b11eade7382ace"
    response2 = requests.get(url_census) #the json given to us is the website
    CensusData = json.loads(response2.text)
    zip_tract_df = pd.read_csv("/Users/idalysperez/Documents/umich/courses/SI 507/Final Project/ZIP_TRACT_122021.csv", dtype={"tract":"string"})
    for x in public_school_list3:
        census_tract = convert_zip_to_tract(zip_tract_df, x["School City"], x["School Zipcode"])
        x["Census Tract"] = census_tract
        for i in CensusData:
            if i[1]+i[2]+i[3] == census_tract:
                x["Cost of 1 Bedroom"] = i[0] #PRICE OF 1BD

    # for x in public_school_list:
    for x in public_school_list3:
        if x["Cost of 1 Bedroom"] == '-666666666':
            x["Cost of 1 Bedroom"] = "Room price not available"
    print(public_school_list3)

    if len(public_school_list3) == 0:
        print("There are no schools under that search criteria. Please re-start the screening question process to enter new search criteria. Thank you!")
        quit()
    else:
        print("You will be receiving data on the public universities/colleges that best meet your needs. List of your top schools with data loading...")
        pass






def tree_function_CC(answer_school_size): #inputs are yes and yes #may need to run student_info before this function
    user_questions = student_info_CC()
    zipcode = int(user_questions[0])
    student_income = int(user_questions[1])
    distance = user_questions[2]
    scorecache_file = input("Please insert a new name for the file. Make sure to include .json at the end (filename.json)")
    scorecard_cache_input = open_cache(scorecache_file)
    scorecard_with_cache(zipcode, distance, scorecard_cache_input, scorecache_file) #HOW TO I EDIT JSON NAME AND CALL IT
    scorecard_cache_data = read_json(scorecache_file)
    select_public_schools(scorecard_cache_data, zipcode) #How do I narrow down the scope to this.
    two_or_four_year(scorecard_cache_data, zipcode)
    filter_degree_type("no", public_school_list)
    # print(public_school_list2)
    school_size(scorecard_cache_data, zipcode)
    filter_population_size(answer_school_size, public_school_list2)
    # print(public_school_list3)
    student_net_price(student_income, scorecard_cache_data, zipcode)
    # print(public_school_list3)
    school_median_income(scorecard_cache_data, zipcode)
    # print(public_school_list3)
    url_census = "https://api.census.gov/data/2018/acs/acs5?get=B25031_003E&for=tract:*&in=state:06&key=b026a491bed6c8d67183bd6b61b11eade7382ace"
    response2 = requests.get(url_census) #the json given to us is the website
    CensusData = json.loads(response2.text)
    zip_tract_df = pd.read_csv("/Users/idalysperez/Documents/umich/courses/SI 507/Final Project/ZIP_TRACT_122021.csv", dtype={"tract":"string"})
    # print(zip_tract_df)
    for x in public_school_list3:
        # print(x)
        census_tract = convert_zip_to_tract(zip_tract_df, x["School City"], x["School Zipcode"])
        x["Census Tract"] = census_tract
        # print(public_school_list3)
        for i in CensusData:
            if i[1]+i[2]+i[3] == census_tract:
                x["Cost of 1 Bedroom"] = i[0] #PRICE OF 1BD
    for x in public_school_list3:
        if x["Cost of 1 Bedroom"] == '-666666666':
            x["Cost of 1 Bedroom"] = "Room price not available"
    print(public_school_list3)
    if len(public_school_list3) == 0:
        print("There are no schools under that search criteria. Please re-start the screening question process to enter new search criteria. Thank you!")
        quit()
    else:
        print("You will be receiving data on the public universities/colleges that best meet your needs. List of your top schools with data loading...")
        pass


#College Question Tree Structure
CollegeQuestionTree = \
    ("Do you want to obtain a 4 year (i.e. Bachelors) degree, if yes enter 'yes'? If you want a 2 year degree (i.e. associates) enter 'no'",
        ("Do you want to go to a large university with over 15,000 students?",
            (("yes", "yes"), None, None),
            (("yes", "no"), None, None)),
            # (tree_function_4_year("yes"), None, None), #tree[1][1][0] #list comprehension/function
            # (tree_function_4_year("no"), None, None)), #tree[1][2]
        ("Do you want to go to a large community college with over 15,000 students?",
            (("no", "yes"), None, None),
            (("no", "no"), None, None)))
            # (tree_function_CC("yes"), None, None), #tree[2][1]
            # (tree_function_CC("no"), None, None))) #tree[2][2]


if __name__ == "__main__":


    save_college_reponses = call_college_questions(CollegeQuestionTree)
    print(save_college_reponses)
    if save_college_reponses[0] == "yes":
        tree_function_4_year(save_college_reponses[1])
    else:
        tree_function_CC(save_college_reponses[1])



    # tree_function_4_year("Yes") #LA 25 miles
    # # tree_function_CC("yes") #LA 10 miles



    #PLOTLY GRAPHS

    school_names = []
    school_population = []
    school_median_earnings1 = []
    school_netprice = []
    school_names_room =[]
    cost_of_bedroom = []

    for school in public_school_list3:
        school_names.append(school["name"])
        school_population.append(school["Student Population"])
        school_median_earnings1.append(school["Median earnings after graduation"])
        school_netprice.append(school["net_price"])
        if school != "Room price not available":
            school_names_room.append(school["name"])
            cost_of_bedroom.append(school["Cost of 1 Bedroom"])


    #Input school name and student population list
    bar_data = go.Bar(x=school_names, y=school_population)
    basic_layout = go.Layout(title="List of top choice CA public colleges' student populations")
    fig = go.Figure(data=bar_data, layout=basic_layout)
    fig.show()

    # for school in public_school_list3:
    bar_data2 = go.Bar(x=school_names, y=school_median_earnings1)
    basic_layout2 = go.Layout(title="List of top choice CA public colleges' student median earnings after graduation (Earnings in U.S. Dollars)")
    fig2 = go.Figure(data=bar_data2, layout=basic_layout2)

    fig2.show()

    # for school in public_school_list3:
    bar_data3 = go.Bar(x=school_names, y=school_netprice)
    basic_layout3 = go.Layout(title="List of top choice CA public colleges' student cost of attendance based on your financial aid needs (Price in U.S. dollars)")
    fig3 = go.Figure(data=bar_data3, layout=basic_layout3)

    fig3.show()

    # for school in public_school_list3:
    bar_data4 = go.Bar(x=school_names_room, y=cost_of_bedroom)
    basic_layout4 = go.Layout(title="List of top choice CA public colleges' cost of housing for 1 bedroom in the campus area (Price in U.S. dollars)")
    fig4 = go.Figure(data=bar_data4, layout=basic_layout4)

    fig4.show()

# #####################################################################################################################################################
