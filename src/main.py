import dbcmd
import interface
import database

if __name__ == "__main__":
    # Initialize the database
    db = database.Database("warehouseDatabase")

    if db.is_open():
        interface.menu_main(db)
        
    db.close()

