import sqlite3

from haversine import haversine, Unit

line = "----------------------------------"


def create_db():
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()

    curs.execute('PRAGMA foreign_keys = ON')

    # Users
    curs.execute('''
      CREATE TABLE IF NOT EXISTS Users (
      Username VARCHAR(20),
      Password VARCHAR(25),
      FirstName VARCHAR(25),
      LastName VARCHAR(25),
      AddressLine1 VARCHAR(25),
      AddressLine2 VARCHAR(25),
      CityTown VARCHAR(25),
      PostalCode VARCHAR(8),
      Car BOOLEAN,
      PRIMARY KEY(Username));
      ''')
    curs.execute('''
          CREATE TABLE IF NOT EXISTS Neighbours (
          NewUsers VARCHAR(20),
          OldUsers VARCHAR(25),
          FOREIGN KEY(NewUsers) REFERENCES Users(Username)
          FOREIGN KEY(OldUsers) REFERENCES Users(Username)
          PRIMARY KEY(NewUsers, OldUsers));
          ''')


def search(table, columns, condition: str):
    print(line)

    str_columns = str(columns).strip(" ()[]").replace("'", "")

    print("Searching...")
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()

    query = f'''
   SELECT {str_columns}
   FROM {str(table)}
   WHERE {str(condition)} ;
   '''

    print(query)

    results = []

    # Try searching...
    try:
        results = curs.execute(query).fetchall()

    except sqlite3.OperationalError:
        print("No results. Try another query.")

    conn.commit()
    conn.close()

    print(line)

    # prints number of results (summary stats)
    no_repeats = set(results)
    print(str(len(no_repeats)) + " results found.")

    return results


def insert(table, values):
    success = False
    print(line)
    # Check input types are valid...
    if not validate_insert(table, values):
        print("Insert unsuccessfull. \n")
        return success

    print("Inserting...")
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()

    query = f'''
      INSERT INTO {str(table)} VALUES
      {str(values)}
      '''

    print(query)

    # Try inserting...
    try:
        curs.execute(query)
        print(table + " was successfully inserted into. \n")
        success = True

    except sqlite3.IntegrityError:
        print("Integrity error. Insert unsuccessful. \n")
        success = False
        # TODO give user more information

    conn.commit()
    conn.close()
    print(line)
    return success


"""def foreign_insert(table, values):
    valid = True

    vals_dict = dict(zip(values, get_attributes(table), strict=True))

    for v, attr in vals_dict.items():
        t = check_foreign(table, attr)  # original table
        if t is not None:
            for p, f in foreign_dict.items():
                if attr == f \
                        and not search(t, p, f'{p} = \'{v}\''):
                    # ...then output error for each invalid foreign key
                    print(p)
                    print(f"{v} does not exist in in {f}'s main table \
{t}. Please enter a valid foreign key value.")
                    valid = False

    return valid"""


# VALIDATION
def validate_insert(table, values):
    # first check types...
    valid = check_types(get_types(table), values)

    if not valid:
        print("Invalid types.")
        return valid

    print("All values are of valid data types. \n")

    # then check foreign keys exist...
    print("Checking foreign keys...")

    # valid = foreign_insert(table, values)

    # then return if valid or not
    return valid


# Checking types n stuff
def check_types(atypes, values) -> bool:
    valid = True
    for (atype, value) in zip(atypes, values, strict=True):
        valid = valid and check_type(atype, value)
    return valid


def check_type(atype, value) -> bool:
    t = atype.strip(")").split("(")[0]
    # print("t: " + t)
    valid = types_dict[t](value, atype)
    return valid


# returns the table the foreign key was refrenced from
def check_foreign(table, column):
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()

    # gets names of table's foreign keys
    columns = [
        f[3] for f in curs.execute(f'''
  PRAGMA foreign_key_list({str(table)})
  ''').fetchall()
    ]

    # gets the table they were originally from
    origins = [
        f[2] for f in curs.execute(f'''
  PRAGMA foreign_key_list({str(table)})
  ''').fetchall()
    ]

    f_keys = dict(zip(columns, origins, strict=True))

    if column in columns:
        # returns the table the foreign key was refrenced from
        return f_keys.get(column)

    return None


# get table info
def get_types(table):
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()

    types = [c[2] for c in \
             curs.execute(f'''
     PRAGMA table_info({table})
    ''').fetchall()]

    conn.close()
    return types


# returns a list of column names of a given table
def get_attributes(table):
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()

    columns = [c[1] for c in \
               curs.execute(f'''
    PRAGMA table_info({table})
    ''').fetchall()]

    conn.close()

    return columns


# TYPE CHECKS
def is_varchar(s, datatype):
    t = datatype.strip(")").split("(")
    data_length = int(t[1])

    rval = len(s) <= data_length
    if not rval:
        print(s + " should be of type " + datatype)

    return rval


"""def is_char(s, datatype):
    t = datatype.strip(")").split("(")
    data_length = int(t[1])

    rval = len(s) == data_length
    if not rval:
        print(s + " should be of type " + datatype)

    return rval
"""

