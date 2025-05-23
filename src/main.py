import dbcmd
import database

if __name__ == "__main__":
    # Initialize the database
    db = database.Database("warehouseDatabase")

    if True:
        import menu

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
    else:
        import interface
        
        if db.is_open():
            interface.menu_main(db)
        
    db.close()

