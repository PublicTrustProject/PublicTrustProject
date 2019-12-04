import csv
import checkdmarc

domains = []
nospf = []
nodmarc = []
multidmarc = []
locdmarc = []
spfdmarc = []
yesdmarc = []

line_count = 0

with open('current-full.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        if line_count == 0:
            #print(f'Column names are {", ".join(row)}')
            line_count += 1
        if row["State"] == "NE":
            #print(f'\t{row["Domain Name"]} is in State {row["State"]} .')
            domains.append(row["Domain Name"])
            line_count += 1
    #print(f'Processed {line_count} lines.')

for domain in domains:
    #spf check
    try:
        y = checkdmarc.query_spf_record(domain)
    except checkdmarc.SPFRecordNotFound:
        nospf.append(domain)
    
    #dmarc check
    try:
        z = checkdmarc.query_dmarc_record(domain)
        yesdmarc.append(domain)
    except checkdmarc.DMARCRecordNotFound:
        nodmarc.append(domain)
    except checkdmarc.MultipleDMARCRecords:
        multidmarc.append(domain)
    except checkdmarc.DMARCRecordInWrongLocation:
        locdmarc.append(domain)
    except checkdmarc.SPFRecordFoundWhereDMARCRecordShouldBe:
        spfdmarc.append(domain)

print (f"\n{len(nospf)} of {line_count} have no SPF record:")
for domain in nospf:
    print (domain)

print (f"\n{len(nodmarc)} of {line_count} have no DMARC record:")
for domain in nodmarc:
    print (domain)

print ("\nmulti dmarc records:")
for domain in multidmarc:
    print (domain)

print ("\ndmarc in wrong location:")
for domain in locdmarc:
    print (domain)

print ("\nSPF Where DMARC Should Be:")
for domain in spfdmarc:
    print (domain)

print (f"\n{len(yesdmarc)} of {line_count} do have a dmarc record (P could still be none):")
for domain in yesdmarc:
    print (domain)