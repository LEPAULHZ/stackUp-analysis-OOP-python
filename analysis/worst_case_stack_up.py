# Worst Case method utilize simple arithmetic
# This method assumed the extreme limits
# Recommend this method for low production volumes
import numpy as np
from analysis.limit_combinations import calculate_limit_combinations


class WorstCaseStackUp:
    def __init__(self, internal_data_frame, external_data_frame):
        # Initialize with the provided data frames for internal and external stack-up
        self.internal_data_frame = internal_data_frame
        self.external_data_frame = external_data_frame
        # Initialize variables to store analysis results
        self.internal_lower_lim = None
        self.internal_upper_lim = None
        self.external_lower_lim = None
        self.external_upper_lim = None
        self.min_gap_value = None
        self.max_gap_value = None
        self.min_gap_label = None
        self.max_gap_label = None
        self.result_message = None

    def run_worst_case(self):
        # Calculate worst-case dimensions and gaps
        self.calculate_internal_limits()
        self.calculate_external_limits()
        self.calculate_limit_combinations()

    # Math for internal stack up
    # Upper limit determines by Max Material Conditions (MMC)
    # Lower limit determines by Least Material Conditions (LMC)
    # Straight forrward logic and airthmetic

    def calculate_internal_limits(self):
        # Calculate internal limits based on nominal and tolerances
        nominal_values = self.internal_data_frame['Nominal'].to_numpy()
        lower_tolerances = self.internal_data_frame['Tolerance'].to_numpy()
        upper_tolerances = self.internal_data_frame['Tolerance'].to_numpy()

        # Calculate upper and lower limits
        sum_nominal = np.sum(nominal_values)
        sum_lower_tol = np.sum(lower_tolerances)
        sum_upper_tol = np.sum(upper_tolerances)

        self.internal_lower_lim = round(sum_nominal - sum_lower_tol, 3)
        self.internal_upper_lim = round(sum_nominal + sum_upper_tol, 3)

    # Math for external stack up
    # Not as straight forward and require understanding the ME design

    def calculate_external_limits(self):
        n = len(self.external_data_frame.index)
        if n >= 5:
            # Calculate external limits based on material conditions and tolerances
            ex_nominal_val = self.external_data_frame['Nominal'].to_numpy()
            ex_lower_tol = self.external_data_frame['Tolerance'].to_numpy()
            ex_upper_tol = self.external_data_frame['Tolerance'].to_numpy()

            # Calculate lower and upper values of the array using vectorized operations
            ex_lower_val = ex_nominal_val - ex_lower_tol
            ex_upper_val = ex_nominal_val + ex_upper_tol

            # Adjust the first and last row limits
            # The lower limit for the first and last row is when we have MMC
            # The upper limit for the first and last row is when we have LMC
            # This logic is opposite for all the other bodies
            ex_lower_val[0] = ex_nominal_val[0] + ex_lower_tol[0]
            ex_lower_val[-1] = ex_nominal_val[-1] + ex_lower_tol[-1]
            ex_upper_val[0] = ex_nominal_val[0] - ex_upper_tol[0]
            ex_upper_val[-1] = ex_nominal_val[-1] - ex_upper_tol[-1]

            # Calculate upper and lower limits
            ex_lower_lim = round(((ex_lower_val[1]-ex_lower_val[0]) + (
                sum(ex_lower_val[2:-2])) + (ex_lower_val[-2]-ex_lower_val[-1])), 3)
            ex_upper_lim = round(((ex_upper_val[1]-ex_upper_val[0]) + (
                sum(ex_upper_val[2:-2])) + (ex_upper_val[-2]-ex_upper_val[-1])), 3)

            self.external_lower_lim = ex_lower_lim
            self.external_upper_lim = ex_upper_lim

        else:
            raise ValueError(
                'This particular case requires at least 5 arguments')

    def calculate_limit_combinations(self):
        # Calculate the gap combinations and results
        self.min_gap_value, self.max_gap_value, self.min_gap_label, self.max_gap_label, self.result_message = calculate_limit_combinations(
            self.internal_lower_lim, self.internal_upper_lim, self.external_lower_lim, self.external_upper_lim)

    def print_results(self):
        # Print the results of the Worst Case analysis
        print('Worst Case Method')
        print('Internal Dimensions: |Lower Limit:', self.internal_lower_lim, 'in.|',
              '|Upper Limit:', self.internal_upper_lim, 'in.|')
        print('External Dimensions: |Lower Limit:', self.external_lower_lim, 'in.|',
              '|Upper Limit:', self.external_upper_lim, 'in.|')
        print("Minimum Gap:", self.min_gap_label,
              '|', self.min_gap_value, 'in.|')
        print("Maximum Gap:", self.max_gap_label,
              '|', self.max_gap_value, 'in.|')
        print(self.result_message)
