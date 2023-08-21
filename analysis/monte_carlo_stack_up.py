# Monte Carlo Simulation method for random distribution
import numpy as np
from analysis.random_sample_generator import RandomSampleGenerator


class MonteCarloStackUp:
    def __init__(self, internal_data_frame, external_data_frame, num_samples):
        # Initialize with the provided data frames for internal and external stack-up
        self.internal_data_frame = internal_data_frame
        self.external_data_frame = external_data_frame
        self.num_samples = num_samples
        # Initialize variables to store analysis results
        self.internal_dim = None
        self.external_dim = None
        self.gap_dim = None

    def run_monte_carlo(self):
        # Entry point for performing the Monte Carlo analysis
        self.generate_sample_data()
        self.perform_monte_carlo_analysis()

    def generate_sample_data(self):
        # Generate random sample data for the analysis

        # Create instances of RandomSampleGenerator for internal and external data
        sample_generator_internal = RandomSampleGenerator(
            self.internal_data_frame)
        sample_generator_external = RandomSampleGenerator(
            self.external_data_frame)

        # Generate vertical stacks of 'ave', 'SD', and 'sample size' array
        v_stack_internal = sample_generator_internal.vertical_stack(
            self.num_samples)
        v_stack_external = sample_generator_external.vertical_stack(
            self.num_samples)

        # Generate normal distributions for internal and external samples
        random_sample_internal = np.apply_along_axis(
            sample_generator_internal.normal_dist, axis=1, arr=v_stack_internal)
        random_sample_external = np.apply_along_axis(
            sample_generator_external.normal_dist, axis=1, arr=v_stack_external)

        # Select random values from the normal distributions for each sample
        in_samp_rand = np.apply_along_axis(
            np.random.choice, axis=1, arr=random_sample_internal)
        ex_samp_rand = np.apply_along_axis(
            np.random.choice, axis=1, arr=random_sample_external)

        # Store the generated sample data for future use
        self.in_samp_rand = in_samp_rand
        self.ex_samp_rand = ex_samp_rand
        self.random_sample_internal = random_sample_internal
        self.random_sample_external = random_sample_external

    def perform_monte_carlo_analysis(self):
        # Perform the Monte Carlo analysis using the generated sample data
        internal_dim, external_dim = self.calculate_monte_carlo(
            self.in_samp_rand, self.ex_samp_rand)

        # Calculate the gap dimension between internal and external stack-ups
        gap_dim = np.round(
            external_dim - internal_dim, 3)

        # Store the calculated results for later reference
        self.internal_dim = internal_dim
        self.external_dim = external_dim
        self.gap_dim = gap_dim

    def calculate_monte_carlo(self, internal_sample, external_sample):
        # Math for internal stack up
        # Sum all the individual random samples for each body together
        internal_stack_sum = np.round(sum(internal_sample), 3)

        # Math for external stack up
        # Calculate the difference on the top and bottom bodies to get the thickness
        # Then sum all the individual random samples for each body together
        ex_bottom_layer = np.absolute(external_sample[0] - external_sample[1])
        ex_top_layer = np.absolute(external_sample[-1] - external_sample[-2])
        ex_mid_layers_sum = sum(external_sample[2:-2])

        num_external_samples = len(external_sample)
        if num_external_samples >= 5:
            external_stack_sum = np.round(
                sum([ex_bottom_layer, ex_top_layer, ex_mid_layers_sum]), 3)
        else:
            raise ValueError(
                'This particular case requires at least 5 arguments')
        return internal_stack_sum, external_stack_sum

    def print_results(self):
        # Print the results of the Monte Carlo analysis
        print('Monte Carlo Method')
        print('Internal Dimensions:', '|', self.internal_dim, 'in. |')
        print('External Dimensions:', '|', self.external_dim, 'in. |')
        print('Gap:', '|', self.gap_dim, 'in. |')
