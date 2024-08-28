import datetime
import matplotlib.pyplot as plt
import numpy as np


def count_ab_ba_events(data):
    """Counts the number of AB-BA event sequences in the network data, 
    and returns the count and the edges in the sequences."""
    ab_ba_counter = 0
    ab_ba_events = []  # List to store the events in AB-BA event sequences

    # Sort the data list by datetime
    data.sort(key=lambda x: x['datetime'])

    for i in range(len(data)):
        initial_reverter = data[i]['reverter']
        initial_reverted_user = data[i]['reverted_user']
        initial_datetime = data[i]['datetime']
        ba_response_found = False  # Flag to track if BA response is found

        for j in range(i+1, len(data)):
            reverter = data[j]['reverter']
            reverted_user = data[j]['reverted_user']

            if initial_reverter == reverted_user and initial_reverted_user == reverter:
                if initial_datetime < data[j]['datetime'] <= initial_datetime + datetime.timedelta(hours=24):
                    if not ba_response_found:
                        ab_ba_counter += 1
                        ba_response_found = True
                        break # Exit the inner loop to prevent the code from running unnecessarily

                    ab_ba_events.append(data[j])  # Store the event in the AB-BA event sequence

        if ba_response_found:
            ab_ba_events.append(data[i])  # Store the initial AB event in the AB-BA event sequence

    return f"There are " + str(ab_ba_counter) + " AB-BA event sequences", ab_ba_events


def separate_abba(data, abba_events):
    """Separates the data into edges involved in AB-BA event sequences and edges not involved in AB-BA events."""
    abba_edges = [] # List to store the edges involved in AB-BA event sequences
    non_abba_edges = [] # List to store the edges not involved in AB-BA event sequences

    for edge in data:
        if edge in abba_events:
            abba_edges.append(edge)
        else:
            non_abba_edges.append(edge)

    return abba_edges, non_abba_edges


def abs_seniority_diff(data):
    """Calculates the absolute seniority difference for each row in the given data.
    Returns a list of the differences."""
    differences = [] # List to store the differences

    for row in data:
        reverter_seniority = row['reverter_seniority']
        reverted_user_seniority = row['reverted_user_seniority']
        difference = abs(reverter_seniority - reverted_user_seniority) # Calculate the absolute difference
        differences.append(difference)

    return differences


def plot_histograms(abba_diff, other_diff):
    """Plots two distributions of absolute seniority difference on the same histogram with overlapping bars."""
    plt.hist(abba_diff, bins=10, alpha=0.7, label='AB-BA', histtype='stepfilled', density=True) # Plot the AB-BA distribution
    plt.hist(other_diff, bins=10, alpha=0.5, label='Other', histtype='step', density=True) # Plot the non-AB-BA distribution
    plt.legend(loc='upper right') # Add a legend
    plt.title('Histograms of Absolute Seniority Difference in AB-BA and non-AB-BA edges') # Add a title
    plt.xlabel('Absolute Seniority Difference') # Add x-axis label
    plt.ylabel('Density') # Add y-axis label
    plt.show() # Display the plot


def mean_diff(abba_diff, other_diff):
    """Calculates the mean absolute seniority difference for editors in AB-BA events and not in AB-BA events."""
    abba_mean = np.mean(abba_diff)
    other_mean = np.mean(other_diff)
    
    return f"The mean absolute seniority difference for editors in AB-BA events is {abba_mean}\n" \
       f"The mean absolute seniority difference for editors not in AB-BA events is {other_mean}"
