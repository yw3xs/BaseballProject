# will get stuff from mlbstartingnine and make it usable by excel

replace_this = "<br />"

with open("data.txt", "r+") as file:
    raw_txt = file.read()
    new_txt = raw_txt.replace(replace_this, "\n")

new_file = raw_input("type the name of the team: ")
fend = 'LineUp_20140420.txt'
fname = new_file + fend

with open(fname, "w") as file:
    file.write(new_txt)
    
with open(fname, "r") as file:
    lst = file.readlines()

with open(fname, "w") as file:
    for elem in lst:
        line = elem.strip() + '\n'
        file.write(line)

