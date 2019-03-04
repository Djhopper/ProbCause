from probcause.src.util.table_from_csv import table_from_csv
import bayeslite

db_handle = 'african_traffic_data.bdb'
table_name = 'TRAFFICDATA'
csv_handle = '../datasets/traffic_data.csv'


def main():
    with bayeslite.bayesdb_open(pathname=db_handle) as bdb:
        with open(csv_handle, 'r') as f:
            table_from_csv(bdb, table_name, f)

        ignore = ["date", "time"]
        numerical = ["distance_to_nearest_traffic_light", "speed_limit", "estimated_speed_of_collision"]
        nominal = ["vehicle_type", "second_vehicle_type", "road_has_pavement", "distance_to_nearest_traffic_light",
                   "seat_belt_used", "injury_sustained", "lethal", "land_use", "city"]

        schema = \
            "(" + \
            "; ".join("ignore "+i for i in ignore) + "; " + \
            "; ".join(i + " numerical " for i in numerical) + "; " + \
            "; ".join(i + " nominal" for i in nominal) + \
            ")"

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
