import msvcrt, json

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
    content_type = "No type"
    print("Data:::\n" + data[line])
    # Check if readable content
    key = "WebSocket Event: "
    if key in data[line]:
        # Remove header info and replace single quotes with double quotes, as well as None -> null
        #pruned_data = data[line][data[line].index(key)+len(key):].replace('"',"<<<DOUBLEQUOTE>>>").replace("'",'"').replace("<<<DOUBLEQUOTE>>>","'").replace(": None",": null")
        pruned_data = dict([entry.split(":") for entry in data[line][data[line].index(key)+len(key):].split(",")])
        # Create dict 
        pruned_data = json.loads(pruned_data)
        print(pruned_data)
        try:
            content_type = str(pruned_data["t"])
        except KeyError:
            pass
        if content_type == "MESSAGE_CREATE":
            content_type += "\n MESSAGE: {}".format(pruned_data["content"])
    return (data[line], line, content_type)

COMMANDS = [27, 75, 77, 114]

data, DATA_LENGTH = loadFile()
line = DATA_LENGTH # start from the end

# main line
while True:
    print("\n{}> ".format(line - 1))
    choice = ord(msvcrt.getch())
    if choice not in COMMANDS:
        print('\n'*100 + 'Use the left and right arrow keys to navigate.\nR key to reload log file.')
    elif choice == 27:
        print("Closing.")
        break
    elif choice == ord('r'):
        data, DATA_LENGTH = loadFile()
    else:
        content, lineNumber, content_type = outputLine(data, line, choice)
        print("{}Type: {}\n\n{}".format("\n"*100, content_type, content))
        line = lineNumber
