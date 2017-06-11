import psycopg2
#for some reason this is not working - potentially because the postgreSQL implementation has a different path which is
# "/Applications/Postgres.app/Contents/Versions/9.6/bin/psql" -p5432 -d "snippets"
import logging
import argparse

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")

def put(name, snippet):
	"""Store a snippet with an associated name."""
	logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
	cursor = connection.cursor()
	# command = "insert into snippets values (%s, %s)"
	command = "insert into snippets values('{0}', '{1}')".format(name, snippet)
	# apparently this is old style language?  Can we express as .format notation?
	cursor.execute(command)
	connection.commit()
	logging.debug("Snippet stored successfully.")
	return name, snippet

def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return '404: Snippet Not Found'.

    Returns the snippet.
    """
    logging.info("Retrieve snippet associated with name: {!r})".format(name))
    cursor = connection.cursor()
    command = "select message from snippets where keyword='{0}'".format(name)
    cursor.execute(command)
    #i stole this from online but I have no idea why i'm trying to find a tuple here
    # if i understand correctly here i am creating the command cursor.execute("select message from snippets where keyword='name'")
    # which makes sense, but why a tuple?  Why won't (command, (name)) work?
    logging.debug("Snippet retrieved successfully") 
    if 1==False:
    ## need to fix this
     	return cursor.fetchone()
    else:
    	return cursor.fetchone()
    # also this returns a tuple e.g. against 'dogs' in my database returns ('woof',) instead of just 'woof'

def view_all():
	"""
	Views all the current snippets saved and their associated names
	"""
	logging.info("Retrieve all snippets")
	cursor = connection.cursor()
	command = "select * from snippets"
	cursor.execute(command)
	return cursor.fetchall()

def search(string):
	"""
	Allows search of all saved snippets and names 

	Returns all snippets containing the string entered

	If there is no such snippet, return 'No snippets found'
	"""
	logging.info("Search all snippets to find related snippets to string")
	cursor = connection.cursor()
	command = "select * from snippets where keyword like '%{0}%'".format(string)
	cursor.execute(command)
	logging.debug("Snippet/s retrieved successfully")
	return cursor.fetchall()

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    #subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of the snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
	#subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="Name of the snippet")

    #I guess this is a subparser for the view all command
    logging.debug("Constructing the parser for view_all")
    get_parser = subparsers.add_parser("view_all", help="See all snippets stored in the table")

    #and the subparser for the search command
    logging.debug("Constructing search subparser")
    get_parser = subparsers.add_parser("search", help="Search all snippets for a string")
    get_parser.add_argument("string", help="String to search for")

    arguments = parser.parse_args()
    # convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
    	name, snippet = put(**arguments)
    	print ("Stored {!r} as {!r}".format(snippet,name))

    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet[0]))
        # see comment above on tuple

    elif command == "view_all":
    	snippet = view_all(**arguments)
    	print ("Retrieved all available snippets")
    	print (snippet)

    elif command == "search":
    	snippet = search(**arguments)
    	print ("Retrieved all related snippets")
    	print (snippet)

if __name__ == "__main__":
    main()
