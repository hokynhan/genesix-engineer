import argparse

def sum(args):
    a = args.a
    b = args.b
    print(f"Sum of a and b is {a + b}")

# This is only executed when invoking this script
if __name__ == "__main__":
    # Create a parser to receive the command line arguments
    parser = argparse.ArgumentParser()

    # Define all arguments
    parser.add_argument("-a", type=int, required=True)
    parser.add_argument("-b", type=int, required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Run the sum function
    sum(args)