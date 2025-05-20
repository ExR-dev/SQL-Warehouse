import dbcmd
import database

if __name__ == "__main__":
    # Initialize the database
    db = database.Database("warehouseDatabase")

    while db.is_open():
        try:
            cmd_in = input("> ")
        except:
            print("\nError: Closing Database...")
            db.close()
            break

        dbcmd.exec_cmd(db, cmd_in)
        print(" ")
