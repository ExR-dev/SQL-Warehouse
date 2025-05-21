import dbcmd
import database
import menu

if __name__ == "__main__":
    # Initialize the database
    db = database.Database("warehouseDatabase")

    devmode = menu.main_menu(db)
    
    if devmode:
        print("Entered dev mode")
        while db.is_open():
            try:
                cmd_in = input("> ")
            except:
                print("\nError: Closing Database...")
                db.close()
                break

            dbcmd.exec_cmd(db, cmd_in)
            print(" ")
    else:
        print("Closing Database")
        db.close()