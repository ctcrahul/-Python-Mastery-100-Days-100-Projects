
"""                             Day17.py

                      Student Report Generator: CSV Files

"""

import csv

with open('students.csv', 'r') as file:
  reader = csv.reader(file)
  for row in reader:
    print(row)

import csv

with open('students.csv', 'r') as file:
  reader = csv.DictReader(file)
  for row in reader:
    print(row)

import csv

with open('new_students.csv', 'w', newline='') as file:
  writer = csv.writer(file)
  writer.writerow(['Name', 'Math', 'Science', 'English'])
  writer.writerow(['Daisy', 88, 92, 85])

import csv

with open('new_students.csv', 'w', newline='') as file:
  writer = csv.DictWriter(file, fieldnames=['Name', 'Math', 'Science', 'English'])
  writer.writeheader()
  writer.writerow({'Name': 'Eve', 'Math': 91, 'Science': 87, 'English': 90})

# Student Report Generator
import csv

# Step 1: Read student data and calculate avergaes
def process_student_data(input_file, output_file):
  try:
    with open(input_file, 'r') as infile:
      reader = csv.DictReader(infile)
      student_reports = []

      for row in reader:
        name = row['Name']
        math = int(row['Math'])
        science = int(row['Science'])
        english = int(row['English'])
        average = round((math + science + english) / 3, 2)
        status = "Pass" if average >= 60 else "Fail"

        student_reports.append({
          'Name': name,
          'Math': math,
          'Science': science,
          'English': english,
          'Average': average,
          'Status': status
        })

    # Step 2: Write processed data to a new CSV
    with open(output_file, 'w', newline='') as outfile:
      fieldnames = ['Name', 'Math', 'Science', 'English', 'Average', 'Status']
      writer = csv.DictWriter(outfile, fieldnames=fieldnames)
      writer.writeheader()
      writer.writerows(student_reports)

    print(f"Student report generated in {output_file} successfully.")

  except FileNotFoundError:
    print(f"Error: File '{input_file}' not found")
  except KeyError:
    print("Error: Invalid column names in the input file")
  except Exception as e:
    print(f"An error occurred: {e}")

# Main Program
input_file = 'students.csv'
output_file = 'student_report.csv'

process_student_data(input_file, output_file)
