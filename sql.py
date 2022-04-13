import os

with open("text08-11-2021.txt","r",encoding="UTF-8") as input:
    leserbriefe = input.read().split("\n")

with open("out_sql.txt","w",encoding="UTF-8") as out:
    for line in leserbriefe:
        item=line.split("---")
        print(item[0])
        out_put="INSERT INTO Leserbriefe VALUES (\'"+str(int(item[0]))+"\',\'"+str(item[1])+"\',\'"+str(item[2].split("|")[0])+"\',\'"+str(item[2].split("|")[1])+"\',\'"+str(item[3])+"\');"
        out.write(out_put+"\n")
    