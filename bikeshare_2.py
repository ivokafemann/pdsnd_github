import time
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 500)

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

city_options = list(CITY_DATA.keys())
timefilter_options = ['month', 'day', 'both', 'none']
month_options = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_options = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            city = city_options[city_options.index(input('\nPlease enter the city (Chicago, New York City or Washington) you would like to analyse: ').lower())]
            timefilter = timefilter_options[timefilter_options.index(input('\nWould you like to filter the data by month, day, both, or not at all? Type "none" for no time filter: ').lower())]
            if timefilter == 'month':
                month = month_options[month_options.index(input('\nPlease enter the month (January, ..., June) you want to filter by: ').lower())]
                day = day_options[day_options.index('all')]
                break
            elif timefilter == 'day':
                month = month_options[month_options.index('all')]
                day = day_options[day_options.index(input('\nPlease enter the day (Monday, ..., Sunday) you want to filter by: ').lower())]
                break
            elif timefilter == 'both':
                month = month_options[month_options.index(input('\nPlease enter the month (January, ..., June) you want to filter by: ').lower())]
                day = day_options[day_options.index(input('\nPlease enter the day (Monday, ..., Sunday) you want to filter by: ').lower())]
                break
            elif timefilter == 'none':
                month = month_options[month_options.index('all')]
                day = day_options[day_options.index('all')]
                break

        except ValueError:
            print("\nWe detected a flaw (e.g. misspelling, input not in data base). Please enter the input again: ")


    print('-'*40)
    print("Your selected filters:\ncity filter: ", city.title(), "\nmonth filter: ", month.title(), "\nday filter: ", day.title())
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and start hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mode_month = df['month'].mode()[0]
    print('The most popular month is:', month_options[mode_month - 1].title())

    # display the most common day of week
    mode_weekday = df['day_of_week'].mode()[0]
    print('The most popular day of week is:', mode_weekday)

    # display the most common start hour
    mode_start_hour = df['hour'].mode()[0]
    print('The most popular starting time is: {}:00'.format(mode_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mode_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', mode_start)

    # display most commonly used end station
    mode_end = df['End Station'].mode()[0]
    print('The most commonly used end station is:', mode_end)

    # display most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + ' + ' + df['End Station']
    mode_start_end = df['Start and End Station'].mode()[0]
    print('The most frequent combination of start station and end station trip is:', mode_start_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    def conversion(time):
        a=str(time//3600)
        b=str((time%3600)//60)
        c=str((time%3600)%60)
        d=["{} hours {} mins {} seconds".format(a, b, c)]
        return d

    # display total travel time
    print('\nThe TOTAL travel time for the selected data frame was: {}'.format(conversion(total_travel_time)))

    # display mean travel time
    print('\nThe AVERAGE travel time for the selected data frame was: {}'.format(conversion(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print('Counts of User Types\n',user_count)

    if city != 'washington':

        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print('\nCounts of Gender\n',gender_count)

        # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        recent_birth = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('\nYear of Birth Statistics\nEarlieset: {}\nMost Recent: {}\nMost Common: {}'.format(earliest_birth, recent_birth, common_birth))

    else:
        print('\nThere are no statistics on Gender and Birth Year available for Washington.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def individual_data(df):
    """Displays the items of the first 5 rows of the data frame defined by the get_filters function."""
    """Asks if the user wants to see 5 more rows of data until the input is "no"."""

    count = 0
    while True:
        print(df[count:(count+5)])
        count += 5
        restart = input('\nWould you like to see five more rows of individual data? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
