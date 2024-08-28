
import datetime 
import math

def open_file(file_path):
    """Opens a file and returns a list of lists, where each list is a line of the file.
    Drops the heading of the file, turns the version column into an integer, and turns 
    the datetime column into a datetime object."""
    with open(file_path, 'r') as file:
        data = file.readlines()[1:]
    
    split_data = [string.strip().split('\t') for string in data] # Split the data into a list of lists

    for i in range(len(split_data)):
        split_data[i][3] = int(split_data[i][3]) # Turn the version column into an integer
        split_data[i][1] = datetime.datetime.strptime(split_data[i][1], "%Y-%m-%d %H:%M:%S") # Turn the datetime column into a datetime object
    
    return split_data # Return the data


def preprocess_data(data):
    """Preprocesses the data to create a dictionary that maps each username to a list of relevant dates,
    in order to calculate seniority."""
    username_dates = {} # Create a dictionary to store the usernames and dates
    
    for row in data:
        username = row[4]
        date = row[1]
        if username not in username_dates:
            username_dates[username] = []
        username_dates[username].append(date)
    
    return username_dates


def calculate_seniority(username, date, username_dates):
    """Calculates the seniority of a user after a specific date using the preprocessed username dates."""
    if username in username_dates:
        count = sum(1 for d in username_dates[username] if d < date)
        if count > 0:
            seniority = math.log10(count)
            return seniority

    return 0


def make_network_data(data):
    """Creates a network as a list of dictionaries, where each dictionary is a revert. Each dictionary contains the 
    username of the reverter and the reverted user, the timestamp of the revert, and the seniority of both users.
    Returns the data, as well as the number of edges and nodes in the network."""
    username_dates = preprocess_data(data)
    network_data = [] # Create a list to store the network data
    
    for i in range(len(data)):
        is_revert = data[i][2]
        version = data[i][3]
        username = data[i][4]

        if is_revert == '1' and i + 1 < len(data) and version != data[i + 1][3]: 
            j = i + 1
            while j < len(data) and data[j][3] != version:
                j += 1
            if j < len(data) and data[j-1][4] != username:
                reverter_seniority = calculate_seniority(username, data[i][1], username_dates)
                reverted_user_seniority = calculate_seniority(data[j-1][4], data[j-1][1], username_dates)
                revert_data = { 
                    'reverter': username,
                    'reverted_user': data[j-1][4],
                    'datetime': data[i][1],
                    'reverter_seniority': reverter_seniority,
                    'reverted_user_seniority': reverted_user_seniority
                }
                network_data.append(revert_data)

    usernames = set() # Create a set to store the usernames (nodes)
    for d in network_data:
        usernames.add(d['reverter']) # Add the reverter and reverted user to the set
        usernames.add(d['reverted_user'])
    
    num_edges = len(network_data) # Calculate the number of edges
    num_nodes = len(usernames) # Calculate the number of nodes
    
    return network_data, f"There are {str(num_edges)} edges and {str(num_nodes)} nodes in the network."