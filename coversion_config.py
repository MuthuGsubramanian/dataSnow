conf_map = {
    'create  macro': '''CREATE OR REPLACE PROCEDURE "{0}"()
                        RETURNS VARCHAR(16777216)
                        LANGUAGE JAVASCRIPT
                        STRICT
                        EXECUTE AS OWNER''',
    'merge into':   'var_sql_merge_base = {0}',

}

sf_exe_b = '''snowflake.execute( {sqlText: var_sql_logical_delete_capture + ";"} ); '''

sf_exe_e = '''
                }
            catch (err)
                {
                return "Failed: " + err;   
                }
                $$;'''