#!/usr/bin/env python3

from __future__ import print_function

import sys
import MySQLdb
import bcrypt

## NEED TO INSTALL mysqlcient and bcrypt (pip install 'name') ON PYTHON VERSION 3.6

# prints out the results contained in the cursor from a given query
def execute_print_results(cursor, sql_query, number_of_columns, header, params=None):
    cursor.execute(sql_query, params)
    print("\n" + header)
    for i in range(cursor.rowcount):
        row = cursor.fetchone()
        if row is None:
            break
        result = ""
        for j in range(number_of_columns):
            result += str(row[j])
            result += " "
        print(result)

def get_options(cursor, number_of_columns, column_names, table):
    print ("Options:")
    options = """
    SELECT {}
    FROM {};
    """.format(column_names, table)
    execute_print_results(cursor, options, number_of_columns, column_names)

def main():
    try:
        # connect to mysql db
        db = MySQLdb.connect(user="root", db="qwiktix")

        with db:
            cursor = db.cursor()
            continuing = True
            while continuing == True:
                print("\nAvailable Queries: ")
                print("1.  Record that a user loves a movie\n" +
                "2.  Provide a ranked list of revenue generated from the top-10 studios\n" +
                "3.  Find all movies directed by the person with the inputted last name\n" +
                "4.  Register a new user\n" +
                "5.  Order a ticket from a local theatre\n" +
                "6.  Credit an existing actress for a movie\n" +
                "7.  Get movie names and images ordered by a particuar user\n" +
                "8.  Get movies a user has loved but not ordered\n" +
                "9.  Find all people credited for a particular movie\n" +
                "10. Provide a ranked list of revenue generated from the top-3 movie genres\n" +
                "11. Find a given directors popularity in each genre that they have directed a movie\n" +
                "12. Compare streaming and theatre revenues over time\n" +
                "13. Find the genres with the greatest streaming revenue for a given city.\n" +
                "14. Show if love for a streaming service's movies leads to higher revenues.\n" +
                "15. Find users for a given city that have been inactive on the platform\n")
                query_num = int(input("Which query do you want to do? "))
                print()
                params = {}

                #Task: Record that a user loves a movie
                if query_num == 1:
                    get_options(cursor, 2, "MovieID, Name", "movie")
                    params['movie_id'] = int(input("Enter the ID for the movie: "))
                    get_options(cursor, 3, "UserID, FName, LName", "user")
                    params['user_id'] = int(input("Enter the ID for the user: "))
                    check = """
                    SELECT *
                    FROM search
                    WHERE search.MovieID=%(movie_id)s
                    AND search.UserID=%(user_id)s;
                    """
                    cursor.execute(check, params)
                    if cursor.rowcount > 0:
                        sql = """UPDATE search
                        SET Love = 1
                        WHERE search.MovieID=%(movie_id)s
                        AND search.UserID=%(user_id)s;"""
                    else:
                        sql = """
                        INSERT INTO search(MovieID, UserID, Love)
                        VALUES (%(movie_id)s, %(user_id)s, 1)
                        """
                    execute_print_results(cursor, sql, 0, "User's Love Recorded", params)

                #Task: Ranked list of revenue from top 10 studios
                elif query_num == 2:
                    sql = """SELECT SUM(userorder.Total) AS Revenue, movie.Studio AS Studio
                    FROM userorder INNER JOIN movie ON userorder.MovieID = movie.MovieID
                    GROUP BY movie.Studio
                    ORDER BY Revenue DESC
                    LIMIT 10;"""
                    execute_print_results(cursor, sql, 2, "Results:")

                #Task: Movies directed by a specific person
                elif query_num == 3:
                    get_options(cursor, 1, "LName",
                    """person INNER JOIN role
                    ON person.PersonID = role.PersonID
                    WHERE role.Title = 'Director'""")
                    params['last_name'] = input("Enter the director's last name: ")
                    sql = """SELECT movie.Name
                    FROM ((movie INNER JOIN role ON role.MovieID  = movie.MovieID)
                    INNER JOIN person ON person.personID = role.PersonID)
                    WHERE person.LName = %(last_name)s AND role.Title='Director'"""
                    execute_print_results(cursor, sql, 1, "Results:", params)

                #Task: Register a new user
                elif query_num == 4:
                    params['email'] =  input("Enter the user's email: ")
                    params['f_name'] = input("Enter the user's first name: ")
                    params['l_name'] =  input("Enter the user's last name: ")
                    salt = bcrypt.gensalt()
                    params['password'] = bcrypt.hashpw(
                    input("Enter the user's pasword: ").encode(),
                    salt).decode()
                    params['salt'] = salt.decode()
                    params['phone'] =  input("Enter the user's phone number: ")
                    params['city'] =  input("Enter the user's city: ")
                    params['street'] =  input("Enter the user's street: ")
                    params['country'] =  input("Enter the user's country: ")
                    params['postal_code'] =  input("Enter the user's postal code: ")
                    sql = """INSERT INTO user(Email, FName, LName, Password, Salt,
                    Phone, City, Street, Country, Postal)
                    VALUES (%(email)s, %(f_name)s, %(l_name)s, %(password)s, %(salt)s,
                    %(phone)s, %(city)s, %(street)s, %(country)s, %(postal_code)s)"""
                    execute_print_results(cursor, sql, 0, "Table Updated", params)

                #Task: Order a ticket from a local theater
                elif query_num == 5:
                    get_options(cursor, 3, "UserID, FName, LName", "user")
                    print()
                    params['user_id'] = input("Enter the user's id: ")

                    get_options(cursor, 2, "MovieID, Name", "movie")
                    print()
                    params['movie_id'] = input("Enter the movie id: ")

                    get_options(cursor, 3,
                                "t.VendorID, v.Name, v.PricePerMovie",
                                "vendor v JOIN theatre t ON v.VendorID = t.VendorID")
                    print()
                    params['vendor_id'] = input("Enter the vendor id: ")
                    get_price = """
                    SELECT vendor.PricePerMovie
                    FROM vendor
                    WHERE VendorID = %(vendor_id)s
                    """
                    cursor.execute(get_price, params)
                    row = cursor.fetchone()
                    number_of_tickets = int(input("Enter number of tickets: "))
                    params['total'] = int(row[0]) * number_of_tickets

                    add_order = """
                    INSERT INTO userorder (UserID, MovieID, Total, PurchaseDate)
                    VALUES (%(user_id)s, %(movie_id)s, %(total)s, CURRENT_TIMESTAMP);
                    """
                    cursor.execute(add_order, params)
                    cursor.execute("SELECT LAST_INSERT_ID();")
                    order_id = cursor.fetchone()[0]

                    add_ticket_order =  """
                    INSERT INTO ticket (OrderID, VendorID)
                    VALUES (%s, %s)
                    """
                    execute_print_results(cursor, add_ticket_order, 0, "Tickets Purchased", (order_id, params['vendor_id']))

                    for i in range(number_of_tickets):
                        add_ticket = """
                        INSERT INTO ticketnumbers (OrderID, TicketNum)
                        VALUES (%s, %s)
                        """
                        cursor.execute(add_ticket, (order_id, i+1))

                #Task: Credit an Existing Actress for a movie
                elif query_num == 6:
                    get_options(cursor, 2, "MovieID, Name", "movie")
                    params['movie_id'] = input("Enter the movie id: ")
                    get_options(cursor, 3, "PersonID, FName, LName", "person")
                    params['person_id'] = input("Enter the person ID for this actress: ")
                    params['character_name'] = input("Enter the name of the character this actress played: ")
                    params['picture'] = input("Submit file path of a picture of the character this actress played: ")
                    with open(params['picture'], "rb") as file:
                        params['picture'] = file.read()
                        file.close()
                    sql = """INSERT INTO role(MovieID, Title, AssocPic, CharacterName, PersonID)
                    VALUES (%(movie_id)s, 'Actress', %(picture)s, %(character_name)s, %(person_id)s)"""
                    execute_print_results(cursor, sql, 0, "Actor Creditted", params)

                #Task: Movie Names and Images Ordered By a Particular User
                elif query_num == 7:
                    get_options(cursor, 3, "UserID, FName, LName", "user")
                    params['user_id'] = input("Enter the user's id: ")
                    sql = """SELECT DISTINCT m.CoverImg,  m.Name
                    FROM movie m
                    INNER JOIN userorder ON userorder.MovieID = m.MovieID
                    INNER JOIN user ON user.UserID = userorder.UserID
                    WHERE user.UserID = %(user_id)s"""
                    cursor.execute(sql, params)
                    for i in range(cursor.rowcount):
                        row = cursor.fetchone()
                        if row is None:
                            break
                        with open(row[1]+".jpeg", "wb") as file:
                            file.write(row[0])
                            file.close()
                    print("Images Saved to Current Directory")

                #Task: Movies a user has loved but not ordered
                elif query_num == 8:
                    get_options(cursor, 3, "UserID, FName, LName", "user")
                    user_id = int(input("Enter the user's id: "))
                    sql = """SELECT movie.name
                    FROM ((movie INNER JOIN search ON movie.movieID = search.movieID)
                    INNER JOIN user ON user.UserID = search.UserID)
                    WHERE search.Love = 1 AND user.UserID = %s AND movie.ReleaseDate LIKE '2018%%'
                    AND movie.name NOT IN(
                    SELECT movie.name
                    FROM ((movie INNER JOIN userorder ON movie.movieID = userorder.movieID)
                    INNER JOIN user ON user.UserID = userorder.UserID)
                    WHERE user.UserID = %s AND movie.ReleaseDate LIKE '2018%%');"""
                    execute_print_results(cursor, sql, 1,  "Results:", (user_id, user_id))

                #Task: Find all people (name, picture, and role) credited for a particular movie (supplied by name)
                elif query_num == 9:
                    get_options(cursor, 1, "Name", "movie")
                    params['movie_name'] = input("Enter the name of the movie: ")
                    sql = """SELECT p.FName, p.LName, p.Picture, r.CharacterName
                    FROM (Person p INNER JOIN Role r ON p.PersonID = r.PersonID) INNER JOIN Movie m ON m.MovieID = r.MovieID
                    WHERE m.Name = %(movie_name)s;"""
                    cursor.execute(sql, params)
                    for i in range(cursor.rowcount):
                        row = cursor.fetchone()
                        if row is None:
                            break
                        print(row[0]+ " " + row[1] + " " + row[3])
                        with open(row[1]+".jpeg", "wb") as file:
                            file.write(row[2])
                            file.close()

                #Task: Provide a ranked list of revenue generated from the top-3 movie genres
                elif query_num == 10:
                    sql = """SELECT m.Genre AS genre, SUM(uo.Total) AS revenue
                    FROM Movie m INNER JOIN UserOrder uo ON m.MovieID = uo.MovieID
                    GROUP BY m.genre
                    ORDER BY revenue DESC
                    LIMIT 3;"""
                    execute_print_results(cursor, sql, 2, "Results", params)

                # Report: find a given directors popularity in any each genre that they have directed a movie
                # by using the number of times the movies in each genre were loved by users.
                elif query_num == 11:
                    get_options(cursor, 2, "FName, LName", "person")
                    params['f_name'] = input("Enter the person's first name: ")
                    params['l_name'] = input("Enter the person's last name: ")
                    sql = """
                    SELECT movie.Genre AS genre, COUNT(*) AS timesLoved
                    FROM ((movie JOIN search ON movie.MovieID = search.MovieID)
                    JOIN role ON movie.MovieID = role.MovieID)
                    JOIN person ON role.PersonID = person.PersonID
                    WHERE person.FName = %(f_name)s AND person.LName = %(l_name)s AND role.Title = "Director" AND search.Love = 1
                    GROUP BY genre
                    HAVING timesLoved > 0
                    ORDER BY timesLoved DESC
                    """
                    execute_print_results(cursor, sql, 2, "Results:", params)

                # Report: compare streaming and theatre revenues over time
                elif query_num == 12:
                    sql = """
                    SELECT t.purchaseYear AS purchaseYear, t.revenue AS ticketRevenue, s.revenue AS streamingRevenue
                    FROM (
                    SELECT YEAR(userorder.PurchaseDate) AS purchaseYear, SUM(userorder.Total) AS revenue
                    FROM userorder JOIN ticket ON userorder.OrderID = ticket.OrderID
                    GROUP BY purchaseYear
                    ) t JOIN (
                    SELECT YEAR(userorder.PurchaseDate) AS purchaseYear, SUM(userorder.Total) AS revenue
                    FROM userorder JOIN streaming ON userorder.OrderID = streaming.OrderID
                    GROUP BY purchaseYear
                    ) s ON t.purchaseYear = s.purchaseYear
                    ORDER BY purchaseYear ASC
                    """
                    execute_print_results(cursor, sql, 3, "Year, Ticket Revenue, Streaming Revenue")

                # Report: find the genres with the greatest streaming revenue for a given city
                elif query_num == 13:
                    get_options(cursor, 2, "City", "user")
                    params['city'] = input("Enter the user's city name: ")
                    sql = """
                    SELECT movie.Genre AS genre, FORMAT(SUM(userorder.Total), 2) AS revenue
                    FROM ((userorder JOIN movie ON userorder.MovieID = movie.MovieID)
                    JOIN user ON userorder.UserID = user.UserID)
                    JOIN streaming ON userorder.OrderID = streaming.OrderID
                    WHERE user.City = %(city)s GROUP BY genre HAVING revenue < 1000
                    ORDER BY revenue DESC
                    """
                    execute_print_results(cursor, sql, 2, "Results", params)

                # Report: show if love for a streaming service's movies leads to higher revenues
                elif query_num == 14:
                    sql = """
                    SELECT vendor.name AS name, COUNT(*) AS numberLoved, FORMAT(sum(userorder.Total), 2) AS revenue
                    FROM (((vendor JOIN streaming ON vendor.VendorID = streaming.VendorID)
                    JOIN userorder ON streaming.OrderID = userorder.OrderID)
                    JOIN movie ON userorder.MovieID = movie.MovieID)
                    JOIN search ON movie.MovieID = search.MovieID
                    WHERE search.Love = 1
                    GROUP BY name
                    ORDER BY numberLoved DESC, revenue DESC
                    """
                    execute_print_results(cursor, sql, 3, "Results:")

                # Report: find users for a given city that have been inactive on the platform
                elif query_num == 15:
                    get_options(cursor, 2, "City", "user")
                    params['city'] = input("Enter the desired city: ")
                    sql = """
                    SELECT DISTINCT(user.UserId) AS user_id
                    FROM user
                    WHERE user.City = %(city)s
                    NOT IN (
                    SELECT DISTINCT(user.UserID) AS user_id
                    FROM userorder JOIN ticket ON userorder.OrderID = ticket.OrderID
                    JOIN user ON user.UserID = userorder.UserID
                    UNION
                    SELECT DISTINCT(user.UserID) AS user_id
                    FROM search JOIN user ON search.UserID = user.UserID
                    WHERE search.Love = 1
                    )
                    """
                    execute_print_results(cursor, sql, 1, "Results:", params)

                # check if the user would like to process another query
                user_continuing = input("\nWould you like to process another query (Y/N): ")
                continuing = user_continuing.upper() == "Y"

    except MySQLdb.Error as err:
        print("Error connecting to db: {}".format(err))

if __name__ == "__main__":
    main()
