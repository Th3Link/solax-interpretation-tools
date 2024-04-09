import json
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

# Mapping of German month names to English month names
month_mapping = {
    "Jan": "Jan",
    "Feb": "Feb",
    "Mär": "Mar",  # Mär -> Mar
    "Apr": "Apr",
    "Mai": "May",  # Mai -> May
    "Jun": "Jun",
    "Jul": "Jul",
    "Aug": "Aug",
    "Sep": "Sep",
    "Okt": "Oct",  # Okt -> Oct
    "Nov": "Nov",
    "Dez": "Dec"   # Dez -> Dec
}

# Mapping of German days of the week to English days of the week
day_mapping = {
    "Mo": "Mon",
    "Di": "Tue",
    "Mi": "Wed",
    "Do": "Thu",
    "Fr": "Fri",
    "Sa": "Sat",
    "So": "Sun"
}

def plot_data(timestamps, data_dict, keys):
    plt.figure(figsize=(10, 6))
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Data Plot')

    for key in keys:
        plt.plot(timestamps, data_dict[key], label=key)

    plt.legend()
    plt.show()

def plot_data_subplots(timestamps, data_dict, keys):
    num_plots = len(keys)
    fig, axs = plt.subplots(num_plots, 1, figsize=(10, 9 * num_plots))
    fig.suptitle('Data Plots')

    for i, key in enumerate(keys):
        ax = axs[i] if num_plots > 1 else axs
        ax.plot(timestamps, data_dict[key], label=key)
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.set_title(f'{key} Plot')
        ax.legend()

    plt.tight_layout()
    plt.show()

def analyze_data(data):
    # Identify missing data points
    missing_indices = [index for index, value in data_guesses.items() if data[index] == value]
    return missing_indices
    
def load_samples(filepath):
    timestamps = []
    value_dict = {}

    with open(filepath, 'r') as file:
        for line in file:
            # Find the index of the last closing curly brace
            last_brace_index = line.rfind('}')

            # Extract JSON object
            json_data = json.loads(line[:last_brace_index + 1].strip())

            # Extract date from the line
            date_str = line[last_brace_index + 1:].strip()

            # Convert German month names to English
            for ger_month, eng_month in month_mapping.items():
                date_str = date_str.replace(ger_month, eng_month)

            # Convert German days of the week to English
            for ger_day, eng_day in day_mapping.items():
                date_str = date_str.replace(ger_day, eng_day)

            # Parse the date string into a datetime object
            timestamps.append(datetime.strptime(date_str, "%a %d. %b %H:%M:%S %Z %Y"))

            # Iterate through each value in json_data['Data']
            for idx, value in enumerate(json_data['Data']):
                if value > 32768:
                    value -= 65536
                if idx not in value_dict:
                    value_dict[idx] = []
                value_dict[idx].append(value)
        print("loaded {} samples from json".format(len(value_dict[0])))
        print("measures count: {}".format(len(value_dict)))
    return timestamps, value_dict


def load_excel(filepath):
    # Read the Excel file into a pandas DataFrame, skipping the first four rows which contain metadata
    df = pd.read_excel(filepath, skiprows=4)
    
    # Extract the timestamps and measurements
    timestamps = []
    measurements = {col: [] for col in df.columns[1:]}

    for index, row in df.iterrows():
        # Extract timestamp from column A
        timestamp_str = row[df.columns[0]]
        if isinstance(timestamp_str, str):
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        elif isinstance(timestamp_str, pd.Timestamp):
            timestamp = timestamp_str.to_pydatetime()
        timestamps.append(timestamp)
        
        # Extract measurements from columns B to W
        for col in df.columns[1:]:
            measurements[col].append(row[col])
    return timestamps, measurements

def remove_zero_measurements(measurements):
    non_zero_measurements = {}
    
    for col, values in measurements.items():
        all_zero = all(value == 0 for value in values)
        if not all_zero:
            non_zero_measurements[col] = values
            
    return non_zero_measurements

def remove_extreme_measurements(measurements):
    filtered_measurements = {}

    for col, values in measurements.items():
        extreme_values = any(value < 9 or value > 45 for value in values)
        if not extreme_values:
            filtered_measurements[col] = values

    return filtered_measurements

def keep_three_values(dictionary):
    filtered_dict = {key: value for key, value in dictionary.items() if len(set(value)) >= 3}
    return filtered_dict

def filter_keys(dictionary, keys_to_keep):
    filtered_dict = {key: value for key, value in dictionary.items() if key in keys_to_keep}
    return filtered_dict

def remove_keys(dictionary, keys_to_remove):
    filtered_dict = {key: value for key, value in dictionary.items() if key not in keys_to_remove}
    return filtered_dict

def datetime_to_timestamps(datetime_list):
    return [int(dt.timestamp()) for dt in datetime_list]

