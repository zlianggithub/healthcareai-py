from healthcareai.common.healthcareai_error import HealthcareAIError
import time
import datetime
import pandas as pd


def table_archiver(server, database, source_table, destination_table, timestamp_column_name='ArchivedDTS'):
    """
    Takes a table and archives a complete copy of it with the addition of a timestamp of when the archive occurred to a
    given destination table on the same database.

    This should build a new table if the table doesn't exist.

    :param server: server name
    :param database: database name
    :param source_table: source table name
    :param destination_table: destination table name
    :param timestamp_column_name: new timestamp column name
    :rtype: str: basic stats about how many records were archived
    
    Example usage:

    ```
    from healthcareai.common.table_archiver import table_archiver
    table_archiver('localhost', 'SAM_123', 'RiskScores', 'RiskScoreArchive', 'ArchiveDTS')
    ```
    """
    # Basic input validation
    if type(server) is not str:
        raise HealthcareAIError('Please specify a server address')
    if type(database) is not str:
        raise HealthcareAIError('Please specify a database name')
    if type(source_table) is not str:
        raise HealthcareAIError('Please specify a source table name')
    if type(destination_table) is not str:
        raise HealthcareAIError('Please specify a destination table name')

    start_time = time.time()

    connection_string = 'mssql+pyodbc://{}/{}?driver=SQL+Server+Native+Client+11.0'.format(server, database)

    # Load the table to be archived
    df = pd.read_sql_table(source_table, connection_string)
    number_records_to_add = len(df)

    # Add timestamp to dataframe
    df[timestamp_column_name] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    # Save the new dataframe out to the db without the index, appending values
    df.to_sql(destination_table, connection_string, index=False, if_exists='append')

    end_time = time.time()
    delta_time = end_time - start_time
    result = 'Archived {} records from {}/{}/{} to {} in {} seconds'.format(number_records_to_add, server, database,
                                                                            source_table, destination_table,
                                                                            delta_time)

    return result
