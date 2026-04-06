import csv

# If the requested logo is in the database lookup returns it
names = []
with open("LogoDatabase.csv", "r", encoding='utf-8', errors='ignore') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        if row['logoName'].upper not in names:
            names.append(row['logoName'].upper())

def lookup(name):
    if name.upper() in names:
        return name
    return None


