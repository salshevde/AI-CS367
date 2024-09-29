import numpy as np
import h5py
import scipy.io as sio
from sklearn.metrics import pairwise_distances

# Load the scrambled image from .mat file (HDF5 format)
def load_scrambled_image(file_path):
    with h5py.File(file_path, 'r') as f:
        scrambled_image = f['scrambled_lena.mat'][()]
    return scrambled_image

# Split image into tiles of size (tile_size x tile_size)
def split_image(image, tile_size):
    tiles = []
    img_h, img_w = image.shape
    for row in range(0, img_h, tile_size):
        for col in range(0, img_w, tile_size):
            tiles.append(image[row:row+tile_size, col:col+tile_size])
    return tiles

# Calculate edge features for a tile
def calculate_edge_features(tile):
    top_edge = tile[0, :]
    bottom_edge = tile[-1, :]
    left_edge = tile[:, 0]
    right_edge = tile[:, -1]
    return np.concatenate([top_edge, bottom_edge, left_edge, right_edge])

# Solve the puzzle and assemble the correct image
def solve_puzzle(tiles, tile_size):
    num_tiles = len(tiles)
    grid_size = int(np.sqrt(num_tiles))

    # Calculate edge features for all tiles
    edge_features = np.array([calculate_edge_features(tile) for tile in tiles])

    # Calculate distances between edge features
    distances = pairwise_distances(edge_features)
    np.fill_diagonal(distances, np.inf)

    # Create an empty array for the solved image
    solved_image = np.zeros((grid_size * tile_size, grid_size * tile_size), dtype=np.uint8)

    # Start with the first tile
    current_tile_idx = 0
    visited = {current_tile_idx}
    solved_image[0:tile_size, 0:tile_size] = tiles[current_tile_idx]

    # Place tiles based on closest matching edges
    for i in range(1, num_tiles):
        current_distances = distances[current_tile_idx]
        next_tile_idx = np.argmin(current_distances)
        while next_tile_idx in visited:
            current_distances[next_tile_idx] = np.inf
            next_tile_idx = np.argmin(current_distances)

        visited.add(next_tile_idx)

        row = (i // grid_size) * tile_size
        col = (i % grid_size) * tile_size
        solved_image[row:row+tile_size, col:col+tile_size] = tiles[next_tile_idx]

        current_tile_idx = next_tile_idx

    return solved_image

# Save the solved image to a .mat file
def save_image_to_mat(file_path, image):
    sio.savemat(file_path, {'solved_lena': image})

# Main function
def main():
    input_file = 'scrambled_lena.mat'  # Adjust the path if necessary
    output_file = 'solved_lena.mat'
    tile_size = 128  # Adjust based on your scrambled image size

    # Load scrambled image
    scrambled_image = load_scrambled_image(input_file)

    # Split the image into tiles
    tiles = split_image(scrambled_image, tile_size)

    # Solve the puzzle
    solved_image = solve_puzzle(tiles, tile_size)

    # Save the solved image
    save_image_to_mat(output_file, solved_image)

if __name__ == '__main__':
    main()
