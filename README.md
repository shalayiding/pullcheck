# Homework Submission Status Checker

This project calculates the homework submission status based on pull requests from a GitHub repository.

## Installation

To get started, clone the repository and install the required dependencies.

```bash
git clone https://github.com/yourusername/homework-submission-checker.git
cd Pullcheck
pip install -r requirements.txt
```

## Usage

To calculate the homework submission status, run the main.py script with the required arguments.
The script expects two arguments: the start hw(i)th to the end hw(j)th.

```bash
python main.py (i)th (j)th
```

For example, to check the submission homework 1 to 5, you would run:

```bash
python main.py 1 5
```

## Results

After running the script, the results will be saved in a CSV file located at table/homework.csv.
