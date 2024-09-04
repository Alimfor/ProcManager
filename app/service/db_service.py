import sql

from app.db.database import get_db_connection, close_db_connection


def call_db_function(schema: str, func_name: str, params: list[dict], limit: int = None, return_result: bool = True):
    """
    Calls a database function with the given schema, function name, and parameters.

    Args:
        schema (str): The schema of the database function.
        func_name (str): The name of the database function.
        params (list[dict]): A list of parameter dictionaries, each containing 'column_name' and 'value' keys.
        limit (int, optional): The maximum number of rows to return. Defaults to None.
        return_result (bool, optional): Whether to return the result of the query. Defaults to True.

    Returns:
        list[dict] or dict: If return_result is True, a list of dictionaries representing the query results.
            Otherwise, a dictionary with a 'message' key indicating the query execution status.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        param_names = ', '.join([f"%({param['column_name']})s" for param in params])
        query = sql.SQL(f"SELECT * FROM {schema}.{func_name}({param_names})") if return_result else sql.SQL(
            f"CALL {schema}.{func_name}({param_names})")

        if return_result and limit:
            query += sql.SQL(" LIMIT {limit}").format(limit=sql.Literal(limit))

        param_values = {param['column_name']: param['value'] for param in params}

        cursor.execute(query, param_values)

        if return_result:
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in result]
        else:
            conn.commit()
            return {"message": "Query executed successfully"}

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cursor.close()
        close_db_connection(conn)