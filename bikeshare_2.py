import time
import pandas as pd
import numpy as np

# set up the definitions that are allowed for city, month and day.
# include 'all' where relevant
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get the city
    city = input("Please enter a city: ").lower()
    #check the city entry is ok
    while CITY_DATA.get(city) ==None:
        city = input("City not found.  Please choose Chicago, New York City or Washington: ").lower()


    # get the month
    month = input("Please enter a month: ").lower()

    if month != 'all':
        # check the month entry is ok
        while month not in months :
            month = input("Please enter a month (january, february, march, april, may, june or all): ").lower()


    # get the day of week
    day = input("Please enter a day: ").title()

    #check we have a valid day
    while day not in days :
        day = input("Please enter a day: ").title()


    #city = 'chicago'
    #month = 'all'
    #day = 'all'

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load appropriate csv file
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    #months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by days if needed
    if day != 'All':
        # filter by day to create the new dataframe
        df = df[df['day_of_week'] == day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #additional columns required, calulate these:
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # Display the most common month
    # need to check whether more than one month's data has been loaded.
    # Otherwise, what's the point?

    if df.groupby(['month'])['month'].count().size>1:
        month_common = months[df['month'].mode()[0]-1].title()
        print('The most common month for a trip is: ' + month_common)
    else:
        print('Only data for ' + months[df['month'].iloc[0]-1].title() + ' was loaded')

    # display the most common day of week
    # need to check whether more than one day's data has been loaded.
    # Otherwise, what's the point?

    if df.groupby(['day_of_week'])['day_of_week'].count().size>1:
        day_common = df['day_of_week'].mode()[0]
        print('The most common day of the week for a trip is: ' + day_common)
    else:
        print('Only data for ' + df['day_of_week'].iloc[0].title() + ' was loaded')

    #display the most common start hour
    hour_common = df['hour'].mode()[0]
    # get this into a nice format (am or pm)
    #Calculate the hours
    hour_12_common = hour_common % 12
    # and then am or pm
    if hour_common //12 == 1:
        am_pm = 'pm'
    else:
        am_pm = 'am'
    print('The most common hour for a trip to start is: ' + str(hour_12_common) + am_pm)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Set up the additional column required for start & end stations
    df['Journey'] = df['Start Station'].map(str) + ' to ' + df['End Station']

    #display most commonly used start station
    start_station_common = df['Start Station'].mode()[0]
    start_station_common_count = str(df[df['Start Station']==start_station_common].count()['Start Station'])
    print(start_station_common_count + " trips started from the most popular start station of " + start_station_common+'.')

    # display most commonly used end station
    end_station_common = df['End Station'].mode()[0]
    end_station_common_count = str(df[df['End Station']==end_station_common].count()['End Station'])
    print(end_station_common_count + " trips ended at the most popular end station of " + end_station_common +'.')

    # display most frequent combination of start station and end station trip
    journey_common = df['Journey'].mode()[0]
    journey_common_count = str(df[df['Journey']==journey_common].count()['Journey'])
    print(journey_common_count + " trips were between " + journey_common+ ", which is the most popular journey.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    trip_time_total = df['Trip Duration'].sum()
    print('The total time spent cycling was '+'{:.2f}'.format(trip_time_total) + ' seconds.')
    # and express this in mre useful time units (years, weekes, days, hours, minutes & seconds)
    print('which is: ' + time_text(trip_time_total)+'.')

    # display mean travel time
    trip_time_mean = df['Trip Duration'].mean()
    print('\nThe average time per trip was ' + '{:.2f}'.format(trip_time_mean) +' seconds.')
    # and express this in mre useful time units (years, weekes, days, hours, minutes & seconds)
    print('which is: ' + time_text(trip_time_mean)+'.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # user type statistics
    #check to see if user type data are available (use try)
    # and build up a string of the user types
    try:
        user_type_count= df.groupby(['User Type'])['User Type'].count()
        print_text = 'Trips were made by ' + str(user_type_count[0]) + ' ' + str(user_type_count.index[0])
        if user_type_count.size > 2:
            for count in range(user_type_count.size-2):
                print_text = print_text + ', ' +  str(user_type_count[count+1]) + ' ' + str(user_type_count.index[count+1])
        if user_type_count.size > 1:
            print_text = print_text + ' and ' +  str(user_type_count[user_type_count.size-1]) + ' ' + str(user_type_count.index[user_type_count.size-1])

        print_text = print_text + ' user types'
        print(print_text)
        #and figure out if there was any missing data
        missing_values = df.shape[0] - df['User Type'].count()
        if missing_values > 0:
            print(str(missing_values) + ' trips had no user type data.')
    except:
        print('No user types data exists.')

    #Display counts of gender
    #first chack data are available
    # and build up a string of the genders
    try:
        gender_count= df.groupby(['Gender'])['Gender'].count()
        print_text = 'Trips were made by ' + str(gender_count[0]) + ' ' + str(gender_count.index[0])
        if gender_count.size > 2:
            for count in range(gender_count.size-2):
                print_text = print_text + ', ' +  str(gender_count[count+1]) + ' ' + str(gender_count.index[count+1])

        if gender_count.size > 1:
            print_text = print_text + ' and ' +  str(gender_count[gender_count.size-1]) + ' ' + str(gender_count.index[gender_count.size-1])

        print_text = print_text + ' users.'
        print(print_text)
        #and figure out if there was any missing data
        missing_values = df.shape[0] - df['Gender'].count()
        if missing_values > 0:
            print(str(missing_values) + ' trips had no gender data.')
    except:
        print('No gender data exists.')




    # Display earliest, most recent, and most common year of birth
    # And chacj=k the year of birth data exist
    # and build up a string of for the birth years
    try:
        birth_year_min = int(df['Birth Year'].min())
        birth_year_max = int(df['Birth Year'].max())

        print('Trips were taken by people born between ' + str(int(birth_year_min)) +' and ' + str(int(birth_year_max)))
        mode_value, mode_string = mode_ties(df, 'Birth Year')
        print(mode_string + ' was the most common year of birth, with '+ str(mode_value) +' trips being taken by people born in this year')
        #and figure out if there was any missing data
        missing_values = df.shape[0] - df['Birth Year'].count()
        if missing_values > 0:
            print(str(missing_values) + ' trips had no year of birth data.')
    except:
        print('No year of birth data exists.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_data(df):
    # ask the user if they would like to see some data
    get_data= input("Would you like to see 5 rows of data?  Answer yes or no. \n").lower()
    if get_data == 'yes':
        print(df.head())
        count = 0
        # check whether to show more data
        while get_data == 'yes':
            get_data = input("Would you like to see the next 5 rows of data?    Answer yes or no. \n").lower()
            if get_data == 'yes':
                count = count+1
                print(df[count*5:].head())




def mode_ties(df, column_name):
    """
    Takes a dataframe and column name and finds the mode
    Deals with more than one row being returned (i.e. ties)

    Args:
        df - dataframe
        column_name (str) - the name of teh column to be used
    Returns:
        mode_value - the value of the mode
        mode_string - the factors that constitute the mode (and deals with ties)
    """

    mode_data = df[column_name].mode()
    mode_value = df[df[column_name]==mode_data[0]].count()[column_name]
    mode_count = mode_data.size
    mode_string = str(df[column_name].mode()[0])

    if mode_count > 1:
        for count in range(mode_count-1):
            mode_string = mode_string + ', ' + str(mode_data[count+1])


    return mode_value, mode_string



def time_text(time_seconds):
    """
    takes a time in seconds and returns a string with the time broken down as follows:
    years, weeks, days, hours and seconds
    (assumes 365 days in a year)

    Args:
        (float) time_sconds - the time in seconds to be processed

    Returns:
        (str) time_string
    """

    # define useful time units in seconds (makes code easier to follow)
    min_sec = 60
    hour_sec = min_sec*60
    day_sec = hour_sec*24
    week_sec = day_sec *7
    year_sec = day_sec * 365
    time_string = ''

    # build the text up sequentially, showing the total number of seconds in more intuitive time units
    if time_seconds > year_sec:
        time_string = time_string + str(time_seconds//year_sec) + ' year(s), '
        time_seconds = time_seconds % year_sec

    if time_seconds > week_sec:
        time_string = time_string + str(time_seconds//week_sec) + ' weeks(s), '
        time_seconds = time_seconds % week_sec

    if time_seconds > day_sec:
        time_string = time_string + str(time_seconds//day_sec) + ' day(s), '
        time_seconds = time_seconds % day_sec

    if time_seconds > hour_sec:
        time_string = time_string + str(time_seconds//hour_sec) + ' hour(s), '
        time_seconds = time_seconds % hour_sec

    if time_seconds > min_sec:
        time_string = time_string + str(time_seconds//min_sec) + ' minutes(s) and '
        time_seconds = time_seconds % min_sec

    # show the seconds to 2 decimal places - acceptable accuracy in this context and easy on the eye
    time_string = time_string + "{:.2f}".format(time_seconds) + ' second(s)'
    return time_string



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
