#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt


def plot_csv_data(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Display the first few rows of the DataFrame
    print(df.head())

    # Plot the data
    df.plot(kind="line", x=df.columns[0], y=df.columns[1:])

    # Set the title and labels
    plt.title("CSV Data Plot")
    plt.xlabel(df.columns[0])
    plt.ylabel("Values")

    # Show the plot
    plt.show()
