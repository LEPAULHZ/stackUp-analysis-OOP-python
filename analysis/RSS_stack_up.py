# Root Sum Square (RSS) method assume a normal statistical distribution
import numpy as np
from analysis.limit_combinations import calculate_limit_combinations
sigma = 3


class RSSStackUp:
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

    def run_RSS(self):
        # Calculate RSS dimensions and gaps
        self.calculate_internal_limits()
        self.calculate_external_limits()
        self.calculate_limit_combinations()

    def calculate_internal_limits(self):
        # Extract 'Nominal', 'SD' columns as NumPy arrays
        in_nominal_val = self.internal_data_frame['Nominal'].to_numpy()
        in_SD_val = self.internal_data_frame['SD'].to_numpy()

        # Calculate squares of standard deviations
        in_SD_square = in_SD_val ** 2

        # Calculate Root Sum Square (RSS) & 'Nominal' sum
        in_rss = np.sqrt(np.sum(in_SD_square))
        in_nominal_sum = sum(in_nominal_val)

        # Calculate 3 sigma tolerance zone
        in_tol = in_rss * sigma

        # Calculate upper and lower limits
        self.internal_lower_lim = round(in_nominal_sum - in_tol, 3)
        self.internal_upper_lim = round(in_nominal_sum + in_tol, 3)

    def calculate_external_limits(self):
        n = len(self.external_data_frame.index)
        if n >= 5:
            # Extract 'Nominal', 'SD' columns as NumPy arrays
            ex_nominal_val = self.external_data_frame['Nominal'].to_numpy()
            ex_SD_val = self.external_data_frame['SD'].to_numpy()

            # Calculate squares of standard deviations
            ex_SD_square = ex_SD_val ** 2

            # Calculate the 'Nominal' sum of external dimensions,
            # accounting for the unique calculation for the first and last row,
            # and summing the rest of the intermediate rows.
            ex_rss = np.sqrt(np.sum(ex_SD_square))
            ex_nominal_sum = (ex_nominal_val[1] - ex_nominal_val[0]) + sum(
                ex_nominal_val[2:-2]) + (ex_nominal_val[-2] - ex_nominal_val[-1])

            # Calculate 3 sigma tolerance zone
            ex_tol = ex_rss * sigma

            # Calculate upper and lower limits
            self.external_lower_lim = round(ex_nominal_sum - ex_tol, 3)
            self.external_upper_lim = round(ex_nominal_sum + ex_tol, 3)

        else:
            raise ValueError(
                'This particular case requires at least 5 arguments')

    def calculate_limit_combinations(self):
        # Calculate the gap combinations and results
        self.min_gap_value, self.max_gap_value, self.min_gap_label, self.max_gap_label, self.result_message = calculate_limit_combinations(
            self.internal_lower_lim, self.internal_upper_lim, self.external_lower_lim, self.external_upper_lim)

    def print_results(self):
        # Print the results of the Root Sum Square analysis
        print('Root Sum Square Method')
        print('Internal Dimensions: |Lower Limit:', self.internal_lower_lim, 'in.|',
              '|Upper Limit:', self.internal_upper_lim, 'in.|')
        print('External Dimensions: |Lower Limit:', self.external_lower_lim, 'in.|',
              '|Upper Limit:', self.external_upper_lim, 'in.|')
        print("Minimum Gap:", self.min_gap_label,
              '|', self.min_gap_value, 'in.|')
        print("Maximum Gap:", self.max_gap_label,
              '|', self.max_gap_value, 'in.|')
        print(self.result_message)
