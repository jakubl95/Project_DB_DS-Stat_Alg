import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from tabulate import tabulate
import scipy.stats as st
import numpy as np
from sklearn.linear_model import LinearRegression

try:
    # start database connection and create engine
    con = mysql.connector.connect(user='jlis', password='database_password',
                                  host='127.0.0.1',
                                  database='covid19')
    cursor = con.cursor()

    engine = create_engine("mysql+pymysql://jlis:database_password@127.0.0.1/covid19")

    # statistics for Poland for year 2020
    statistics_base = pd.read_sql('SELECT * FROM cases_monthly '
                                  'WHERE year_index = 2020 '
                                  'AND country_id = (SELECT id FROM country WHERE code = "PL")',
                                  con=con)

    mean_cases = statistics_base['cases'].mean()
    mean_deaths = statistics_base['deaths'].mean()
    median_cases = statistics_base['cases'].median()
    median_deaths = statistics_base['deaths'].median()
    var_cases = statistics_base['cases'].var()
    var_deaths = statistics_base['deaths'].var()
    std_cases = statistics_base['cases'].std()
    std_deaths = statistics_base['deaths'].std()
    cv_cases = std_cases / mean_cases
    cv_deaths = std_deaths / mean_deaths
    kur_cases = st.kurtosis(statistics_base.cases)
    kur_deaths = st.kurtosis(statistics_base.deaths)
    skew_cases = st.skew(statistics_base.cases)
    skew_deaths = st.skew(statistics_base.deaths)

    print('Cases')
    print(tabulate([
        ['mean', mean_cases],
        ['median', median_cases],
        ['variance', var_cases],
        ['st.dev.', std_cases],
        ['cv', cv_cases],
        ['kurtosis', kur_cases],
        ['skew', skew_cases]
    ], headers=['Statistics', 'Value']))
    print('Deaths')
    print(tabulate([
        ['mean', mean_deaths],
        ['median', median_deaths],
        ['variance', var_deaths],
        ['st.dev.', std_deaths],
        ['cv', cv_deaths],
        ['kurtosis', kur_deaths],
        ['skew', skew_deaths]
    ], headers=['Statistics', 'Value']))

    print(" ")
    print("Normal Distribution")
    k_cases, p_cases = st.normaltest(statistics_base.cases)
    k_deaths, p_deaths = st.normaltest(statistics_base.deaths)

    alpha = 5e-2
    print('Cases: p={} < alpha={}'.format(p_cases, alpha))
    if p_cases < alpha:
        print('cases does not come from a normal distribution')
    else:
        print('cases may come from a normal distribution')
    print('Deaths p={} < alpha={}'.format(p_deaths, alpha))
    if p_deaths < alpha:
        print('The null hypothesis can be rejected')
    else:
        print('The null hypothesis cannot be rejected')

    print(" ")
    print("T-Student")
    statistic_cases, pvalue_cases = st.ttest_1samp(statistics_base.cases, mean_cases)
    statistic_deaths, pvalue_deaths = st.ttest_1samp(statistics_base.deaths, mean_deaths)
    print("T_student for cases mean: statistic={}, pvalue={}".format(statistic_cases, pvalue_cases))
    print("T_student for deaths mean: statistic={}, pvalue={}".format(statistic_deaths, pvalue_deaths))

    statistics_base_uk = pd.read_sql('SELECT * FROM cases_monthly '
                                     'WHERE year_index = 2020 '
                                     'AND country_id = (SELECT id FROM country WHERE code = "PL")',
                                     con=con)
    statistic_both, pvalue_both = st.ttest_ind(statistics_base.cases, statistics_base_uk.cases)
    print("T_student for PL and UK mean: statistic={}, pvalue={}".format(statistic_both, pvalue_both))

    correlation = np.corrcoef(statistics_base.cases, statistics_base.deaths)
    corr_coef = correlation[0, 1]
    print(" ")
    print("Correlation coefficient between cases and deaths is equal to: {}".format(corr_coef))
    if corr_coef == 0:
        print("No correlation")
    elif corr_coef < 0.5:
        print("Weak correlation")
    else:
        print("Strong correlation")

    pearson, pvalue_pearson = st.pearsonr(statistics_base.cases, statistics_base.deaths)
    print(" ")
    print("Pearson Correlation for cases and deaths: statistic={}, pvalue={}".format(pearson, pvalue_pearson))

    spearman, pvalue_spearman = st.spearmanr(statistics_base.cases, statistics_base.deaths)
    print(" ")
    print("Spearman Correlation for cases and deaths: statistic={}, pvalue={}".format(spearman, pvalue_spearman))

    model = LinearRegression()
    model.fit(np.array(statistics_base.cases).reshape(-1, 1), statistics_base_uk.cases)
    print(" ")
    print("Linear Regression")
    print("Independent term: {}".format(model.intercept_))
    print("Estimated coefficients: {}".format(model.coef_))
    print("y = {}*x + {}".format(model.coef_[0], model.intercept_))
    print("Score: {}".format(model.score(np.array(statistics_base.cases).reshape(-1, 1), statistics_base_uk.cases)))
    prediction = model.predict(np.array(statistics_base.cases).reshape(-1, 1))
    print("Prediction: {}".format(prediction))
except mysql.connector.Error as err:
    # catch errors
    print(err)
else:
    # end database connection
    cursor.close()
    con.close()
