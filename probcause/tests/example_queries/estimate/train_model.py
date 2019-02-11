from estimate_setup import db_handle
import bayeslite


def main():
    with bayeslite.bayesdb_open(pathname=db_handle) as bdb:
        iterations = int(input("How many iterations to do: "))
        print "Training model..."
        bdb.execute(
            "ANALYZE g FOR " + str(iterations) + " ITERATIONS")


if __name__ == "__main__":
    main()
