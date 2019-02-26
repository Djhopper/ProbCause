from probcause.src.util import table_from_csv
import bayeslite

db_handle = 'crime.bdb'
table_name = 'CRIMEDATA'
csv_handle = '../datasets/crime_data.csv'

def main():
    with bayeslite.bayesdb_open(pathname=db_handle) as bdb:
        with open(csv_handle, 'r') as f:
            table_from_csv(bdb, table_name, f)

        ignore = ['CaseNumber', 'Date', 'Block', 'IUCR', 'PrimaryType', 'Description',
                  'LocationDescription', 'FBICode', 'UpdatedOn', 'XCoordinate',
                  'YCoordinate', 'Latitude', 'Longitude', 'Location']
        numerical = ['ID', 'Beat', 'District', 'Year']
        nominal = ['Arrest', 'Domestic', 'CommunityArea', 'Ward']
        schema = \
            "(" + \
            "; ".join("ignore "+i for i in ignore) + "; " + \
            "; ".join(i + " numerical " for i in numerical) + "; " + \
            "; ".join(i + " nominal" for i in nominal) + \
            ")"
        print([i for i in bdb.execute('SELECT * FROM CRIMEDATA WHERE ID=10000092;')])

        print "Creating population..."
        bdb.execute(
            "CREATE POPULATION FOR " + table_name + " " + schema)
        print "Creating generator..."
        bdb.execute(
            "CREATE GENERATOR crimegen FOR " + table_name)
        print "Initialising model..."
        bdb.execute(
            "INITIALIZE 1 MODEL FOR crimegen")


if __name__ == "__main__":
    main()
