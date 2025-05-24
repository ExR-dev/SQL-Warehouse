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
        "- quit \nReturn to the simple interface",
        "- save \nSave the database",
        "- print [<table>] [<columns>] \nPrint a specific table, specific columns, or all tables if no parameters are given",
        "- sql <query> \nExecute a raw SQL query",
        "- insert <table> <values> \nInsert a row into a table",
        "- drop [<tables>] \nDrop the entire database or specific tables",
        "- devDB \nDrop the entire database and create a new one with pre-defined data",
        # ...
    )

    print("\n\n".join(cmd_names))
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
    
    return "quit"

def cmd_print(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "print") or (cmd == "p"):
        passed = True

    if not passed:
        return False

    # Handle the print command
    if len(params) < 1: # Print all tables
        for tbl in ["Warehouse", "Supplier", "Product", "Stock", "ToRestock"]:
            print(f"\n{tbl}:")
            db.print_table(tbl, None)
    else: # Print specific table
        table = params[0]
        columns = params[1:] if len(params) > 1 else None

        db.print_table(table, columns)
    return True

def cmd_sql(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "sql"):
        passed = True

    if not passed:
        return False

    # Handle the SQL command
    if len(params) != 1:
        print("Usage: sql <query>")
        return True

    query = params[0]

    try:
        for result in db.cursor.execute(query, multi=True):
            if result.with_rows:
                rows = result.fetchall()
                for row in rows:
                    print(row)
    except Exception as e:
        print(f"SQL Error: {e}")

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

def cmd_drop(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "drop"):
        passed = True

    if not passed:
        return False

    if len(params) == 0:
        db.cursor.execute(f"DROP DATABASE IF EXISTS {db.db_name};")
        print(f"Database dropped.")
        db.close()
    else:
        for i in range(len(params)):
            params[i] = params[i].strip()
            table = params[0].lower()
            db.cursor.execute(f"DROP TABLE IF EXISTS {table};")
            print(f"Table {table} dropped.")
    return True

