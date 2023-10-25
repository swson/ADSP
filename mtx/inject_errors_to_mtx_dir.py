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

def add_gaussian_noise_symmetric(matrix, error_rate, injection_rate, mean, std_dev):
    rows, cols = np.shape(matrix)
    
    # Count total number of elements
    total_elements = rows * (cols - 1) 

    # Calculate the number of elements to inject noise
    num_noisy_elements = int(np.ceil(total_elements * injection_rate))


    # Randomly select a location to inject noise
    noisy_indices = np.random.choice(total_elements, num_noisy_elements, replace=False)

    # Create an empty matrix to add errors to.
    noise_matrix = np.zeros((rows, cols))



    # Add Gaussian noise to selected locations
    counter = 0
    for index in noisy_indices:
        # Convert 1D index to 2D matrix index
        i = index // cols
        j = index % cols
        if j < i:  # Skip the bottom triangle for symmetry.
            continue

        # Gaussian noise generation
        noise = np.random.normal(mean, std_dev)

        #Noise adjustment based on error rate
        noise = noise * error_rate

        # Add noise (maintain symmetry)
        noise_matrix[i][j] = noise
        noise_matrix[j][i] = noise

        counter += 1
        if counter >= num_noisy_elements:
            break

    # Add a noise matrix to the original matrix.
    result_matrix = np.add(matrix, noise_matrix)

    
    return result_matrix


# Read the matrix market file
A = read_matrix_from_mtx('C:\\Work\\School\\Coding\\ADSP\\494_bus\\494_bus.mtx')

# # example matrix
# A = np.array([[1, 0, 2, 0, 0, 0, 0, 0, 0, 0],
#               [0, 3, 0, 0, 1, 0, 0, 0, 0, 3],
#               [2, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#               [0, 0, 0, 2, 1, 0, 0, 0, 0, 0],
#               [0, 1, 0, 1, 7, 0, 0, 0, 0, 1],
#               [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
#               [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
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
mtx_file_path = 'C:\\Work\\School\\Coding\\ADSP\\result_1013\\494_bus_gauss_0p10_0p10_sym.mtx'


# Save the dense matrix to a .mtx file
save_dense_to_mtx(noisy_matrix, mtx_file_path)


# print("matrix with added noise:")
# print(noisy_matrix)

# print(mean,std_dev, error_rate, injection_rate)