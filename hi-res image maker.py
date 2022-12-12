from tkinter import *

window = Tk()
c = Canvas(window, width=480,height = 460,bg='black')
c.pack()

grid = []
for i in range(21):
    row = []
    for j in range(24):
        row.append(0)
    grid.append(row)

c.create_text(20,10, text='Create the image',anchor='nw',fill='white',font='Times 15')
for i in range(25):
    c.create_line(i*20,40,i*20,460,fill='white')
    c.create_line(0,(i*20)+40,480,(i*20)+40,fill='white')

# click event
def callback(event):
    print("clicked at", event.x, event.y)

    if event.y >= 40:
        x = event.x // 20
        y = event.y // 20
        if grid[y-2][x] == 0:
            grid[y-2][x] = 1
            c.create_rectangle(x*20,(y*20),(x*20)+20,(y*20)+20,fill='white',outline='white')
        else:
            grid[y-2][x] = 0
            c.create_rectangle(x*20,(y*20),(x*20)+20,(y*20)+20,fill='black',outline='white')

    for row in grid:
        line = ''
        for i in row:
            line += str(i) + ' '
        print(line)

c.bind("<Button-1>", callback)

def generate():
    values = []
    for row in grid:
        for i in range(0,24,8):
            value = 0
            count = 1
            for j in range(7,-1,-1):
                if row[i+j] == 1:
                    value += count
                count *= 2
            values.append(value)
    for value in values:
        print(value)    

    spritenum = int(input('Enter sprite number (0-7): '))
    location = int(input('Enter location in BASIC area to be stored (33-255): '))
    line_data = int(input('Enter starting line number of data (0-32746): '))
    line_code = int(input('Enter starting line of load code (0-32767): '))
    
    colour = int(input('''
Select a colour:
0 - Black
1 - White
2 - Red
3 - Cyan
4 - Purple
5 - Green
6 - Blue
7 - Yellow
8 - Orange
9 - Brown
10 - Pink
11 - Dark Grey
12 - Grey
13 - Light Green
14 - Light Blue
15 - Light Grey

>>> '''))

    ext_x = int(input('Double width? (0/1): '))
    ext_y = int(input('Double height? (0/1): '))
    clr_home = int(input('Clear screen? (0/1): '))
    name = input('Name your image: ')
    
    for i in range(100):
        if i != 0:
            filename = 'GeneratedBASIC (' +str(i)+ ').txt'
        else:
            filename = 'GeneratedBASIC.txt'
        try:
            file = open(filename,'x')
        except:
            continue
        break

    lines = []

    lines.append(str(line_code) + ' rem load '+name+'\n')
    line_code += 1
    if clr_home == 1:
        lines.append(str(line_code) + 'print chr$(147)\n')
        line_code += 1
    lines.append(str(line_code) + ' poke 63,' + str(line_data // 256)+'\n')
    line_code += 1
    lines.append(str(line_code) + ' poke 64,' + str(line_data % 256)+'\n')
    line_code += 1
    lines.append(str(line_code) + ' for i=0to62:read a:poke ' + str(location*64) + '+i,a:next\n')
    line_code += 1
    lines.append(str(line_code) + ' poke ' + str(2040 + int(spritenum)) + ',' + str(location)+'\n')
    line_code += 1
    lines.append(str(line_code) + ' poke ' + str(53287 + spritenum) + ',' + str(colour) + '\n')
    line_code += 1
    if ext_x == 1:
        lines.append(str(line_code) + ' poke 53277,peek(53277)or' + str(2**spritenum) + '\n')
        line_code += 1
    if ext_y == 1:
        lines.append(str(line_code) + ' poke 53271,peek(53271)or' + str(2**spritenum) + '\n')
        line_code += 1
    lines.append(str(line_code) + ' poke 53269,peek(53269)or' + str(2**spritenum) + '\n')
    line_code += 1
    lines.append(str(line_code) + ' poke ' + str(53248 + (2*spritenum)) +',24\n')
    line_code += 1
    lines.append(str(line_code) + ' poke ' + str(53249 + (2*spritenum)) +',50\n')

    file.writelines(lines)

    file.write(str(line_data) + ' rem ' + name + ' data\n')
    line_data += 1
    for i in range(0,63,7):
        linenumber = int(line_data + i/7)
        codeline = str(linenumber) + ' data '
        for j in range(7):
            codeline += str(values[i+j])
            if j != 6:
                codeline += ', '
        codeline += '\n'
        file.write(codeline)




generatebutton = Button(window, activeforeground = 'white', command = generate, text = 'Generate')
generatebutton.place(x = 370, y = 10, width = 100, height = 20)


window.mainloop()