import time
import pandas as pd
import numpy as np
from collections import Counter

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    while True:
        city = input('\nWould you like to see data for Chicago, New York City or Washington?\n')
        city = city.lower()
        if city not in ('new york city', 'chicago', 'washington'):
            print('\nSorry, I didn\'t catch that. Try again.\n')
            continue
        else:
            print('\nLooks like you want to learn more about {}. if this is incorrect, restart the program\n'.format(city.title())) #capitalises city name
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input('\nSelect one of the following months to see data for: January, February, March, April, May or June?\nPlease enter the full name of the month or "All".\n')
        month = month.lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june','all'):
            print('\nSorry, I didn\'t catch that. Try again.\n')
            continue
        else:
            print('\nOk, so lets filter the data for {}. If this is incorrect, restart the program\n'.format(month.title())) #capitalises city name
            break

        # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nPlease choose which day of the week you\'d like to see the results for Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\nPlease enter the full day of the week or "All".\n')
        day = day.lower()
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print('\nSorry, I didn\'t catch that. Try again.\n')
            continue
        else:
            print('\nOk, so lets filter the data for {}. If this is incorrect, restart the program\n'.format(day.title())) #capitalises city name
        break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of month if applicable
    if day != 'all':

        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = df['month'].mode()[0]
    result = months[popular_month - 1].title()
    print('The most popular month for bike hire is {}'.format(result))

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most popular day for bike hire is {}'.format(popular_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    result = int(popular_hour + 1)
    print('The most popular hour to start bike hire is from {}.00 to {}.00'.format(popular_hour, result))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode().values[0]
    print('The most commonly used Start Station is {}'.format(common_start))

    # display most commonly used end station
    common_fin = df['End Station'].mode().values[0]
    print('The most commonly used End Station is {}'.format(common_fin))

    # display most frequent combination of start station and end station trip
    freq_trip = df[['Start Station', 'End Station']].groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most common trip was:\n {}'.format(freq_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = sum(df['Trip Duration'])
    total_days = int(total_time / 86400)
    total_min = int((total_time - (total_days*86400)) / 3600)
    print('The total travel time was {} days and {} minutes'.format(total_days, total_min))

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    result = int(mean_time / 60)
    print('The average travel time was {} minutes'.format(result))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_subscriber = (df['User Type'].values == 'Subscriber').sum()
    print('{} subscribers used the bike sharing service.'.format(user_subscriber))

    user_customer = (df['User Type'].values == 'Customer').sum()
    print('{} customers used the bike sharing service.'.format(user_customer))

    user_dep = (df['User Type'].values == 'Dependent').sum()
    print('{} dependents used the bike sharing service.'.format(user_dep))

    # Display counts of gender
def gender_stats(df):

    print('\nCalculating Gender Stats...\n')
    start_time = time.time()
    #to prevent error where there is no gender data
    try:
        user_male = (df['Gender'].values == 'Male').sum()
        print('{} users were male'.format(user_male))

        user_female = (df['Gender'].values == 'Female').sum()
        print('{} users were female'.format(user_female))

        user_null = df['Gender'].isnull().sum()
        print('{} users did not report their gender'.format(user_null))
    except:
        print('There is no available gender data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Display earliest, most recent, and most common year of birth
def birth_stats(df):
    print('\nCalculating Birth Stats...\n')
    start_time = time.time()
    #to prevent error where there is no birth data
    try:
        earliest_year = df['Birth Year'].min()
        print('The oldest user was born in {}'.format(int(earliest_year)))

        recent_year = df['Birth Year'].max()
        print('The youngest user was born in {}'.format(int(recent_year)))

        common_year = df['Birth Year'].mode()
        print('The most common year of birth of users was {}'.format(int(common_year)))
    except:
        print('There is no available birth data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df, current_line):
        print('\nShowing raw data...\n')
        start_time = time.time()

        # displays 5 lines of raw data and then prompts to see more until user opts out
        display = input('\nWow that was pretty impressive!\nWould you like to view individual trip data?'
                        ' Type \'yes\' or \'no\'.\n')
        display = display.lower()
        if display == 'yes':
            print(df.iloc[current_line:current_line+5])
            current_line += 5
            return display_data(df, current_line)
        if display == 'no':
            return
        else:
            print('\nSorry, I didn\'t catch that. Try again.\n')
            return display_data(df, current_line)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        gender_stats(df)
        birth_stats(df)

        # Display five lines of data at a time if user specifies that they would like to
        display_data(df, 0)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
