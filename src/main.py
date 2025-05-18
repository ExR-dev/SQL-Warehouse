import database

# Command-line command functions
def cmd_quit(cmd_in: str, db: database.Database) -> bool:
    params = cmd_in.split(" ")
    cmd = params.pop(0) # Separate the main command from the parameters

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

def cmd_null(cmd_in: str, db: database.Database) -> bool:
    print("Unknown command. Try \"help\" for a list of available commands.")
    return True


if __name__ == "__main__":
    # Initialize the database
    db = database.Database("warehouse.db")

    cmd_list = [
        cmd_quit, 
        cmd_help, 
        # ...
        cmd_null
    ]

    while db.is_open():
        try:
            cmd_in = input("> ").lower() # Standardize input to lowercase
        except:
            print("\nError: Closing Database...")
            db.close()
            break

        for cmd in cmd_list:
            if cmd(cmd_in, db):
                break
        print(" ")
