import os


if __name__ == "__main__":
    creators={}
    posts=[]
    with open("text.txt","r", encoding="UTF-8") as input:
        texts = input.read().lower().split("\n")          
        
    for lines in texts:
        lines=lines.lower()
        line = lines.split("---")
        try:
            posts=[line[0], line[1], line[2],line[3]]
            if line[2].split(",")[0] not in creators.keys():
                creators[line[2].split(",")[0]] = posts
            else:
                creators[line[2].split(",")[0]] += posts
        except IndexError as IndexError:
            print("Index Error @ " + posts[0]+ " with: ")
                     
    with open("casino_analysis.txt", "w", encoding="UTF-8") as clear:
        clear.write("")
    query= "casino"
    with open("casino_analysis.txt", "a", encoding="UTF-8") as casino:
        for creator in creators:
            for post in range(len(creators[creator])//4):
                buffer_0=0
                buffer_0+=creators[creator][post*4+3].count(query)
                if buffer_0>0:
                    casino.write(creator+" HAS WRITTEN " + str(buffer_0) + " in this " + str(creators[creator][post*4]) + " article" +" about: " + query + "\n")

    with open("output.txt", "w", encoding="UTF-8") as clear:
        clear.write("")
    with open("output.txt", "a", encoding="UTF-8") as out:
        for creator in creators:
            buffer_1=[]
            for i in range(len(creators[creator])//4):
                buffer_1.append(creators[creator][i*4])
            out.write(creator + " HAS WRITTEN: " + str(len(creators[creator])//4) + " ID's: " + str(buffer_1) + "\n")
