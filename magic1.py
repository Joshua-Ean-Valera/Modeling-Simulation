def generate_odd_magic_square(n):
    """
    Generates an n x n magic square for an odd n using the Siamese method.
    """
    if n % 2 == 0:
        raise ValueError("This function only generates magic squares for odd orders.")

    magic_square = [[0 for _ in range(n)] for _ in range(n)]

    # Starting position for 1
    i = 0
    j = n // 2

    # Fill the square with numbers from 1 to n*n
    for num in range(1, n * n + 1):
        magic_square[i][j] = num

        # Calculate the next position
        next_i = (i - 1 + n) % n
        next_j = (j + 1) % n

        # If the next position is already filled, move down instead
        if magic_square[next_i][next_j] != 0:
            i = (i + 1) % n
        else:
            i = next_i
            j = next_j

    return magic_square

def print_magic_square(square):
    """
    Prints a magic square in a formatted way.
    """
    n = len(square)
    for i in range(n):
        for j in range(n):
            print(f"{square[i][j]:4}", end="")
        print()

# Example usage:
n = 5  # Must be an odd number
try:
    magic_square = generate_odd_magic_square(n)
    print(f"Magic Square of order {n}:")
    print_magic_square(magic_square)
except ValueError as e:
    print(e)