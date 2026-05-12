import csv

# 예전 방식
data = [
    ["name", "age", "City"],
    ["John", "25", "Seoul"],
    ["James", "23", "Busan"],
    ["Bob", "24", "Seoul"] 
]

filename = "data.csv"

with open(filename, "w", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(data)

data2 = [
    {"Name":"John", "Age":"25", "City":"Seoul"},
    {"Name":"James", "Age":"23", "City":"Busan"},
    {"Name":"Bob", "Age":"24", "City":"Seoul"} 
]


with open(filename, "w", newline="") as file:
    # headers = ["Name","Age","City"]
    headers = data2[0].keys()
    csv_writer = csv.DictWriter(file, fieldnames=headers)
    csv_writer.writeheader()
    csv_writer.writerows(data2)