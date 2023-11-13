import requests
from bs4 import BeautifulSoup as soup
import time
import csv
from datetime import datetime, timedelta

fastest_first_names = []
fastest_last_names = []
fastest_race_nums = []
fastest_race_times = []
races = []

def convert_relative_times_to_actual_times(list_of_times):
    actual_times = []
    reference_time = None

    for time_str in list_of_times:
        if 'lap' in time_str or 'DNF' in time_str or 'DNS' in time_str:
            actual_times.append(time_str)  # Keep 'lap' or 'DNF' entries as they are
        elif ':' in time_str:
            # Handle the first time in 'MM:SS.sss' format
            actual_times.append(time_str)
            # Set the reference time for subsequent relative times
            reference_time = datetime.strptime(time_str, '%M:%S.%f').time()
        else:
            # Handle relative times in '+XX.XXXs' format
            if reference_time:
                relative_time = timedelta(seconds=float(time_str.rstrip('s')))
                actual_time = (datetime.min + timedelta(minutes=reference_time.minute, seconds=reference_time.second, microseconds=reference_time.microsecond) + relative_time).time()
                actual_times.append(actual_time.strftime('%M:%S.%f')[:-3])

    return actual_times


def get_page(url):
    page = requests.get(url, headers={
        "User-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"})
    doc = soup(page.content, "html.parser")
    return doc

def get_tbody(race_name, y):
    url = "https://www.formula1.com/en/results.html/"+str(y)+"/races/" + \
        race_name+"/fastest-laps.html"
    
    # url = "https://cis2.stvincent.edu/F1/2022_350_F1/www.formula1.com/en/results.html/"+str(y)+"/races/" + \
    #     race_name+"/fastest-laps.html"
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

def get_sidenav(race_name, y):
    url = f"https://www.formula1.com/en/results.html/{y}/races/{race_name}/race-result.html"
    #url = f"https://cis2.stvincent.edu/F1/2022_350_F1/www.formula1.com/en/results.html/{y}/races/{race_name}/race-result.html"
    response = requests.get(url)
    if response.status_code == 200:
        page = soup(response.content, 'html.parser')
        side_nav_items = page.find_all('li', class_='side-nav-item')
        
        data_values = []  # To store the data values
        
        for item in side_nav_items:
            anchor = item.find('a', class_=['side-nav-item-link ArchiveLink', 'side-nav-item-link ArchiveLink selected'])
            data_value = anchor.get('data-value') if anchor else None  # Get the 'data-value' attribute
            if data_value:
                data_values.append(data_value)
        
        return data_values
    else:
        print(f"Failed to retrieve the web page for {race_name}")
        return []

def fastest_lap(race_name, y):
    tbody = get_tbody(race_name, y)
    first_name = ""
    last_name = ""

    tds = tbody.find_all("td", class_="dark hide-for-mobile")
    for td in tds:
        num = td
        racenum = (num.text)
        
        # If you only want the first number, break out of the loop
        break
    
    
    tds = tbody.find_all("td", class_="dark bold")
    for td in tds:
        names = td.find_all(True, {"class": ["hide-for-tablet", "hide-for-mobile"]})
        if not names:
            continue
        else:
            first_name = names[0].string
            last_name = names[1].string
            # just need first name we find cause we ant fastest lap for each race.
            break
    
    # Find the second time
    if len(tds) > 2:
        fast_time = tds[2].text

    return first_name, last_name, racenum, fast_time  # Include second_time in the return values
    

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


def fastest_lap_csv(race_link, y):
    
    data = list(zip(races * len(fastest_first_names), fastest_first_names, fastest_last_names, fastest_race_nums, convert_relative_times_to_actual_times(fastest_race_times)))
    
    # Define the CSV file name with the year and race name
    csv_filename = f"formula1_fastest_laps_{y}.csv"
    
    # Open the CSV file in append mode
    with open(csv_filename, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        
        # Check if the file is empty, and if so, write the header row
        if csv_file.tell() == 0:
            writer.writerow(["Race Name", "First Name", "Last Name", "Racer Number", "Fastest Time"])
        
        # Write the data
        writer.writerows(data)

    
def get_event_types(race_links, race_name, y):
    eventtypelist = []
    for index in range(1, len(race_links)):
        #print(race_links[index][0])
        race_name = race_links[index][0]
        try:
            eventtypelist.append(get_sidenav(race_name, y))
            first_name, last_name, race_num, fastest_time = fastest_lap(race_name, y)
            fastest_first_names.append(first_name)
            fastest_last_names.append(last_name)
            fastest_race_nums.append(race_num)
            fastest_race_times.append(fastest_time)
            races.append(race_name[5:])
            
            
        except Exception as e:
            print(f"Error while checking race {race_name}: {e}")
            continue

        time.sleep(1)
    return eventtypelist

y = 2023
import raceInfo

url = "https://www.formula1.com/en/results.html/"+str(y)+"/races.html"
#url = f"https://cis2.stvincent.edu/F1/2022_350_F1/www.formula1.com/en/results.html/"+str(y)+"/races.html"
doc = get_page(url)
race_links = get_races(doc)
race_name = get_race_input(race_links, y)

if (race_name == "all"):
    eventlist = get_event_types(race_links, race_name, y)
    fastest_lap_csv(race_links, y)
    
desired_events = ['race-result', 'practice-1', 'practice-2', 'practice-3', 'sprint-results', 'qualifying', 'sprint-shootout']

# Create a dictionary to store lists of indices for each event
event_indices = {event: [] for event in desired_events}

for i, sublist in enumerate(eventlist):
    for event in desired_events:
        if event in sublist:
            event_indices[event].append(i+1)

# Print the lists of indices for each event
for event, indices in event_indices.items():
    print(f"{event} indices: {indices}")


print("\nRace Scrape Starting")
raceInfo.main(race_links, race_name, y, event_indices)
print("\nRace Scrape Finished")

""" 
print("---------------------------------------------------------------------------")
print("Qualifying Scrape Starting\n")

import QualInfo
QualInfo.main(race_links, race_name, y, event_indices)

print("\nQualifying Scrape Finished")
print("---------------------------------------------------------------------------")
print("Sprint Qualifying Scrape Starting\n")

import SprintQualInfo
SprintQualInfo.main(race_links, race_name, y, event_indices)

print("\nSprint Qualifying Scrape Finished")
print("---------------------------------------------------------------------------")
print("Sprint Scrape Starting\n")
import sprintInfo
sprintInfo.main(race_links, race_name, y, event_indices)

print("\nSprint Scrape Finished")
print("---------------------------------------------------------------------------")
print("Practice 1 Scrape Starting\n")

import practiceInfo1
practiceInfo1.main(race_links, race_name, y, event_indices)
print("\nPractice 1 Scrape Finsihed")
print("---------------------------------------------------------------------------")
print("Practice 2 Scrape Starting\n")
import practiceInfo2
practiceInfo2.main(race_links, race_name, y, event_indices)
print("\nPractice 2 Scrape Finsihed")
print("---------------------------------------------------------------------------")
print("Practice 3 Scrape Starting\n")
import practiceInfo3
practiceInfo3.main(race_links, race_name, y, event_indices)
print("Practice 3 Scrape Finsihed\n") """