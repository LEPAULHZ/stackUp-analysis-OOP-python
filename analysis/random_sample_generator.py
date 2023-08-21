import numpy as np


class RandomSampleGenerator:

    def __init__(self, data_frame):
        self.data_frame = data_frame

    def vertical_stack(self, sample_size):
        # Extract 'Nominal' and 'SD' columns as arrays
        ave = self.data_frame['Nominal'].to_numpy()
        std = self.data_frame['SD'].to_numpy()

        # Create an array with the value sample_size for each row
        sizes = np.full(self.data_frame.shape[0], sample_size)

        # Stack 'ave', 'std', and 'sizes' vertically
        v_stack = np.column_stack((ave, std, sizes))
        return v_stack

    def normal_dist(self, row):
        mean = row[0]  # 'Nominal'
        std = row[1]   # 'SD'
        sizes = int(row[2])  # Convert to integer

        # Generate random samples from a normal distributions
        samples = np.random.normal(mean, std, sizes)
        return samples
