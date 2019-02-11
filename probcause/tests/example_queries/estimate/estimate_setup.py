from probcause.util.table_from_csv import table_from_csv
import bayeslite

db_handle = 'estimate_examples.bdb'
csv_handle = 'GenderPayGap.csv'
table_name = 'GenderPayGap'

with bayeslite.bayesdb_open(pathname=db_handle) as bdb:
    with open(csv_handle, 'r') as f:
        table_from_csv(bdb, table_name, f)

        ignore = ["EmployerName", "Address", "Postcode", "CompanyLinkToGPGInfo", "ResponsiblePerson", "CurrentName"]
        numerical = ["PercentDifferenceinMeanHourlyWage", "PercentDifferenceinMedianHourlyWage", "PercentDifferenceinMeanBonusReceived", "PercentDifferenceinMedianBonusReceived", "PercentageofMalesthatReceivedaBonus", "PercentageofFemalesthatReceivedaBonus", "ProportionofMalesinLowerQuartile", "ProportionofFemalesinLowerQuartile", "ProportionofMalesinLowerMiddleQuartile", "ProportionofFemalesinLowerMiddleQuartile", "ProportionofMalesinUpperMiddleQuartile", "ProportionofFemalesinUpperMiddleQuartile", "ProportionofMalesinTopQuartile", "ProportionofFemalesinTopQuartile"]
        nominal = ["SubmittedAfterTheDeadline", "EmployerSize"]
        schema = \
            "(" + \
            "; ".join("ignore "+i for i in ignore) + "; " + \
            "; ".join(i + " numerical " for i in numerical) + "; " + \
            "; ".join(i + " nominal" for i in nominal) + \
            ")"
        print "Schema:\n" + schema
        bdb.execute(
            "CREATE POPULATION FOR " + table_name + " " + schema)
        bdb.execute(
            "CREATE GENERATOR g FOR " + table_name)
        bdb.execute(
            "INITIALIZE 1 MODEL FOR g")
        bdb.execute(
            "ANALYZE g FOR 30 MINUTES")
