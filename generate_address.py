# This file generates a list of addresses from the national address database.
# https://www.transportation.gov/mission/open/gis/national-address-database/national-address-database-nad-disclaimer
# My hometown participates in the NAD, so I used the NAD to generate a list of addresses in my hometown.
# It included the lat / long as well as the physical address, this was run once to generate the normal.txt file. 

addy = open("./TXT/NAD.txt", "r") 
normal = open("./TXT/normal.txt", "w")
last_line = ""
# for loop for each line of the file:
count = 0
for l in addy:
    count += 1
    try:
        fields = l.split(",")
        if count % 100000 == 0:
            print(count + ": " + fields[33] + ", " + fields[23])
        if fields[33] == "IL":
            if fields[23] == "NORMAL":
                line = (fields[2] + fields[3].lower() + " " + fields[13].lower() + ", " + fields[23].lower() + ", " + fields[33].upper() + " " + fields[34] + ": " + fields[39] + ", " + fields[40] + "\n")
                if line != last_line:    
                    print(line)
                    normal.write(line)
                last_line = line
    except: 
        pass

addy.close()
normal.close()