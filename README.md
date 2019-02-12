# The Item Catalog
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fzlav%2FItemCatalog.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fzlav%2FItemCatalog?ref=badge_shield)

The Item Catalog is a shopping catalog that utilizes a python server as well as an sqlite database to track items.

## Installation
Download all the files from the github page https://github.com/zlav/ItemCatalog.git.
Ensure all neccesary packages are installed as well:
* flask
* sqlalchemy
* sqlite
* oauth2client

Using a Vagrant virtual machine is recomended however it is not neccesary.
## Usage
1. Start a UNIX terminal and navigate to the folder containing the package items.
2. Create the Database
    * Run `python database_setup.py` to initialize the database.
    * (Optional) Run ` python database_load` to place a custom set of data into the database.
3.  Start the server
    * Navigate to the folder containing all three files inside of the terminal and enter `python project.py`
        * Default port # is 5000

4. Wokring with the Catalog
    * Navigate to localhost:5000 to access the catalog
    * Login with Facebook or Google using the link on the upper right of the page
    * Once logged in you can add categories and items as well as edit them
        * Only items that you added may be edited

(Both of these options were tested on macOS HighSierra 10.13)

## Debugging and Common Errors
### Server Issues
* Fails to start - Check that all of the neccesary packages are installed.
* Fails when loading a page - Inspect the debugging page and report the problem.

### Browser Issues
* Fails to load after running the server.
    * Ensure you are logging onto the correct port.
    * Check the server debugging information.

### Database Issues
* Data storage issues
    * Database may not have been initialized. Run database_setup.py

## Future Updates
* Shopping cart functionality
* Native login authorization support
* Images for categories and items

## License
GPL



[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fzlav%2FItemCatalog.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fzlav%2FItemCatalog?ref=badge_large)