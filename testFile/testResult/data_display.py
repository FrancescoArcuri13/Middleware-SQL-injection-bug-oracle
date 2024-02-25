import os
from matplotlib.ticker import FuncFormatter
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from testFile.tools import subtractTime, addTime, meanTime, increase_percent, to_percent

time_mean_noProxy = []
time_mean_Proxy = []

time_sum_proxy = [0, 0, 0, 0, 0]
time_sum_noProxy = [0, 0, 0, 0, 0]

matrix_sum_noProxy = []
matrix_sum_proxy = []

accumulated_delay_matrix = []
delay_point_from_sum = []


# data extraction
file_path_proxy = 'result_Proxy_1000000.csv'
file_path_no_proxy = 'result_noProxy_1000000.csv'

# read CSV
df = pd.read_csv(file_path_proxy)
matrix_Proxy = df.to_numpy()

df = pd.read_csv(file_path_no_proxy)
matrix_noProxy = df.to_numpy()

if (len(matrix_Proxy) != len(matrix_noProxy)):
    raise ValueError("Matrix size")

for i in range(len(matrix_noProxy)):
    time_sum_proxy = addTime(time_sum_proxy, matrix_Proxy[i])
    time_sum_noProxy = addTime(time_sum_noProxy, matrix_noProxy[i])

    if i > 0:
        matrix_sum_proxy.append(addTime(matrix_sum_proxy[i - 1], matrix_Proxy[i]))
        matrix_sum_noProxy.append(addTime(matrix_sum_noProxy[i - 1], matrix_noProxy[i]))
        accumulated_delay_matrix.append(addTime(accumulated_delay_matrix[i-1],
                                                subtractTime(matrix_Proxy[i], matrix_noProxy[i])))
    else:
        matrix_sum_proxy.append(matrix_Proxy[i])
        matrix_sum_noProxy.append(matrix_noProxy[i])
        accumulated_delay_matrix.append(subtractTime(matrix_Proxy[i], matrix_noProxy[i]))

    delay_point_from_sum.append(subtractTime(matrix_sum_proxy[i], matrix_sum_noProxy[i]))


time_mean_Proxy = meanTime(time_sum_proxy, len(matrix_Proxy))
time_mean_noProxy = meanTime(time_sum_noProxy, len(matrix_noProxy))

average_percentage_increase = increase_percent(time_mean_noProxy, time_mean_Proxy)

# Phase 4 plot result
print("Average noProxy: " + str(time_mean_noProxy))
print("Average Proxy : " + str(time_mean_Proxy))
print("Average percentage increase: " + str(average_percentage_increase))

delay_average_proxy = subtractTime(time_mean_Proxy, time_mean_noProxy)

print("delay average: " + str(delay_average_proxy))


# ----- time proxy vs noProxy -----

# Creating a DataFrame to hold the data
data = {
    'Operation': ['Select', 'Delete', 'Insert', 'Error'],
    'No Proxy': time_mean_noProxy[1:],
    'Proxy': time_mean_Proxy[1:]
}

df = pd.DataFrame(data)
# Melting the DataFrame to make it suitable for sns.barplot
df_melted = df.melt(id_vars='Operation', var_name='Type', value_name='Time')

# Creating the bar plot
sns.set_theme(style="whitegrid")  # Setting the theme for the plot
plt.figure(figsize=(10, 6))  # Setting the figure size
sns.barplot(x='Operation', y='Time', hue='Type', data=df_melted)  # Creating the bar plot

plt.title('Operation Time Comparison')  # Setting the title of the plot
plt.xlabel('Operation')  # Naming the x-axis
plt.ylabel('Time')  # Naming the y-axis
plt.xticks(rotation=45)  # Rotating the x-axis labels for better readability
plt.legend(title='Proxy Usage')  # Adding a legend with a title

# Adjust layout to make room for labels and titles
plt.tight_layout()


# Ensure the 'graphs' subdirectory exists
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# Save the figure
plt.savefig('graphs/operation_time_comparison.png')
# plt.show()  # Displaying the plot


# ----- Percent increase -----

data_percent = {
    'Operation': ['Select', 'Delete', 'Insert', 'Error'],
    'Increase': average_percentage_increase[1:],  # Assuming this is defined correctly
}

df = pd.DataFrame(data_percent)
# Melting the DataFrame to make it suitable for sns.barplot
df_melted = df.melt(id_vars='Operation', var_name='Type', value_name='Time')

