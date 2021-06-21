import csv
import sys




def readFirstLine():
    linecount = 0
    header = []
    with open('eth_txs_201901.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if linecount == 0:
                header = row
                linecount += 1
            elif linecount == 1:
                for index, entry in enumerate(row):
                    print(header[index], ":", entry)
                linecount += 1
            else:
                break

def createSmallerFile(start_line = 1, num_lines = 100):
    endline = start_line + num_lines
    linecount = 0
    file = "ethtxs_" + str(start_line) + "_" + str(endline) + ".csv"
    write_file = open(file, 'w')
    writer = csv.writer(write_file)
    with open('eth_txs_201901.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if linecount == 0:
                writer.writerow(row)
                linecount += 1
            elif linecount < start_line:
                print("ignoring", linecount)
                linecount += 1
            elif linecount >= start_line and linecount < endline:
                # print("writing", linecount)
                writer.writerow(row)
                linecount += 1
            else:
                print(linecount)
                break
    write_file.close()
    print("done!")


def countAddresses(filename):
    '''
        Total From Addresses: 16500883
        Total To Addresses: 16500883
        Total Unique From Addresses: 2501718
        Total Unique To Addresses: 2061195
        Total Unique From and To Addresses: 1626334


        Percent Unique From Addresses: 15%
        Percent Unique To Addresses: 12%
        Unique From and To Addresses: 10%
    '''

    csv.field_size_limit(sys.maxsize)

    linecount = 0
    to_addr = []
    from_addr = []
    # count transactions between addresses
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if linecount == 0:
                linecount += 1
                continue
            # linecount += 1
            if row[5] and row[6]:
                from_addr.append(row[5])
                to_addr.append(row[6])


    print("Total From Addresses:", len(from_addr))
    print("Total To Addresses:", len(to_addr))
    set_from = set(from_addr)
    set_to = set(to_addr)

    print("Total Unique From Addresses:",len(set_from))
    print("Total Unique To Addresses:", len(set_to))

    if (set_from & set_to):
        print("Total Unique From and To Addresses:", len(set_from & set_to))


def createCountTxns(filename):
    csv.field_size_limit(sys.maxsize)
    # fraud = ['0x226c98fba127213154a121e9ebcfe73236e6f0dd', '0x0902077c90a7ab86d729d74124873b527cd9085b', '0xaea3846e14bec1ba8f562844d39b1215a1d588c6', '0xef57aa4b57587600fc209f345fe0a2687bc26985']
    # txns = {}
    linecount = 0
    to_addr = []
    from_addr = []
    # count transactions between addresses
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if linecount == 0:
                linecount += 1
                continue
            # linecount += 1
            if row[5] and row[6]:
                from_addr.append(row[5])
                to_addr.append(row[6])


    print("Total From Addresses:", len(from_addr))
    print("Total To Addresses:", len(to_addr))
    set_from = set(from_addr)
    set_to = set(to_addr)

    print("Total Unique From Addresses:",len(set_from))
    print("Total Unique To Addresses:", len(set_to))

    if (set_from & set_to):
        print("Total Unique From and To Addresses:", len(set_from & set_to))

    '''
            if txn_addr in txns:
                txns[txn_addr] += 1
            else:
                txns[txn_addr] = 1

    sortedtxns = sorted(txns, key=txns.__getitem__)

    for entry in sortedtxns:
        if txns[entry] > 1:
            print(entry, ":", txns[entry])
    '''



# createSmallerFile(num_lines=1000)
big = 'eth_txs_201901.csv'
small = 'ethtxs_1_1001.csv'
# createCountTxns(big)
countAddresses(big)
