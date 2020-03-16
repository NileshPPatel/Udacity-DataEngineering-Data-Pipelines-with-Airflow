from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):
    """
    This procedure loads data from staging tables on Redshift into a fact table
      
    INPUT PARAMETERS:
    * redshift_conn_id - AWS Redshift connection ID 
    * table - Target Redshift fact table where the data will be stored  
    * sql_query - SQL query to retrieve data to load into target table
    """
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id="", 
                 table="",
                 sql_query="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.sql_query = sql_query

    def execute(self, context):
        self.log.info("Getting Redshift Credentials")
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info("Created Redshift connection")
                 
        self.log.info("Loading data into fact table in Redshift: {}".format(self.table))  
        formatted_sql = f"""
            INSERT INTO {self.table}
            {self.sql_query}
        """
        redshift.run(formatted_sql)        
        self.log.info("Data loaded into fact table in Redshift: {}".format(self.table))
        
