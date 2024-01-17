import numpy as np
import matplotlib.pyplot as plt
from scipy.io import mmread, mmwrite
from scipy.sparse import csr_matrix, find

def read_matrix_from_mtx(file_path):
    dense_matrix = mmread(file_path)
    csr_data = csr_matrix(dense_matrix)
    # Convert mtx to bin
    bin_data = csr_data.toarray()
    return bin_data

def save_dense_to_mtx(bin_data, mtx_file_path):
    """
    Save a dense matrix to a .mtx file.

    Parameters:
    dense_data (np.ndarray): The dense matrix to save.
    mtx_file_path (str): Path to the .mtx file.
    """
    # Convert dense matrix to CSR format
    csr_data = csr_matrix(bin_data)



    # Save as a .mtx file
    mmwrite(mtx_file_path, csr_data)


def format_element(x):
    if x != 0:
        # Calculate the number of rounding digits by considering the length of the entire number
        if x > 0:
            total_digits = 7
            integer_part = len(str(int(x)))  # length of integer part
            decimal_places = total_digits - integer_part   
            round_number = math.floor(x * (10**decimal_places)) / (10**decimal_places)  
            return round_number
        else:
            total_digits = 8
            integer_part = len(str(int(abs(x))))  # length of integer part
            decimal_places = total_digits - integer_part - 1  # -1 for the decimal point
            round_number = math.floor(x * (10**decimal_places)) / (10**decimal_places)  
            return round_number
    else:
        return 0


def add_gaussian_noise_symmetric(matrix, error_rate, injection_rate, mean, std_dev):
    rows, cols = np.shape(matrix)
    
    # Find the position of a non-zero element.
    non_zero_indices = [(i, j) for i in range(rows) for j in range(i, cols) if matrix[i][j] != 0]

    # Calculate number of elements to inject noise (only for non-zero elements)
    num_noisy_elements = int(np.ceil(len(non_zero_indices) * injection_rate))

    # Randomly select an element to inject noise from among the non-zero elements
    noisy_indices = np.random.choice(range(len(non_zero_indices)), num_noisy_elements, replace=False)

    # Create an empty matrix to add errors to.
    noise_matrix = np.zeros((rows, cols))

    # Add Gaussian noise to selected locations
    for index in noisy_indices:
        i, j = non_zero_indices[index]  # Convert to actual matrix index

        # Gaussian noise generation
        noise = np.random.normal(mean, std_dev)

        # Noise adjustment based on error rate
        noise = noise * error_rate

        # Add noise (maintain symmetry)
        noise_matrix[i][j] = noise
        noise_matrix[j][i] = noise  # Same noise applies to symmetrical elements
       
        
        

    # Add a noise matrix to the original matrix.
    result_matrix = np.add(matrix, noise_matrix)
    
    return result_matrix

# Read the matrix market file
A = read_matrix_from_mtx('C:\\Work\\School\\Coding\\ADSP\\1138_bus\\1138_bus.mtx')

# # example matrix
# A = np.array([[1, 0, 2, 0, 0, 0, 0, 0, 0, 0],
#               [0, 3, 0, 0, 1, 0, 0, 0, 0, 3],
#               [2, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 2, 1, 0, 0, 0, 0, 0],
#               [0, 1, 0, 1, 7, 0, 0, 0, 0, 1],
#               [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],.
#               [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
#               [0, 0, 0, 0, 0, 0, 0, 0, 2, 0],
#               [0, 3, 0, 0, 1, 0, 0, 0, 0, 3]])

# Extract non-zero elements
non_zero_elements = A[A != 0]

# Calculate parameters of Gaussian distribution
mean = np.mean(non_zero_elements)
std_dev = np.std(non_zero_elements)
error_rate=0.10
injection_rate=0.10

# Create a matrix with added noise
noisy_matrix = add_gaussian_noise_symmetric(A, error_rate, injection_rate, mean, std_dev)

# Path to the .mtx file
mtx_file_path = 'C:\\Work\\School\\Coding\\ADSP\\result_1226_2023\\1138_bus_gauss_0p10_0p10_nonzero_round.mtx'

round_noisy_matrix = np.vectorize(format_element)(noisy_matrix)

# Save the dense matrix to a .mtx file
save_dense_to_mtx(round_noisy_matrix, mtx_file_path)


# print("matrix with added noise:")
# print(noisy_matrix)

# print(mean,std_dev, error_rate, injection_rate)
