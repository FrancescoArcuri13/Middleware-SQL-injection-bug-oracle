import os
import random
import string
import csv
import psutil
import platform
from datetime import datetime
from mysql.connector import Error


def addTime (a,b):
    if len(a) != len(b):
        return None
    result = [None] * len(a)

    for i in range(len(a)):
        result[i] = a[i] + b[i]
    return result

def subtractTime (a,b): # a-b
    if len(a) != len(b):
        return None
    result = [None] * len(a)

    for i in range(len(a)):
        result[i] = a[i] - b[i]
    return result

def meanTime (array, num_data):
    result = [None] * len(array)

    for i in range(len(array)):
        result[i] = array[i] / num_data
    return result

def random_string(length):
    # Definisce l'insieme di caratteri da cui estrarre
    caratteri = string.ascii_letters + string.digits + ' '
    # Genera la stringa casuale
    stringa_casuale = ''.join(random.choice(caratteri) for i in range(length))
    return stringa_casuale

def saveResult(directory, matrix, name_file):
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Path file
    file_path = os.path.join(directory, name_file)

    # save matrix in CSV file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(matrix)


def increase_percent(base, increase):
    if len(base) != len(increase): return None
    result = [0] * len(base)
    for i in range(len(base)):
        result[i] = round(((increase[i]-base[i])/base[i])*100, 2)
    return result


def to_percent(y, position):
    """Converts axis values to percentage format."""
    s = str(y)
    return s + '%'

def estimate_completion_time(remaining_operations, elapsed_time, completed_operations):
    """
    Estimates the time for the completion of a process.

    :param remaining_operations: Number of operations remaining to be completed.
    :param elapsed_time: Time already elapsed for the operations that have been completed.
    :param completed_operations: Number of operations that have already been completed.
    :return: Estimated time to complete the remaining operations.
    """
    # Calculate the average completion rate of operations up to this point.
    average_rate = completed_operations / elapsed_time if elapsed_time > 0 else 0

    # If the average rate is greater than zero, estimate the remaining time.
    # Otherwise, return a message indicating that it's not possible to calculate an estimate with the provided data.
    if average_rate > 0:
        estimated_time = remaining_operations / average_rate
        return estimated_time
    else:
        return 0


def print_progress_bar(total_iterations, iterations_completed):
    """
    Prints a progress bar based on the total number of iterations and the number of iterations completed.

    :param total_iterations: The total number of iterations for the process.
    :param iterations_completed: The number of iterations that have been completed.
    """
    # Define the length of the progress bar
    bar_length = 100
    # Calculate the percentage of iterations completed
    progress_percentage = (iterations_completed / total_iterations) * 100
    # Calculate the number of symbols to show in the progress bar
    symbol_count = int((iterations_completed / total_iterations) * bar_length)
    # Create the progress bar stringJami Ramos
    progress_bar = "=" * symbol_count + "." * (bar_length - symbol_count)
    # Print the progress bar with the percentage completed
    print(f"\rProgress: [{progress_bar}] {progress_percentage:.2f}%", end='')


def string_time(seconds):
    # Calculate whole hours, minutes, and seconds
    hours = int(seconds) // 3600
    minutes = (int(seconds) % 3600) // 60
    whole_seconds = int(seconds) % 60

    # Calculate the fractional part of the seconds
    fractional_seconds = seconds - int(seconds)

    # Add the fractional part to the whole seconds to get the total seconds
    total_seconds = whole_seconds + fractional_seconds

    # Print the formatted result
    return f"{hours} h {minutes} min {total_seconds:.2f} sec"


# Funzione per ottenere informazioni sui processori
def get_detailed_cpu_info():
    cpu_info = {
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max}MHz",
        "CPU Name": platform.processor(),
        "Architecture": platform.machine(),
        "Threads per core": psutil.cpu_count(logical=True) // psutil.cpu_count(logical=False)
    }
    return "\n".join([f"{key}: {value}" for key, value in cpu_info.items()])

def get_memory_info():
    ram = psutil.virtual_memory()
    total_ram = ram.total / (1024**3) # Convertito in GB
    return f"Total RAM: {total_ram:.2f} GB"

def get_system_info():
    os, name, version = platform.system(), platform.node(), platform.release()
    return f"Operating System: {os}, System Name: {name}, OS Version: {version}"

# Save information
def save_info(filename="hardware_info.txt"):
    with open(filename, "w") as file:
        file.write(f"Hardware Information - {datetime.now()}\n")
        file.write(get_detailed_cpu_info() + "\n")
        file.write(get_memory_info() + "\n")
        file.write(get_system_info() + "\n")


# Function to set the database connection timeouts
def set_db_timeout(conn, wait_timeout, interactive_timeout):
    try:
        cursor = conn.cursor()
        # Set the session wait_timeout
        cursor.execute(f"SET SESSION wait_timeout = {wait_timeout}")
        # Set the session interactive_timeout
        cursor.execute(f"SET SESSION interactive_timeout = {interactive_timeout}")
        cursor.close()
    except Error as e:
        print(f"Error setting database timeout: {e}")

# Function to reset the database connection timeouts to their default values
def reset_db_timeout_to_default(conn):
    # Default values for wait_timeout and interactive_timeout could vary, 28800 (8 hours) is common
    default_wait_timeout = 28800
    default_interactive_timeout = 28800
    set_db_timeout(conn, default_wait_timeout, default_interactive_timeout)

