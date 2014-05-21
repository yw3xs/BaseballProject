# will get stuff from mlbstartingnine and make it usable by excel

replace_this = "<br />"
fend = 'LineUp_20140516.txt'
raw_txt = []

with open("data20140516.txt", "r+") as file:
    raw_txt = file.readlines()
    #for line in file.readlines():
    #   raw_txt.extend(line)
        
for line in raw_txt:
    print line
    new_txt = line.replace(replace_this, "\n")
    new_file = raw_input("type the name of the team: ")
    fname = new_file + fend
    with open(fname, "w") as file:
        file.write(new_txt)
    
    with open(fname, "r") as file:
        lst = file.readlines()

    with open(fname, "w") as file:
        for elem in lst:
            line = elem.strip() + '\n'
            file.write(line)

