#! /usr/bin/env python

import sqlite3
from datetime import datetime


class Clocker:
    """
    Clocker is a simple utility class for verifing the user names of employees.
    Checking to see if they can clock in/out, and actually clocking them in/out.
    """

    def user_exists(self, user_name, connection):
        """
        Verifies that a user exists.

        Parameters:
            var1 = The user name of the employee to be verified
            var2 = The connection to the database that stores the employee user names

        Returns:
            True if the user name exists and false otherwise.
        """

        cur = connection.cursor()

        try:
            cur.execute('SELECT *\
                         FROM employee\
                         WHERE user_name = ?', (user_name,))
            user = cur.fetchone()
            cur.close()

            if(user is not None):
                return True
            return False

        except sqlite3.Error, e:
            print "Error with executing statement in user_exists():", e.args[0]

    def can_clock(self, user_name, status, connection):
        """
        Verifies that a user is able to clock in/out at the current moment.

        Parameters:
            var1 = The user name to verify for
            var2 = The status, which is either "in"/"In" or "out"/"Out", to verify for
            var3 = The connection to the database that contains the needed information to check

        Returns:
            True if the user is able to clock in/out and false otherwise
        """

        cur = connection.cursor()

        try:
            cur.execute('SELECT max(id) AS id, time_in, time_out\
                         FROM time\
                         WHERE user_name = ?', (user_name,))

            result = cur.fetchone()
            cur.close()

            # Base case:  The user has never once clocked in before
            if(result[0] is None and (status == 'In' or status == 'in')):
                return True

            # If clocking In make sure the users last record has something recorded in the "clock_out" column.
            # If clocking Out make sure the users last record has something recorder in "clock_in" but not "clock_out"
            if((status == 'In' or status == 'in') and result[2] is not None):
                return True
            elif((status == 'Out' or status == 'out') and result[1] is not None and result[2] is None):
                return True

            print user_name + " is not able to clock " + status  # DEBUG
            return False

        except sqlite3.Error, e:
            print "Error with executing statement in can_clock():", e.args[0]

    def clock_in_out(self, user_name, status, connection):
        """
        Clock a user in/out.
        No verification is done to make sure a user can even clock in/out.  Make sure to verify
        using user_exists() and can_clock() first.

        Parameters:
            var1 = The user that is to be clocked in/out
            var2 = "In" or "in" for clocking a user in and "Out" or "out" for clocking a user out
            var3 = The connection to the database that contains the records of the user's clock in/out data
        """

        cur = connection.cursor()
        dt = datetime.now()

        try:
            if(status == 'In' or status == 'in'):
                cur.execute('INSERT INTO time (time_in, user_name)\
                             VALUES (?, ?)', (dt, user_name))
            elif(status == "Out" or status == 'out'):
                cur.execute('SELECT max(id)\
                             FROM time\
                             WHERE user_name = ?', (user_name,))
                result = cur.fetchone()
                cur.execute('UPDATE time\
                             SET time = ?\
                             WHERE id = ?', (dt, result[0]))

            cur.close()
            connection.commit()
        except sqlite3.Error, e:
            print "Error with executing statement in clock_in_out():", e.args[0]
