import data.fetch_data as fetch_data
from config import *
import csv
import sys


def validate_integer(arg):
    try:
        return int(arg)
    except ValueError:
        raise ValueError(f"Invalid input: '{arg}' is not an integer.")

def main():
    if len(sys.argv) != 3:
        print("Error: Exactly two integer arguments are required.")
        print("Usage: python script.py <int1> <int2>")
        sys.exit(1)

    arg1, arg2 = sys.argv[1], sys.argv[2]

    try:
        hw_from = validate_integer(arg1)
        hw_to = validate_integer(arg2)
        fetcher = fetch_data.fetch("Liam-Zhou","chuwa0610")
        fetcher.fetch_all_branch()
        fetcher.create_map()
        fetcher.all_pr_by_student()
        colsnames= ["Student Name"]+[f"Hw{i} PR" for i in range(hw_from, hw_to + 1)]
        
        with open(os.path.join(TABLE_DIR,"homework.csv"), mode="w", newline="") as file:
            writer = csv.writer(file)    
            writer.writerow(colsnames)
                
            for pr_author,pr_urls in fetcher.student_pr_map.items():
                row = [pr_author]
                for i in range(hw_from, hw_to + 1):
                    hw_pr = next((url for url in pr_urls if f"hw{i}" in url.lower()), "")
                    row.append(hw_pr)
                writer.writerow(row)
            
    except ValueError as e:
        print(e)
        sys.exit(1)


if __name__ == '__main__':
    main()