def timestamps_to_datetime(timestamps):
    return [datetime.fromtimestamp(ts) for ts in timestamps]

def interpolate_measurements(timestamps1, measurements1, timestamps2, measurements2):
    # Find the intersection of timestamps
    timestamps1_int = datetime_to_timestamps(timestamps1)
    timestamps2_int = datetime_to_timestamps(timestamps2)

    # Find the range of timestamps common to both sets
    min_timestamp = max(min(timestamps1_int), min(timestamps2_int))
    max_timestamp = min(max(timestamps1_int), max(timestamps2_int))
    intersection = [ts for ts in timestamps1_int if min_timestamp <= ts <= max_timestamp]

    # Interpolate measurements1 to match timestamps2
    interp_func1 = interp1d(timestamps1_int, measurements1, kind='linear', fill_value="extrapolate")
    interpolated_measurements1 = interp_func1(intersection)

    # Interpolate measurements2 to match timestamps1
    interp_func2 = interp1d(timestamps2_int, measurements2, kind='linear', fill_value="extrapolate")
    interpolated_measurements2 = interp_func2(intersection)

    return intersection, interpolated_measurements1, interpolated_measurements2

def compare_sequences(measurements1, measurements2):
    # Convert measurements to numpy arrays
    
    arr1 = np.array(measurements1)
    arr2 = np.array(measurements2)
    
    correlation_coefficient = 0
    if np.var(arr1) == 0 and np.var(arr2) == 0:
        correlation_coefficient = 1.0
    elif np.var(arr1) == 0 or np.var(arr2) == 0:
        correlation_coefficient = 0
    else:
        # Compute the correlation coefficient between the two sequences
        correlation_coefficient = np.corrcoef(arr1, arr2)[0, 1]

    # Filter out pairs where one of the values is zero
    non_zero_indices = np.logical_and(arr1 != 0, arr2 != 0)
    arr1_filtered = arr1[non_zero_indices]
    arr2_filtered = arr2[non_zero_indices]

    # Compute the scaling factor
    mean_ratio = 1.0
    median_ratio = 1.0
    if len(arr1_filtered) != 0 and len(arr2_filtered) != 0:
        mean_ratio = np.mean(arr1_filtered) / np.mean(arr2_filtered)
        median_ratio = np.median(arr1_filtered) / np.median(arr2_filtered)

    return correlation_coefficient, mean_ratio, median_ratio

def compare_all_sequences(timestamps1, measurements1, timestamps2, measurements2):
    comparison_results = {}

    for key1, values1 in measurements1.items():
        for key2, values2 in measurements2.items():
            if all(isinstance(value, (int, float)) for value in values1) and all(isinstance(value, (int, float)) for value in values2):               
                # Interpolate measurements to match timestamps
                timestamps, interpolated_values1, interpolated_values2 = interpolate_measurements(timestamps1, values1, timestamps2, values2)
                
                # Compare sequences
                correlation_coefficient, mean_ratio, median_ratio = compare_sequences(interpolated_values1, interpolated_values2)
                
                # Store the comparison results
                comparison_results.setdefault(key1, []).append({
                    "key": key2,
                    "correlation_coefficient": correlation_coefficient,
                    "mean_ratio": mean_ratio,
                    "median_ratio": median_ratio,
                    "values1": interpolated_values1,
                    "values2": interpolated_values2,
                    "timestamps": timestamps_to_datetime(timestamps)})

    # Sort the results by correlation coefficient
    for key in comparison_results:
        comparison_results[key] = sorted(comparison_results[key], key=lambda x: x['correlation_coefficient'], reverse=True)

    return comparison_results

def plot_comparison_results(names, comparisons_dict, factor=1):
    names_in_dict = [name for name in names if name in comparisons_dict]
    num_plots = len(names_in_dict)
    num_rows = num_plots
    fig, axs = plt.subplots(num_rows, 1, figsize=(15, 8 * num_plots))
    fig.suptitle('Comparison Results', y=0.99)

    for i, name in enumerate(names_in_dict):
        comparisons = comparisons_dict[name]
        ax = axs[i] if num_rows > 1 else axs
        ax.set_title(f"Comparison of {name}")

        # Plot the comparator measurement
        ax.plot(comparisons[0]['timestamps'], comparisons[0]['values1']*factor, label="Comparator", color='black')

        # Plot comparison measurements
        for comp in comparisons[0:10]:
            ax.plot(
                comp['timestamps'],
                comp['values2'],
                label=f"{comp['key']} (Corr: {comp['correlation_coefficient']:.2f}, Factor:{comp['mean_ratio']:.4f}/{comp['median_ratio']:.4f})", alpha=0.7)

        ax.set_xlabel("Time")
        ax.set_ylabel("Value")
        ax.legend()
        ax.grid(True)

    plt.tight_layout(pad=8)
    plt.show()
