import database

# Command-line command functions
def cmd_quit(cmd_in: str, db: database.Database) -> bool:
    params = cmd_in.split(" ")
    cmd = params.pop(0).lower() # Separate the main command from the parameters

    # Check if the string executes this command
    passed = False
    if (cmd == "quit") or (cmd == "exit") or (cmd == "q") or (cmd == "qq"):
        passed = True

    if not passed:
        return False
    
    confirm = ("y" in params) or ("-y" in params) or (cmd == "qq")

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

def cmd_help(cmd_in: str, db: database.Database) -> bool:
    params = cmd_in.split(" ")
    cmd = params.pop(0).lower() # Separate the main command from the parameters

    # Check if the string executes this command
    passed = False
    if (cmd == "help") or (cmd == "h"):
        passed = True
    
    if not passed:
        return False

    cmd_names = (
        "quit", 
        "help", 
        "insert",
        # ...
    )

    print("\n".join(cmd_names))
    return True

    params = cmd_in.split(" ")
    cmd = params.pop(0) # Separate the main command from the parameters

    # Check if the string executes this command
    passed = False
    if (cmd == "help") or (cmd == "h"):
        passed = True
    
    if not passed:
        return False

    cmd_names = (
        "quit", 
        "help", 
        # ...
    )

    print("\n".join(cmd_names))
    return True

def cmd_print(cmd_in: str, db: database.Database) -> bool:
    params = cmd_in.split(" ")
    cmd = params.pop(0).lower() # Separate the main command from the parameters

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

def cmd_insert(cmd_in: str, db: database.Database) -> bool:
    params = cmd_in.split(" ")
    cmd = params.pop(0).lower() # Separate the main command from the parameters

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

    table = params[0]
    values = params[1:]

    db.insert(table, values)
    return True

def cmd_save(cmd_in: str, db: database.Database) -> bool:
    params = cmd_in.split(" ")
    cmd = params.pop(0).lower() # Separate the main command from the parameters

    # Check if the string executes this command
    passed = False
    if (cmd == "save") or (cmd == "s"):
        passed = True

    if not passed:
        return False

    db.commit()
    print("Database saved.")
    return True

def cmd_null(cmd_in: str, db: database.Database) -> bool:
    print("Unknown command. Try \"help\" for a list of available commands.")
    return True


if __name__ == "__main__":
    # Initialize the database
    db = database.Database("warehouse.db")

    cmd_list = [
        cmd_quit, 
        cmd_help, 
        cmd_print,
        cmd_insert,
        cmd_save,
        # ...
        cmd_null
    ]

    while db.is_open():
        try:
            cmd_in = input("> ")
            #cmd_in = input("> ").lower() # Standardize input to lowercase
        except:
            print("\nError: Closing Database...")
            db.close()
            break

        for cmd in cmd_list:
            if cmd(cmd_in, db):
                break
        print(" ")