"""def is_int(s, datatype="INT"):
    try:
        int(s)
        return True
    except ValueError:
        print(s + " should be of type " + datatype)
        return False
"""


def is_bool(s, datatype="BOOLEAN"):
    print(s)
    if s is False or s is True:
        return True
    else:
        print(str(s) + " should be of type " + datatype)
        return False


types_dict = {
    "VARCHAR": is_varchar,
    # "CHAR": is_char,
    # "INT": is_int,
    "BOOLEAN": is_bool
}

foreign_dict = {
    # update as needed
}


# main functions to use:
def getLatLong(address):
    # Set your API key here
    API_KEY = 'AIzaSyCX7QD26f7lidyJZfE2fxkGB7lFAv3wjBk'

    # Define the API endpoint
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'

    # Make the API request
    import requests
    response = requests.get(url)
    data = response.json()

    # Parse the response and extract the coordinates
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']
        print(f'Latitude: {latitude}, Longitude: {longitude}')
        return latitude, longitude
    else:
        print('Geocoding failed. Status:', data['status'])
        return None


def calcDistance(coords1, coords2):
    distance = haversine(coords1, coords2, unit=Unit.MILES)
    return distance


def add_user(username, password, fname, lname, addressline1, addressline2, city, pcode, has_car):
    values = (username, password, fname, lname, addressline1, addressline2, city, pcode, has_car)
    fullAddress = f"{addressline1}, {addressline2}, {city}, {pcode}"
    newCoords = getLatLong(fullAddress)
    insert("Users", values)

    address_tuples = search("Users", ("AddressLine1", "AddressLine2", "CityTown", "PostalCode"), f"CityTown='{city}'")
    addresses = []
    for t in address_tuples:
        addresses.append(", ".join(t))
    print("Addresses: " + str(addresses))

    closeAddresses = findNeighbours(newCoords, addresses)
    neighbours = []
    for address in closeAddresses:
        neighbours.append(findResidentID(address))

    print("Neighbours: " + str(neighbours))

    for neighbour in neighbours:
        if neighbour != username:
            add_neighbour(username, neighbour)


def add_neighbour(new_user, old_user):
    check = search("Neighbours", ("NewUsers", "OldUsers"), f"OldUsers = '{new_user}'")
    if len(check) == 0:
        insert("Neighbours", (f"{new_user}", f"{old_user}"))
    else:
        print("Unsuccessful")


def findResidentID(address):  # assuming commas are a reliable seperator
    fields = address.split(", ")
    condition = (f"AddressLine1='{fields[0]}' AND AddressLine2 = '{fields[1]}' AND CityTown = '{fields[2]}' AND "
                 f"PostalCode = '{fields[3]}'")

    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()
    curs.execute(f"SELECT Username FROM Users WHERE {condition}")
    rows = curs.fetchall()
    conn.close()
    return rows[0][0]


def findNeighbours(newCoords, addresses):
    close_addresses = []
    for address in addresses:
        currCoords = getLatLong(address)
        if currCoords is not None and calcDistance(currCoords, newCoords) <= 1:
            close_addresses.append(address)
    print("Close addresses: " + str(close_addresses))
    return close_addresses


def print_table(table_name):
    print()
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()
    #data = curs.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    data = curs.execute(f"SELECT * FROM {table_name};").fetchall()
    conn.close()

    print(table_name + ":")
    print(data)
    # print_data(data, get_attributes(table_name)


def getNeighbourIDs(username):
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()
    curs.execute(f"SELECT OldUsers FROM Neighbours WHERE NewUsers = '{username}'")
    oldusers = curs.fetchall()
    curs.execute(f"SELECT NewUsers FROM Neighbours WHERE OldUsers = '{username}'")
    newusers = curs.fetchall()
    conn.close()
    return oldusers+newusers

def getPersonInfo(username):
    print(username)
    conn = sqlite3.connect("carpooldb.db")
    curs = conn.cursor()
    curs.execute("SELECT FirstName, LastName FROM Users WHERE Username = ?", (username,))
    return curs.fetchall()


# def main():
# create_db()
# print_table("Users")
# print(get_attributes("Users"))
# print(get_types("Users"))
# add_user(("usr", "pass", "first", "last", "al1", "al2", "ct", "pc", False))


create_db()
print_table("Users")

#add_user("tim1", "123", "Timothy", "Jones", "6 Green Park House", "", "Bath", "BA11BQ", False)
#add_user("tom2", "123", "Thomas", "Jeffery", "John Wood Court", "", "Bath", "BA11AG", False)
#add_user("Lee3", "123", "Leeanne", "Rogers", "Carpenter House", "", "Bath", "BA11UB", False)
#add_user("Arr2","123","Arron","Black","11 Regents Court","Uxbridge road","London","HA53LR",False)
#add_user("Tanu1","123","Tanu","Ukidve","Latimer Gardens","Pinner","London","HA53RA",False)