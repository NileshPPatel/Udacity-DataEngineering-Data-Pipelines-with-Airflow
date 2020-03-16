from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):
    """
    This procedure loads data from staging tables on Redshift into dimension tables
      
    INPUT PARAMETERS:
    * redshift_conn_id - AWS Redshift connection ID 
    * table - Target Redshift dimension tables where the data will be stored  
    * sql_query - SQL query to retrieve data to load into target tables
    * insert_mode - "append" or "truncate. Append mode will add data to existing tables.
        Truncate will clear the table of data prior to adding data
    """
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self, 
                 redshift_conn_id="", 
                 table="",
                 sql_query="",
                 insert_mode="truncate",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query
        self.insert_mode = insert_mode

    def execute(self, context):
        self.log.info("Getting Redshift Credentials")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("Created Redshift connection")
        
        if self.insert_mode == "append":
            self.log.info("Insert_mode: append. Appending new data into Redshift table: {}".format(self.table)) 
        elif self.insert_mode == "truncate":
            self.log.info("Insert_mode: truncate. Deleting data from Redshift target table: {}".format(self.table))
            redshift.run("DELETE FROM {}".format(self.table))
        
         
        self.log.info("Loading data into dimension table in Redshift: {}".format(self.table))  
        formatted_sql = f"""
            INSERT INTO {self.table}
            {self.sql_query}
        """
        redshift.run(formatted_sql)        
        self.log.info("Data loaded into dimension table in Redshift: {}".format(self.table))