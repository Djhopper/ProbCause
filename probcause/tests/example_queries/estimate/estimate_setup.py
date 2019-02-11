from probcause.util.table_from_csv import table_from_csv
import bayeslite

db_handle = 'estimate_examples.bdb'
csv_handle = 'GenderPayGap.csv'
table_name = 'GenderPayGap'


def main():
    with bayeslite.bayesdb_open(pathname=db_handle) as bdb:
        with open(csv_handle, 'r') as f:
            table_from_csv(bdb, table_name, f)

        ignore = ["EmployerName", "Address", "Postcode", "CompanyLinkToGPGInfo", "ResponsiblePerson", "CurrentName",
                  "PercentDifferenceinMedianHourlyWage", "PercentDifferenceinMeanBonusReceived", "PercentDifferenceinMedianBonusReceived", "PercentageofMalesthatReceivedaBonus", "PercentageofFemalesthatReceivedaBonus"]
        numerical = ["PercentDifferenceinMeanHourlyWage", "ProportionofMalesinLowerQuartile", "ProportionofFemalesinLowerQuartile", "ProportionofMalesinLowerMiddleQuartile", "ProportionofFemalesinLowerMiddleQuartile", "ProportionofMalesinUpperMiddleQuartile", "ProportionofFemalesinUpperMiddleQuartile", "ProportionofMalesinTopQuartile", "ProportionofFemalesinTopQuartile"]
        nominal = ["SubmittedAfterTheDeadline", "EmployerSize"]
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
            "CREATE GENERATOR g FOR " + table_name)
        print "Initialising model..."
        bdb.execute(
            "INITIALIZE 1 MODEL FOR g")

if __name__ == "__main__":
    main()