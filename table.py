import numpy
import pandas
import psycopg2

#null count analyser
def missing(column):
    return column.isna().sum()

#completeness percentage analyser
def completness(column):
    return round(100*(column.shape[0]-missing(column))/column.shape[0], 2)

#count of distinct values in column
def distinct(column):
    return len(pandas.unique(column))

#range of numerical values
def num_range(column):
    return str(numpy.nanmin(column))+" to "+str(numpy.nanmax(column))

def each_to_str(list):
    new_list = []
    for l in list:
        new_list.append(str(l.__name__))
    return new_list

def mymean(column):
    return round(numpy.nanmean(column),2)

def returnTable(tableName):
    #my local connection
    conn = psycopg2.connect(
       host = "localhost",
        database = "postgres",
        user = "postgres",
        password = "sq39iaiu")

    #my cursor
    cur = conn.cursor()

    #get my data
    cur.execute("select * from public."+tableName)

    data = cur.fetchall()

    columns = []
    for col in cur.description:
        columns.append(col[0])

    dataframe = pandas.DataFrame(data=data, columns=columns)

    #when using select or making changes remember to commit: conn.commit()
    conn.close()

    coltype = dataframe.dtypes

    object_analyser = [completness, missing, distinct]
    int_analyser = [completness, missing, mymean, numpy.nanmedian, num_range]
    float_analyser = [completness, missing, mymean, numpy.nanmedian, num_range]
    all_analyser  = [completness, missing, distinct, mymean, numpy.nanmedian, num_range]
    #rename analyzers completeness, distinct, valuecount
    all_analyser = ['name'] + each_to_str(all_analyser)

    type_dict = {'object':object_analyser, 'int64':int_analyser, 'float64':float_analyser}

    def function_property_of_column(func, column_name):
        return func(dataframe[column_name])

    results = pandas.DataFrame(columns=all_analyser)

    #print(results)

    for i, column in enumerate(columns):
        row = {str('name'):str(dataframe.columns[i])}
        for func in type_dict[str(coltype[i])]:
            row[str(func.__name__)] = str(function_property_of_column(func, column))
        row_dict = pandas.DataFrame(row, columns=all_analyser, index = [0])
        results = pandas.concat([results, row_dict], ignore_index=True)

    #NEXT STEP: separate the application into parts and have a querry system for requests
    html = results.to_html()
    text_file = open("index.html", "w")
    text_file.write(html)
    text_file.close()
    return html

def returnFreq(tableName, column):
    #my local connection
    conn = psycopg2.connect(
       host = "localhost",
        database = "postgres",
        user = "postgres",
        password = "sq39iaiu")

    #my cursor
    cur = conn.cursor()

    #get my data
    cur.execute("select " +column+", count(*) from public."+tableName+" group by 1 order by 2 desc")

    data = cur.fetchall()

    columns = []
    for col in cur.description:
        columns.append(col[0])

    dataframe = pandas.DataFrame(data=data, columns=columns)

    #when using select or making changes remember to commit: conn.commit()
    conn.close()
    html = dataframe.to_html()
    return html
