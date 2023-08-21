import os
import pandas as pd
from matplotlib import pyplot
from analysis.monte_carlo_stack_up import MonteCarloStackUp
from analysis.worst_case_stack_up import WorstCaseStackUp
from analysis.RSS_stack_up import RSSStackUp

# Function to load data from Excel sheets into DataFrames


def load_data(file_path):
    sheet_title1 = 'internal_stack_up_data'
    df1 = pd.read_excel(file_path, sheet_name=sheet_title1)
    df_mod1 = df1.copy()    # Create a copy to work with

    sheet_title2 = 'external_stack_up_data'
    df2 = pd.read_excel(file_path, sheet_name=sheet_title2)
    df_mod2 = df2.copy()    # Create a copy to work with

    return df_mod1, df_mod2


# Function to plot a normal distribution


def plot_normal_distribution(some_array, sample_size):
    pyplot.hist(some_array, bins=20)
    pyplot.title('%d Samples' % sample_size)
    pyplot.show()


# Main function


def main():
    # --------------------------
    # Data Loading and Settings
    # --------------------------

    # Creating original file path of the data
    cwd = os.getcwd()

    # Specify the data folder name
    data_folder = 'data'

    # Construct the file path to your data file
    file_title = 'stack_up_analysis.xlsx'
    file_path = os.path.join(cwd, data_folder, file_title)

    # Load data
    df_mod1, df_mod2 = load_data(file_path)

    # ----------------------
    # Monte Carlo Method
    # ----------------------

    # Set the number of samples to generate
    num_samples = 1000
    monte_carlo = MonteCarloStackUp(df_mod1, df_mod2, num_samples)
    monte_carlo.run_monte_carlo()
    monte_carlo.print_results()
    print('--------------------')

    # ----------------------
    # Worst Case Method
    # ----------------------
    worst_case = WorstCaseStackUp(df_mod1, df_mod2)
    worst_case.run_worst_case()
    worst_case.print_results()
    print('--------------------')

    # ----------------------
    # Root Sum Square Method
    # ----------------------
    RSS = RSSStackUp(df_mod1, df_mod2)
    RSS.run_RSS()
    RSS.print_results()
    print('--------------------')


# Entry point of the scripts
if __name__ == '__main__':
    main()
