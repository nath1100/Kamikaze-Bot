import msvcrt

LOG_FILE = "discord.log"
ENCODING = 'utf-8'

def loadFile():
    print("Loading log file...")
    with open(LOG_FILE, 'r', encoding=ENCODING) as f:
        data = f.read().split("\n")
    print("Finished loading.")
    DATA_LENGTH = len(data) - 1
    print("{} lines detected".format(DATA_LENGTH - 1)) #ord("\n") == 10
    return (data, DATA_LENGTH)

def outputLine(data, line : int, inpt : str):
    """Takes a list of lines, outputs specified lines"""
    if inpt == 75 and line > 0:
        line -= 1
    elif inpt == 77 and line < DATA_LENGTH:
        line += 1
    # type display
    contentType = "No type"
    for x in data[line].split(','):
        if x.startswith(" 't':"):
            contentType = x
    return (data[line], line, contentType)

COMMANDS = [75, 77, 114]

data, DATA_LENGTH = loadFile()
line = DATA_LENGTH # start from the end

# main line
while True:
    print("\n{}> ".format(line - 1))
    choice = ord(msvcrt.getch())
    if choice not in COMMANDS:
        print('\n'*100 + 'Use the left and right arrow keys to navigate.\nR key to reload log file.')
    elif choice == ord('r'):
        data, DATA_LENGTH = loadFile()
    else:
        content, lineNumber, contentType = outputLine(data, line, choice)
        print("{}{}\n\n{}".format("\n"*100, contentType, content))
        line = lineNumber
