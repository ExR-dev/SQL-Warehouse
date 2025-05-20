import database

# Command-line command functions
def cmd_help(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "help") or (cmd == "h"):
        passed = True
    
    if not passed:
        return False

    cmd_names = (
        "save",
        "quit", 
        "insert",
        "print",
        # ...
    )

    print("\n".join(cmd_names))
    return True

def cmd_save(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "save") or (cmd == "s"):
        passed = True

    if not passed:
        return False

    db.commit()
    print("Database saved.")
    return True

def cmd_quit(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "quit") or (cmd == "exit") or (cmd == "q") or (cmd == "qq"):
        passed = True

    if not passed:
        return False
    
    confirm = (cmd == "qq") or ("y" in params) or ("-y" in params)

    if not confirm:
        print("Are you sure you want to quit? (y/n)")
        while not confirm:
            confirm_in = input().lower()
            if confirm_in == "y":
                confirm = True
            elif confirm_in == "n":
                break

    if confirm:
        print("Closing Database...")
        db.close()
    else:
        print("Quit Aborted.")
    return True

def cmd_print(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "print") or (cmd == "p"):
        passed = True

    if not passed:
        return False

    # Handle the print command
    if len(params) < 1:
        print("Usage: print <table> [<columns>]")
        return True

    table = params[0]
    columns = params[1:] if len(params) > 1 else None

    if columns is not None:
        db.print_table(table, columns)
    else:
        db.print_table(table)

    return True

def cmd_insert(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "insert"):
        passed = True

    if not passed:
        return False

    # Handle the insert command
    if len(params) < 2:
        print("Usage: insert <table> <values>")
        return True

    table = params[0].lower()
    values = params[1:]

    db.insert(table, values)
    return True

def cmd_null(db: database.Database, cmd: str, params: list[str]) -> bool:
    print("Unknown command. Try \"help\" for a list of available commands.")
    return True


def parse_cmd(cmd_in: str) -> tuple[str, list[str]]:
    """
    Parse the input command string into a tuple of command and parameters.

    :param cmd_in: Input command string
    :return: Tuple containing the command and parameters
    """
    params = cmd_in.split(" ")
    cmd = params.pop(0).lower() # Separate the main command from the parameters

    for i in range(len(params)):
        params[i] = params[i].strip()

    # Check if any params include a quotation mark.
    # if so, merge all following commands until the string closes with another quotation mark

    for i in range(len(params)):
        if i >= len(params):
            break

        param = params[i]

        if not param.startswith('"'):
            continue

        merged_param = ""

        str_start = i
        for str_end in range(str_start, len(params)):
            merged_param += params[str_end]

            if not merged_param.endswith('"'):
                merged_param += " "
                continue

            merged_param = merged_param.strip('"')
            params[i] = merged_param

            while str_end > str_start:
                params.pop(str_end)
                str_end -= 1
            break
        
    return (cmd, params)

def exec_cmd(db: database.Database, cmd_in: str) -> None:
    func_list =[
        cmd_help, 
        cmd_quit, 
        cmd_save,
        cmd_print,
        cmd_insert,
        # ...
        cmd_null
    ]

    cmd_parsed = parse_cmd(cmd_in)

    for cmd_func in func_list:
        if cmd_func(db, cmd_parsed[0], cmd_parsed[1]):
            break