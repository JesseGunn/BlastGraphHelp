"""
Blast Output Organizer

Input: multiple Blast files

Output:
    single file with all Blasts in csv format
    each line has chromosome number in easy format
    queries are named by the gene
"""
import csv
import os

# All of the following is using the blast output format of
# -outfmt "6 qseqid sseqid sstart send length evalue"
# indexes == 0      1      2      3    4      5


# Assign stat columns based on specified column
EVALUE = 5
LENGTH = 4

# Values to be filtered for
MIN_EVALUE = 1e-20
MIN_LENGTH = 30

# Query names to be replaced (qseqid)
QUERY = 0
QUERY_OLD = ["NC_007422.5:c5213284-5181082", "NC_007417.3:c9357295-9346855"]
QUERY_NEW = ["DOUBLESEX", "FRUITLESS"]

# Chromosome Names (sseqid)
# *Chromosomes must be ordered*
CHROMOSOME = 1
CHROMOSOME_LIST = ["CM069432.1", "CM069433.1", "CM069434.1", "CM069435.1",
                  "CM069436.1", "CM069437.1", "CM069438.1"] # Corresponds to chromosomes 1-7 and X


def readFile(directory, FileName) :
    File = open(f"{directory}{FileName}", "r")
    return File

def tidy(File, data) :
    for line in File :
        line = list(line.split())
        line.append("x")
        line_new = line

        #Create table of data
        print(line_new)
        data.append(line_new)

def filter(data) :
    data_new = []
    for row in data :
        if float(row[EVALUE]) >= MIN_EVALUE and int(row[LENGTH]) >= MIN_LENGTH:
            data_new.append(row)

    return data_new

def rename_query(data) :
    for row in data :
        query_index = QUERY_OLD.index(row[QUERY]) # INDEX OF QUERY
        row[QUERY] = QUERY_NEW[query_index]

def rename_chromosome(data) :
    for row in data :
        chrom_index = CHROMOSOME_LIST.index(row[CHROMOSOME]) # INDEX OF CHROMOSOME
        row[CHROMOSOME] = (f"CHROMOSOME {chrom_index + 1}")

def all_edits(data, filt = False, quer = False, chrom = False) :
    # Filter Stats
    data = filter(data)
    # Rename Queries
    data = rename_query(data)
    # Rename Chromosomes
    data = rename_chromosome(data)
    return data

def asker() :
    print("Would you like to filter for Evalue and Length?")
    filt = input("Y / N\n")
    if filt == "Y" : filt = True
    else : filt = False
    print("Would you like to rename queries?")
    quer = input("Y / N\n")
    if quer == "Y" : quer = True
    else : quer = False
    chrom = input("Y / N\n")
    if chrom == "Y" : chrom = True
    else : chrom = False

    return filt, quer, chrom

def main():
    #Create stored values
    directory = "/School/biol325_evogeno/Capstone/BlastFiles/" #Location of Blast files
    csv_file_path = directory + "file_test.csv" #Location to output CSV file
    
    data = []

    # Run for each file in directory
    for out in os.listdir(directory):
        if out.endswith(".out") :
            file = readFile(directory, out)
            tidy(file, data)
        else : print("Not a Blast File")

    # ask user in terminal
    filt, quer, chrom = asker()

    # if you dont want user input remove following hashtags (Do not worry about false, it is set default)
    #filt = True
    #quer = True
    #chrom = True

    data = all_edits(data, filt, quer, chrom)

    #Create csv
    with open(csv_file_path, mode='w', newline='') as file:
        # Create a csv.writer object
        writer = csv.writer(file)
        # Write data to the CSV file
        writer.writerows(data)

    #CHECK
    print(f"CSV file '{csv_file_path}' created successfully.")


main()