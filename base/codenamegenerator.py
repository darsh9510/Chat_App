import csv
import random
import os

def helper(csv_file):
    pwd = os.getcwd()
    new_path = os.path.join(pwd,csv_file)
    #print(new_path)
    with open(new_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        random_row = random.choice(rows)
        return random_row

# Example usage:
def generate_codenames():
    csv_file = 'birds.csv'
    name = helper(csv_file=csv_file)[0]
    return [name]