# Creating the bar plot with specified modifications
sns.set_theme(style="whitegrid")  # Setting the theme for the plot
plt.figure(figsize=(10, 6))  # Setting the figure size

# Creating the bar plot with a narrower bar width and custom color
barplot = sns.barplot(x='Operation',
                      y='Time',
                      hue='Type',
                      data=df_melted,
                      palette="muted",
                      dodge=True,
                      width=0.5)

for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.2f') + ' %',
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha = 'center', va = 'center',
                     xytext = (0, 9),
                     textcoords = 'offset points')

plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

plt.title('Operation Time Comparison')  # Setting the title of the plot
plt.xlabel('Operation')  # Naming the x-axis
plt.ylabel('Percent')  # Naming the y-axis
plt.xticks(rotation=45)  # Rotating the x-axis labels for better readability
plt.legend(title='Proxy Usage')  # Adding a legend with a title

# Adjust layout to make room for labels and titles
plt.tight_layout()


# Ensure the 'graphs' subdirectory exists
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# Save the figure
plt.savefig('graphs/delay_average_proxy.png')


# ----- Linear graph sum time Proxy -----

# Convert the matrix into a pandas DataFrame with a column for each action
df = pd.DataFrame([row[1:] for row in matrix_sum_proxy], columns=['Select', 'Delete', 'Insert', 'Error'])


# Now, plot the DataFrame
plt.figure(figsize=(10, 6))

# Plot a line for each column in the DataFrame
for column in df.columns:
    plt.plot(df.index, df[column], label=column)

# Add title and labels
plt.title('Cumulative Time for Operations')
plt.xlabel('Observation')
plt.ylabel('Cumulative Time')

# Display the legend
plt.legend()

plt.savefig('graphs/Linear_graph_sum_time_proxy.png')

# ----- Linear graph sum time Proxy vs noProxy -----

# Convert the matrixes into pandas DataFrames, excluding the first column
df_proxy = pd.DataFrame([row[1:] for row in matrix_sum_proxy], columns=['Select', 'Delete', 'Insert', 'Error'])
df_no_proxy = pd.DataFrame([row[1:] for row in matrix_sum_noProxy], columns=['Select', 'Delete', 'Insert', 'Error'])


# Now, plot the DataFrame
plt.figure(figsize=(14, 8))

# Define two color palettes, one for each group
colors_proxy = ['b', 'g', 'r', 'c']

# Plot a line for each column in the proxy DataFrame
for i, column in enumerate(df_proxy.columns):
    plt.plot(df_proxy.index, df_proxy[column],
             label=f'{column} (Proxy)',
             color=colors_proxy[i])

# Plot a line for each column in the no proxy DataFrame
for i, column in enumerate(df_no_proxy.columns):
    plt.plot(df_no_proxy.index, df_no_proxy[column],
             label=f'{column} (No Proxy)',
             color=colors_proxy[i], linestyle='--')

# Add title and labels
plt.title('Cumulative Time for Operations with and without Proxy')
plt.xlabel('Observation Number')
plt.ylabel('Cumulative Time (seconds)')

# Display the legend
plt.legend()

plt.savefig('graphs/Linear_graph_sum_time_proxy_vs_noProxy.png')


# ----- Linear graph accumulated_delay -----

# Convert the matrix into a pandas DataFrame, excluding the first column (timestamp or any non-delay data)
df_accumulated_delay = pd.DataFrame([row[1:] for row in accumulated_delay_matrix],
                                    columns=['Select', 'Delete', 'Insert', 'Error'])

# if Convert the delay values from seconds to minutes by dividing by 60
df_accumulated_delay_minutes = df_accumulated_delay

# Now, plot the DataFrame
plt.figure(figsize=(14, 8))

# Define a color palette
colors = ['b', 'g', 'r', 'c']

# Plot a line for each column in the DataFrame
for i, column in enumerate(df_accumulated_delay_minutes.columns):
    plt.plot(df_accumulated_delay_minutes.index, df_accumulated_delay_minutes[column], label=column, color=colors[i])

# Add title and labels
plt.title('Accumulated Delay for Operations')
plt.xlabel('Observation Number')
plt.ylabel('Accumulated Delay (seconds)')

# Display the legend
plt.legend()

plt.savefig('graphs/Linear_graph_accumulated_delay.png')
