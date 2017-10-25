import sqlalchemy as sa
import pandas as pd


def update_data(pdf, table_name, sa_engine, index_name='index'):
    """
    This function will delete a database table and create a new one
    in its place. Instead of updating, we wipe the data because we
    naiively do not know if the table has updated columns.
    BE CAREFUL! Do not run this accidently with other dataframes.
    """
    # Connect to the database
    conn = sa_engine.connect()
    try:
        # Use metadata to keep track of database information
        metadata = sa.MetaData(bind=conn)
        # Get database information using reflect function
        metadata.reflect()
        if table_name in metadata.tables:
            # Drop table so that we don't make duplicates
            metadata.tables[table_name].drop(sa_engine)
            # Alternatively:
            # conn.execute('DROP TABLE {}'.format(table_name))

        # Make sure index column is named for comparing
        # data moved to and from database.
        # Pandas doesn't require a named index but
        # SQL databases do.
        pdf.index.name = index_name

        # Upload data to database
        pdf.to_sql(table_name, con=conn)
    finally:
        conn.close()


# Make it easier to download data by making a generic function
def df_from_table(table_name, engine, index_col_name=None):
    return pd.read_sql_table(table_name, con=engine, index_col=index_col_name)
    # Faster but unsafe version
    # return pd.read_sql_query('SELECT * FROM {}'.format(table_name),
    #                         con=engine, index_col=index_col_name)

# We will probably want to use a datetime field for plotting so we will do that now
def gen_datetime_col(df, year_col, month_col, day_col):
    # Takes in 3 series: year, month and day, and converts to a new series of type date
    return df[[year_col, month_col, day_col]].apply(lambda x: date(x[0], x[1], x[2]), axis=1)
