import time
import sys
import pandas as pd
import numpy as np

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

    # get user input for city (chicago, new york city, washington). 


    try:
        valid_items=['chicago', 'new york city', 'washington']
        while True:
            user_input = input("Please enter city (valid values are: chicago, new york city, washington):\n").lower()
            if user_input in valid_items:
                city = user_input
                break  # Exit the loop if the input is valid
            else:
                print("Invalid input. Please enter a valid city.")

        # get user input for month (all, january, february, ... , june)
        valid_items=['all', 'january', 'february', 'march', 'april', 'may', 'june']
        # user should also have chance to shorten the input values for quicker handling
	valid_shorts=['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']
        while True:
            user_input = input("Please enter month (valid values are: 'all', 'january', 'february', 'march', 'april', 'may', 'june'):\n").lower()
            if user_input in valid_items:
                month = user_input
                break  # Exit the loop if the input is valid
            elif user_input in valid_shorts:
                # find index of input in shorts and select proper month
                user_input = valid_items[valid_shorts.index(user_input)]
                month = user_input
                break  # Exit the loop if the input is valid
            else:
                print("Invalid input. Please enter a valid month.")

	# This is comment change
        # get user input for day of week (all, monday, tuesday, ... sunday)
        valid_items=['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        valid_shorts=['all', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        while True:
            user_input = input("Please enter day (valid values are: 'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'):\n").lower()
            if user_input in valid_items:
                day = user_input
                break  # Exit the loop if the input is valid
            elif user_input in valid_shorts:
                # find index of input in shorts and select proper month
                user_input = valid_items[valid_shorts.index(user_input)]
                day = user_input
                break  # Exit the loop if the input is valid
            else:
                print("Invalid input. Please enter a valid day.")

        print("Input for processing is: (city, month, day) : ({}, {}, {})".format(city, month, day))    
        print('-'*40)
    except:
        print("Needed Input could not be gathered. Please restart script and try again.")    
        sys.exit()
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
    print("load_data start with (city, month, day) : ({}, {}, {})".format(city, month, day))    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] =  df['Start Time'].dt.day_name()
    # filter by month if applicable
    print('load_data File loaded.')
    if month != 'all':
        print('Load_data filter by month start')
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        print('Load_data filter by month finish')

    # filter by day of week if applicable
    if day != 'all':
        print('Load_data filter by day start')
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        print('Load_data filter by day finish')

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print("The most common month is:", popular_month)
 
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("The most common month is:", popular_day)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("The most common hour is:", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most used Start Station is:", df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print("The most used End Station is:", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    station_combinations = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(station_combinations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time is (sec) : ",  df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print("Mean travel time is (sec) : ",  df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User Types Counts are:  ",  df['User Type'].value_counts())

    if city == 'washington':
        # No gender and birth info available for Washington
        print("Sorry. No gender or birth year info are available for Washington.")
    else:
        # TO DO: Display counts of gender
        print("Gender Counts are:  ",  df['Gender'].value_counts())

        # TO DO: Display earliest, most recent, and most common year of birth
        print("Earliest Year of Birth is:  ",  df['Birth Year'].min())
        print("Most recent Year of Birth is:  ",  df['Birth Year'].max())
        print("Most common Year of Birth is:  ",  df['Birth Year'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays chunked content from raw data ."""

    max_count = df.shape[0]
    rec_chunk = 5
    print("\n\nThere are {} rows after rquested filtering. ".format(max_count))
    show_data = input("Would you like to view 5 rows of individual trip data? (Enter 'No' to skip) \n").lower()
    start_loc = 0
    while show_data != 'no':
        print("Show records {} to {} from total {}".format(start_loc,start_loc + rec_chunk, max_count)) 
        print(df.iloc[start_loc:start_loc + rec_chunk])
        start_loc += rec_chunk
        if start_loc == 50:
            # Increase chunk size as user is insisting to see all records
            rec_chunk += 45
        if start_loc >= max_count:
            # If all records are displayed then loop should end automatically
            print("\** Congrats .. you have seen all records. ")
            break
        show_data = input("Do you wish to continue ? (Enter 'No' to Stop) : ").lower()
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Good bye! Wish you a nice time !')
            break


if __name__ == "__main__":
	main()
