import pandas as pd
import csv

monthsDays = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
months = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}

def get_month():
    """Gets the month from the user"""
    m = "0"

    # Ensures a good month is inputted and no letters
    while int(m) < 1 or int(m) > 12:
        try:
            m = input("Month(1-12): ")
        except:
            print("Please enter a number between 1-12")

    # Website requires a 0 in front of months below 10
    if int(m) < 10:
        m = "0" + m

    return m

def get_year():
    """Gets the year from the user"""
    y ="0"

    # Ensures a good year is inputted and no letters
    while int(y) < 2005 or int(y) > 2022:
        try:
            y = input("\nYear(2005-2022): ")
        except:
            print("Please enter a number between 2005-2022")

    return y

def setup_link(month, year):
    """Sets up the link for the webpage"""
    link = f"https://www.estesparkweather.net/archive_reports.php?date={year + month}"
    return link

def save_csv(output):
    """Saves the output to a csv file"""
    with open('weather.csv', 'a') as cv:
        cv.write("\n")
        for key in output.keys():
            cv.write("%s, %s\n" % (key, output[key]))

def reset_csv():
    """Deletes everything in csv file"""
    choice = input("\nAre you sure you wish to delete all weather reports so far? (Y,N)\nchoice: ")
    if choice == "Y" or choice == "y":
        with open('weather.csv', 'w') as cv:
            cv.write("")

    main()

def view_reports():
    """Prints all current reports"""
    try:
        pd.read_csv('weather.csv')
        with open('weather.csv', 'r') as cv:
            for line in cv:
                print(line, end="")
    except:
        print("\nThere are weather reports to view")

    main()

def read_weather(days, month):
    """Reads the weather and returns the hottest and coldest days"""
    hottest_day = -999
    coldest_day = 999
    temp = 0

    for i in range(monthsDays[month]):
        temp = days[i][1][1]
        temp = float(temp[:(len(temp) - 2)])
        if temp > hottest_day:
            hottest_day = temp
        if temp < coldest_day:
            coldest_day = temp
        
    return hottest_day, coldest_day

def find_average(days):
    """Gets the average temperature for the month"""
    for day in days:
        if "Average and Extremes" in day[0][0]:
            return day[1][1]
    return 0

def weather():
    """Runs the main weather getter"""
    year = get_year()
    month = get_month()

    df = pd.read_html(setup_link(month, year))

    month = int(month)

    if len(df) >= monthsDays[month]:
        hottest_day, coldest_day = read_weather(df, month)
        average_day = find_average(df)
        output = (f"\nHigh, Low, and Average For {months[month]}\nHottest: {hottest_day}{chr(176)}F\nColdest: {coldest_day}{chr(176)}F\nAverage: {average_day}")
        save_output = {"Month": month,
                        "Year": year,
                        "High": hottest_day,
                        "low": coldest_day,
                        "Average": average_day[:(len(average_day) - 2)]}
        print(output)
        save_csv(save_output)
    else:
        print("There is not enough data for that weather page")

    main()

def main():
    """Main function to guide the program"""
    choice = 0
    done = False
    while not done:
        while (choice < 1 or choice > 4):
            try:
                print("\nWeather for Estes Park, Colorado")
                choice = int(input("Would you like to:\n1.Create Weather Report\n2.View Weather Reports\n3.Delete Weather Reports\n4.Quit\nchoice: "))
            except:
                print("\nPlease enter a number between 1-4")
            
        match(choice):
            case 1:
                weather()
                break
            case 2:
                view_reports()
                break
            case 3:
                reset_csv()
                break
            case 4:
                done = True
                break
        choice = 1

if __name__ == "__main__":
    main()