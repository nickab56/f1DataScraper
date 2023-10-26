from numpy import empty
import requests
from bs4 import BeautifulSoup as soup
import time
import csv
from datetime import datetime, timedelta

# Define the CSV file name
csv_filename = "formula1_race_results.csv"


def get_page(url):
    page = requests.get(url, headers={
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    doc = soup(page.content, "html.parser")
    return doc


def get_tbody(race_name, y):
    url = "https://www.formula1.com/en/results.html/"+str(y)+"/races/" + \
        race_name+"/race-result.html"
    doc = get_page(url)
    site_wrapper = doc.find(class_="site-wrapper")
    main = site_wrapper.find(class_="template template-resultsarchive")
    inner_class = main.find(class_="inner-wrap ResultArchiveWrapper")
    result_archive = inner_class.find(class_="ResultArchiveContainer")
    results_archive_wrapper = result_archive.find(
        class_="resultsarchive-wrapper")
    content = results_archive_wrapper.table
    tbody = content.tbody
    return tbody


def get_races(doc):
    main = doc.main
    article = main.article
    container = article.find(class_="resultsarchive-filter-container")
    rarchive1 = container.find(
        class_="resultsarchive-filter-wrap")
    rarchive2 = rarchive1.find_next(class_="resultsarchive-filter-wrap")
    rarchive3 = rarchive2.find_next(class_="resultsarchive-filter-wrap")
    lis = rarchive3.find_all("li", class_="resultsarchive-filter-item")
    race_links = []                                 # bunu dict ile yapmaya calis
    for li in lis:
        race_links.append([item["data-value"]
                           for item in li.find_all() if "data-value" in item.attrs])
    return race_links


def get_input():
    year = []
    ipt = input("What year do you want?\nIf multiple, seperate with comma.\n")
    ipt = ipt.split(",")
    if len(ipt) > 1:
        while int(ipt[0]) < 1950 or int(ipt[1]) > 2022:
            ipt = input(
                "No such year. Dates should be given between 1950 and 2022.\n")
            ipt = ipt.split(",")
        for y in range(int(ipt[0]), int(ipt[1])+1):
            year.append(y)
    else:
        # while int(ipt[0]) < 1950 or int(ipt[0]) > 2022:
        #     ipt = input(
        #         "No such year. Dates should be given between 1950 and 2022.\n")
        #     ipt = ipt.split(",")
        year.append(int(ipt[0]))
    return year


def get_race_input(races, y):
    print("These are the races of", y,
          "select the race you want by typing number of it.")

    for i in range(len(races)):
        print(i, "-", races[i][0].strip("-/1234567890"))
    ipt = input("Enter: ")
    while int(ipt) > len(races):
        ipt = input("Get your shit together and try again: ")
    # print("selected:", races[int(ipt)])
    if int(ipt) == 0:
        return "all"
    else:
        return races[int(ipt)][0]


def get_driver_name(tbody):
    list_of_first_names = []
    list_of_last_names = []
    tds = tbody.find_all("td", class_="dark bold")
    for td in tds:
        names = td.find_all(
            True, {"class": ["hide-for-tablet", "hide-for-mobile"]})
        if not names:
            continue
        else:
            firstName = names[0].string
            lastName = names[1].string 
            #name = names[0].string + " " + names[1].string
            list_of_first_names.append(firstName)
            list_of_last_names.append(lastName)
    return list_of_first_names, list_of_last_names


def get_team_name(tbody):
    list_of_teams = []
    tds = tbody.find_all("td", class_="semi-bold uppercase hide-for-tablet")
    for td in tds:
        list_of_teams.append(td.text)
    return list_of_teams


def get_laps(tbody):
    list_of_completed_laps = []
    tds = tbody.find_all("td", class_="bold hide-for-mobile")
    for td in tds:
        list_of_completed_laps.append(td.text)
    return list_of_completed_laps

def convert_relative_times_to_actual_times(list_of_times):
    actual_times = []
    reference_time = None

    for time_str in list_of_times:
        if 'lap' in time_str or 'DNF' in time_str or 'DNS' in time_str:
            actual_times.append(time_str)  # Keep 'lap' or 'DNF' entries as they are
        elif ':' in time_str:
            # Handle the first time in 'HH:MM:SS.sss' format
            actual_times.append(time_str)
            # Set the reference time for subsequent relative times
            reference_time = datetime.strptime(time_str, '%H:%M:%S.%f').time()
        else:
            # Handle relative times in '+XX.XXXs' format
            if reference_time:
                relative_time = timedelta(seconds=float(time_str.rstrip('s')))
                actual_time = (datetime.min + timedelta(hours=reference_time.hour, minutes=reference_time.minute, seconds=reference_time.second, microseconds=reference_time.microsecond) + relative_time).time()
                actual_times.append(actual_time.strftime('%H:%M:%S.%f')[:-3])

    return actual_times


def get_times(tbody):
    list_of_times = []
    tds = tbody.find_all("td", class_="bold hide-for-mobile")
    for td in tds:
        time = td.find_next(class_="dark bold")
        list_of_times.append(time.text)
    return convert_relative_times_to_actual_times(list_of_times)


def get_points(tbody):
    list_of_points = []
    tds = tbody.find_all(lambda tag: tag.name ==
                         "td" and tag["class"] == ["bold"])
    for td in tds:
        list_of_points.append(td.text)
    return list_of_points

def get_race_num(tbody):
    list_of_racenums = []
    tds = tbody.find_all("td", class_="dark hide-for-mobile")
    for td in tds:
        num = td
        list_of_racenums.append(num.text)
    return list_of_racenums

def makecsv(data, race_name, y):
    
    # Define the CSV file name with the year and race name
    csv_filename = f"formula1_results_race_{y}.csv"
    
    # Open the CSV file in append mode
    with open(csv_filename, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Check if the file is empty, and if so, write the header row
        if csv_file.tell() == 0:
            writer.writerow(["Year", "Race Name", "Position", "First Name", "Last Name", "Racer Number", "Team", "Points", "Laps Completed", "Time"])
        
        # Write the data
        writer.writerows(data)

    print(f"Data for {race_name} in year {y} has been appended to {csv_filename}")


def main(race_links, race_name, y, event_indices):
    print("Scraping year", y)
    if race_name == "all":
        for index in range(1, len(race_links)):
            print(race_links[index][0])
            race_name = race_links[index][0]
            if index in event_indices.get('race-result', []):
                try:
                    tbody = get_tbody(race_name, y)
                    firstnames, lastnames = get_driver_name(tbody)
                    team = get_team_name(tbody)
                    completed_laps = get_laps(tbody)
                    times = get_times(tbody)
                    points = get_points(tbody)
                    racenumber = get_race_num(tbody)
                    race_name = race_name[5:]
        
                    # Generate positions and combine data into a list of lists with "Laps Completed" after "Points"
                    positions = list(range(1, len(firstnames) + 1))  # Positions are 1-based
                    data = list(zip([y] * len(firstnames), [race_name] * len(firstnames), positions, firstnames, lastnames, racenumber, team, points, completed_laps, times))
        
                    # Append data to the CSV file
                    makecsv(data, race_name, y)
                    
                except Exception as e:
                    print(f"Error while processing race {race_name}: {e}")
                    continue
        
                time.sleep(1)
            else:
                print("\n" + race_name + " does not have race result")
    else:
        print(race_name)
        tbody = get_tbody(race_name, y)
        firstnames, lastnames = get_driver_name(tbody)
        team = get_team_name(tbody)
        completed_laps = get_laps(tbody)
        times = get_times(tbody)
        points = get_points(tbody)
        racenumber = get_race_num(tbody)
        
        # Generate positions and combine data into a list of lists with "Laps Completed" after "Points"
        positions = list(range(1, len(firstnames) + 1))  # Positions are 1-based
        data = list(zip([y] * len(firstnames), [race_name] * len(firstnames), positions, firstnames, lastnames, racenumber, team, points, completed_laps, times))
        

        #data = list(zip(positions, firstnames, lastnames, points, completed_laps, team, times))
        
        makecsv(data,race_name, y)
        

    print("Done")