def cmd_devDB(db: database.Database, cmd: str, params: list[str]) -> bool:
    # Check if the string executes this command
    passed = False
    if (cmd == "devdb"):
        passed = True

    if not passed:
        return False
    
    confirm = False
    if not confirm:
        print("Performing this operation will drop the database and initialize a standardized database for testing purposes.")
        print("All data currently stored in the database will be lost forever!")
        print("Are you sure you want to do this? (y/n)")
        while not confirm:
            confirm_in = input().lower()
            if confirm_in == "y":
                confirm = True
            elif confirm_in == "n":
                break

    if confirm:
        db.cursor.execute(f"DROP DATABASE IF EXISTS {db.db_name};")
        #db.close()
        db.init()

        exec_str = """
        INSERT INTO Warehouse (address) VALUES 
        ('Karlskrona'),
        ('Karlshamn'),
        ('Stockholm North'),
        ('Stockholm West'),
        ('Malmö'),
        ('Gothenburg');
        """
        for ret in db.cursor.execute(exec_str, multi=True):
            pass

        exec_str = """
        INSERT INTO Supplier (address, contact) VALUES 
        ('Ericsson', '+46722185976'),
        ('Volvo Cars', 'volvo.cars@email.de'),
        ('Steam Software', 'gaben@valvesoftware.com'),
        ('Fortum', 'Carrier Pigeon'),
        ('IKEA', '+46752345056'),
        ('Raccoon', 'Any Trashcan');
        """
        for ret in db.cursor.execute(exec_str, multi=True):
            pass

        exec_str = """
        INSERT INTO Product (sup_ID, description) VALUES 
        (1, 'Telephone'),
        (2, 'EX30'),
        (2, 'XC60'),
        (2, 'V60'),
        (3, 'Key'),
        (1, 'Software'),
        (1, '5G'),
        (5, 'Table'),
        (5, 'Chair'),
        (5, 'Meatballs'),
        (5, 'Blåhaj'),
        (6, 'Rabies'),
        (6, 'Trash'),
        (3, 'Half-Life 3');
        """

        for ret in db.cursor.execute(exec_str, multi=True):
            pass

        exec_str = """
        INSERT INTO Stock (WH_ID, prod_ID, quantity, minQuantity) VALUES 
        (1, 1, 450, 100),
        (1, 6, 999, 1000),
        (5, 6, 4264, 1000),
        (1, 7, 4, 5),
        (3, 7, 9999999, 100),
        (4, 7, 99999, 70),
        (5, 7, 30, 50),
        (3, 6, 4842, 100000),
        (6, 1, 50, 420),
        (4, 1, 6, 999994),
        (5, 3, 0, 500),
        (6, 3, 749, 750),
        (1, 3, 80, 10),
        (4, 12, 123456, 0),
        (3, 12, 77777, 1),
        (4, 13, 75766, 99999),
        (3, 13, 99998, 99999),
        (5, 11, 5, 0),
        (6, 11, 8999, 9999),
        (3, 11, 540, 999),
        (3, 1, 1000, 500),
        (3, 2, 200, 100),
        (1, 2, 36, 20),
        (4, 2, 101, 80),
        (3, 10, 20, 10),
        (6, 10, 10, 20);
        """

        for ret in db.cursor.execute(exec_str, multi=True):
            pass

        # Modify some existing ToRestock entries to move their dateAdded back in time
        exec_str = """
        UPDATE ToRestock SET dateAdded = '2024-09-04' WHERE stock_ID = 2;
        UPDATE ToRestock SET dateAdded = '2025-01-24' WHERE stock_ID = 4;
        UPDATE ToRestock SET dateAdded = '2025-04-01' WHERE stock_ID = 7;
        UPDATE ToRestock SET dateAdded = '2023-12-31' WHERE stock_ID = 8;
        UPDATE ToRestock SET dateAdded = '2022-08-09' WHERE stock_ID = 10;
        UPDATE ToRestock SET dateAdded = '2025-04-01' WHERE stock_ID = 16;
        UPDATE ToRestock SET dateAdded = '2025-05-23' WHERE stock_ID = 20;
        UPDATE ToRestock SET dateAdded = '2020-10-15' WHERE stock_ID = 26;
        """

        for ret in db.cursor.execute(exec_str, multi=True):
            pass

        exec_str = """
        INSERT INTO ToRestock (stock_ID, dateAdded, dateOrdered, orderCount) VALUES
        (2, '2022-05-03', '2023-12-04', 100),
        (10, '2020-11-01', '2021-12-01', 400),
        (3, '2023-10-02', '2023-10-14', 2000),
        (7, '2023-10-02', '2023-10-14', 2),
        (1, '2020-01-01', '2025-04-13', 600),
        (18, '2023-10-20', '2023-12-23', 8),
        (18, '2023-12-25', '2024-12-20', 90),
        (19, '2019-02-19', '2019-02-21', 1),
        (19, '2019-02-22', '2019-02-23', 1500),
        (19, '2019-02-24', '2020-06-02', 9999),
        (19, '2024-08-17', '2024-08-20', 300),
        (8, '2021-07-30', '2021-08-07', 100),
        (20, '2023-10-22', '2023-10-22', 12);
        """

        for ret in db.cursor.execute(exec_str, multi=True):
            pass

        print("Testing Database initialized successfully.")
    else:
        print("Aborted.")
    
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
    """
    Execute a command on the database.

    :param db: Database object
    :param cmd_in: Input command string
    """
    func_list = [
        cmd_help,
        cmd_quit,
        cmd_save,
        cmd_print,
        cmd_sql,
        cmd_insert,
        cmd_drop,
        cmd_devDB,
        # ...
        cmd_null
    ]

    cmd_parsed = parse_cmd(cmd_in)
    if cmd_parsed[0] == "sql":
        # If the command is SQL, we don't need to parse it
        cmd_sql(db, "sql", [cmd_in[4:]])
        return

    for cmd_func in func_list:
        ret = cmd_func(db, cmd_parsed[0], cmd_parsed[1])

        if ret == False or ret == None: # input did not trigger command
            continue
        elif ret == True: # input triggered command, skip the rest
            break
        elif ret == "quit":
            return "quit"
    return None