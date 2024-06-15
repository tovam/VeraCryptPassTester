import itertools
import argparse
import sys
import os
import subprocess
import getpass
from itertools import chain, combinations, permutations, product
import time

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

class Element:
    def __init__(self, operation, elements):
        self.operation = operation
        self.elements = elements

    def generate(self):
        if self.operation == 'perms':
            return [''.join(p) for p in permutations(self.elements)]
        elif self.operation == 'exact':
            return [''.join(self.elements)]
        elif self.operation == 'oneof':
            return self.elements
        elif self.operation == 'power':
            return [''.join(p) for p in powerset(self.elements)]
        else:
            raise ValueError(f"Unknown operation: {self.operation}")

class PasswordTemplate:
    def __init__(self, elements=None):
        self.elements = elements if elements else []

    def add_element(self, operation, elements):
        self.elements.append(Element(operation, elements))

    def generate_combinations(self):
        parts_combinations = [element.generate() for element in self.elements]
        return [''.join(comb) for comb in product(*parts_combinations)]

    def __contains__(self, item):
        return item in self.generate_combinations()

    def size(self):
        total_size = 1
        for element in self.elements:
            total_size *= len(element.generate())
        return total_size

def test_password(container_path, password):
    """
    Test a single password on the VeraCrypt container.
    """
    os.makedirs('/tmp/veracrypt', exist_ok=True)
    try:
        result = subprocess.run(
            ['veracrypt', '--text', '--mount', container_path, '/tmp/veracrypt', '--password', password, '--non-interactive'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and "Error" not in result.stderr:
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
    return False

def print_progress_line(index, max_tries):
    progress = int(index / max_tries * 100)
    bar_length = 23
    filled_length = int(progress * bar_length // 100)
    bar = '#' * filled_length + '.' * (bar_length - filled_length)
    print(f"Test {index}/{max_tries}   [{bar}]   ", end='', flush=True)

def test_passwords(container_path, password_template):
    """
    Test all combinations of the password template for the VeraCrypt container.
    """
    combinations = password_template.generate_combinations()
    max_tries = len(combinations)
    total_time = 0

    for index, combo in enumerate(combinations):
        start_time = time.time()
        print_progress_line(index, max_tries)

        if test_password(container_path, combo):
            print(f"\nPassword found:\n{combo}")
            subprocess.run(['veracrypt', '--dismount', '/tmp/veracrypt'], capture_output=True)
            return combo

        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        avg_time_per_test = total_time / (index + 1)
        remaining_tests = max_tries - (index + 1)
        remaining_time = avg_time_per_test * remaining_tests / 60
        print(f"remaining: {int(remaining_time)} minutes", end='\r', flush=True)
    print_progress_line(index+1, max_tries)

    print("\nNo valid password found.")
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Test combinations of password templates on a VeraCrypt container.",
        epilog="""\
Interactive input: Use the format 'operation(elements)' separated by '+'.
Operations: perms, exact, oneof, power.
Example: perms(a,b,c)+exact(123)+oneof(x,y,z) will try `abc123x`, `abc123y`, ..., `cba123z`
"""
    )
    parser.add_argument('container_path', metavar='container_path', type=str, help='The path to the VeraCrypt container.')

    args = parser.parse_args()

    password_template = PasswordTemplate()

    print("Enter elements (hidden input):")
    while True:
        input_str = getpass.getpass(" > ")
        if input_str == "":
            break
        for p in input_str.split("+"):
            operation, elements_str = p.split('(')
            elements = elements_str.rstrip(')').split(',')
            password_template.add_element(operation, elements)

    container_path = sys.argv[1]
    test_passwords(container_path, password_template)

if __name__ == "__main__":
    main()
