"""
    build_data.py - Build data
    Author: Hoanh An (hoanhan@bennington.edu)
    Date: 04/27/18
"""

from persister import Persister


if __name__ == "__main__":
    MAX_ID = 10

    for i in range(1, MAX_ID):
        persister = Persister(i)
        persister.write()
        print(persister.read())
