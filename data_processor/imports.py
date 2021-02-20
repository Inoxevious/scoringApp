import csv
from companies import models

# opfile  =  '/home/greats/Documents/projects/dreatol/webapp/fintechapp/clean_applications.csv'

def get_data(csv_file):
    opfile = csv_file
    header  =  []
    lbfile  =  open(opfile, "rt")
    reader  =  csv.reader(lbfile)
    rownum  =  0
    for row in reader:
        if rownum  ==  0:
            header.append(row)
            rownum += 1
        else:
            the_row  =  models.Loan_History(LOAN_ID =row[0],NAME_CONTRACT_TYPE =row[1],CODE_GENDER =row[2],FLAG_OWN_CAR =row[3],FLAG_OWN_REALTY =row[4],NAME_TYPE_SUITE =row[5],
            NAME_INCOME_TYPE =row[6],NAME_EDUCATION_TYPE =row[7],NAME_FAMILY_STATUS =row[8],NAME_HOUSING_TYPE =row[9],OCCUPATION_TYPE =row[10],WEEKDAY_APPR_PROCESS_START =row[11],ORGANIZATION_TYPE =row[12],FONDKAPREMONT_MODE =row[13],HOUSETYPE_MODE =row[14],WALLSMATERIAL_MODE =row[15],
            EMERGENCYSTATE_MODE =row[16],TARGET =row[17],CNT_CHILDREN =row[18],AMT_INCOME_TOTAL =row[19],AMT_CREDIT =row[20],AMT_ANNUITY =row[21],AMT_GOODS_PRICE =row[22],REGION_POPULATION_RELATIVE =row[23],DAYS_BIRTH =row[24],DAYS_EMPLOYED =row[25],
            DAYS_REGISTRATION =row[26],DAYS_ID_PUBLISH =row[27],OWN_CAR_AGE =row[28],FLAG_MOBIL =row[29],FLAG_EMP_PHONE =row[30],FLAG_WORK_PHONE =row[31],FLAG_CONT_MOBILE =row[32],FLAG_PHONE =row[33],FLAG_EMAIL =row[34],CNT_FAM_MEMBERS =row[35],
            REGION_RATING_CLIENT =row[36],REGION_RATING_CLIENT_W_CITY =row[37],HOUR_APPR_PROCESS_START =row[38],REG_REGION_NOT_LIVE_REGION =row[39],REG_REGION_NOT_WORK_REGION =row[40],LIVE_REGION_NOT_WORK_REGION =row[41],REG_CITY_NOT_LIVE_CITY =row[42],REG_CITY_NOT_WORK_CITY =row[43],LIVE_CITY_NOT_WORK_CITY =row[44],EXT_SOURCE_1 =row[45],
            EXT_SOURCE_2 =row[46],EXT_SOURCE_3 =row[47],APARTMENTS_AVG =row[48],BASEMENTAREA_AVG =row[49],YEARS_BEGINEXPLUATATION_AVG =row[50],YEARS_BUILD_AVG =row[51],COMMONAREA_AVG =row[52],ELEVATORS_AVG =row[53],ENTRANCES_AVG =row[54],FLOORSMAX_AVG =row[55],
            FLOORSMIN_AVG =row[56],LANDAREA_AVG =row[57],LIVINGAPARTMENTS_AVG =row[58],LIVINGAREA_AVG =row[59],NONLIVINGAPARTMENTS_AVG =row[60],NONLIVINGAREA_AVG =row[61],APARTMENTS_MODE =row[62],BASEMENTAREA_MODE =row[63],YEARS_BEGINEXPLUATATION_MODE =row[64],YEARS_BUILD_MODE =row[65],
            COMMONAREA_MODE =row[66],ELEVATORS_MODE =row[67],ENTRANCES_MODE =row[68],FLOORSMAX_MODE =row[69],FLOORSMIN_MODE =row[70],LANDAREA_MODE =row[71],LIVINGAPARTMENTS_MODE =row[72],LIVINGAREA_MODE =row[73],NONLIVINGAPARTMENTS_MODE =row[74],NONLIVINGAREA_MODE =row[75],
            APARTMENTS_MEDI =row[76],BASEMENTAREA_MEDI =row[77],YEARS_BEGINEXPLUATATION_MEDI =row[78],YEARS_BUILD_MEDI =row[79],COMMONAREA_MEDI =row[80],ELEVATORS_MEDI =row[81],ENTRANCES_MEDI =row[82],FLOORSMAX_MEDI =row[83],FLOORSMIN_MEDI =row[84],LANDAREA_MEDI =row[85],
            LIVINGAPARTMENTS_MEDI =row[86],LIVINGAREA_MEDI =row[87],NONLIVINGAPARTMENTS_MEDI =row[88],NONLIVINGAREA_MEDI =row[89],TOTALAREA_MODE =row[90],OBS_30_CNT_SOCIAL_CIRCLE =row[91],DEF_30_CNT_SOCIAL_CIRCLE =row[92],OBS_60_CNT_SOCIAL_CIRCLE =row[93],DEF_60_CNT_SOCIAL_CIRCLE =row[94],DAYS_LAST_PHONE_CHANGE =row[95],
            FLAG_DOCUMENT_2 =row[96],FLAG_DOCUMENT_3 =row[97], FLAG_DOCUMENT_4 =row[98], FLAG_DOCUMENT_5 =row[99], FLAG_DOCUMENT_6 =row[100],FLAG_DOCUMENT_7 =row[101],FLAG_DOCUMENT_8 =row[102],FLAG_DOCUMENT_9 =row[103],FLAG_DOCUMENT_10 =row[104],FLAG_DOCUMENT_11 =row[105],
            FLAG_DOCUMENT_12 =row[106],FLAG_DOCUMENT_13 =row[107],FLAG_DOCUMENT_14 =row[108],FLAG_DOCUMENT_15 =row[109],FLAG_DOCUMENT_16 =row[110],FLAG_DOCUMENT_17 =row[111],FLAG_DOCUMENT_18 =row[112],FLAG_DOCUMENT_19 =row[113],FLAG_DOCUMENT_20 =row[114],FLAG_DOCUMENT_21 =row[115],
            AMT_REQ_CREDIT_BUREAU_HOUR =row[116],AMT_REQ_CREDIT_BUREAU_DAY =row[117],AMT_REQ_CREDIT_BUREAU_WEEK =row[118],AMT_REQ_CREDIT_BUREAU_MON =row[119],AMT_REQ_CREDIT_BUREAU_QRT =row[120],AMT_REQ_CREDIT_BUREAU_YEAR =row[121],OFFICER_ID =row[122]
)
            the_row.save()

def get_data_income_data(csv_file):
    opfile = csv_file
    header  =  []
    lbfile  =  open(opfile, "rt")
    reader  =  csv.reader(lbfile)
    rownum  =  0
    for row in reader:
        if rownum  ==  0:
            header.append(row)
            rownum += 1
        else:
            the_row  =  models.IncomeData(LOAN_ID =row[0],age =row[1],workclass =row[2],fnlwgt =row[3],education =row[4],education_num =row[5],
            marital_status =row[6],occupation =row[7],relationship =row[8],race =row[9],sex =row[10],capital_gain =row[11],capital_loss =row[12],hours_per_week =row[13],native_country =row[14],income =row[15]
            )
            the_row.save()

def get_data_applications_data(csv_file):
    opfile = csv_file
    header  =  []
    lbfile  =  open(opfile, "rt")
    reader  =  csv.reader(lbfile)
    rownum  =  0
    for row in reader:
        if rownum  ==  0:
            header.append(row)
            rownum += 1
        else:
            the_row  =  models.LoanApplication(LOAN_ID =row[0],age =row[1],ed =row[2], employ =row[3],address =row[4],income =row[5],
            debtinc =row[6],creddebt =row[7],othdebt =row[8]
            )
            the_row.save()