import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

try:
    # start database connection and create engine
    con = mysql.connector.connect(user='jlis', password='database_password',
                                  host='127.0.0.1',
                                  database='covid19')
    cursor = con.cursor()

    engine = create_engine("mysql+pymysql://jlis:database_password@127.0.0.1/covid19")

    # load csv data
    # covid_df = pd.read_csv('WHO-COVID-19-global-data.csv',
    # covid_df = pd.read_csv('WHO-COVID-19-poland-data.csv',
    covid_df = pd.read_csv('WHO-COVID-19-uk-data.csv',
                           header=1,
                           names=['date_reported', 'country_code', 'country',
                                  'who_region', 'new_cases', 'cumulative_cases',
                                  'new_deaths', 'cumulative_deaths'])

    # countries sub-dataframe
    countries_df = covid_df[['country', 'country_code', 'who_region']]
    countries_df.columns = ['name', 'code', 'who_region']
    countries_df = countries_df.drop_duplicates()

    # remove rows already existing in database
    countries_existing = engine.execute('SELECT DISTINCT(code) FROM country;')
    unique_country_codes = []
    for i in countries_existing:
        for j in i:
            if j not in unique_country_codes:
                unique_country_codes.append(j)

    countries_df = countries_df[~countries_df.code.isin(unique_country_codes)]
    countries_df.reset_index()

    # insert dataframe to db table
    countries_df.to_sql('country', con=engine, if_exists='append', index=False)

    # get country ids
    cursor.execute('SELECT id, name FROM country;')
    countries_codes = cursor.fetchall()
    countries_codes_dict = {}
    for code in countries_codes:
        countries_codes_dict.update({code[1]: code[0]})

    # cases sub-dataframe
    covid_df['country_id'] = covid_df['country'].map(countries_codes_dict)
    cases_df = covid_df[['country_id', 'date_reported', 'new_cases', 'new_deaths']]
    cases_df.columns = ['country_id', 'report_date', 'cases', 'deaths']
    for index, row in cases_df.iterrows():
        cursor.execute('INSERT INTO reported_cases(country_id, report_date, cases, deaths)'
                       ' VALUES ('
                       + str(row['country_id']) + ', "'
                       + row['report_date'] + '", '
                       + str(row['cases']) + ', '
                       + str(row['deaths'])
                       + ') ON DUPLICATE KEY UPDATE '
                         'cases = ' + str(row['cases']) + ', '
                       + 'deaths = ' + str(row['deaths']) + ';')

    con.commit()

    # update summaries
    cursor.execute(
        'SELECT country_id, report_date FROM reported_cases GROUP BY country_id, year(report_date), month(report_date)')
    records_to_update = cursor.fetchall()
    for record in records_to_update:
        args = [record[1], record[0]]
        cursor.callproc('updatemonthlysummaryforcountry', args)
        cursor.callproc('updatequarterlysummaryforcountry', args)
        cursor.callproc('updateyearlysummaryforcountry', args)
    con.commit()

except mysql.connector.Error as err:
    # catch errors
    print(err)
else:
    # end database connection
    cursor.close()
    con.close()
