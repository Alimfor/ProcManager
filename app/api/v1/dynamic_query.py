from fastapi import APIRouter, HTTPException

from app.api.v1.models import DynamicQueryRequest
from app.service.db_service import call_db_function

router = APIRouter()


@router.post("/dynamic_query/")
def dynamic_query(request: DynamicQueryRequest):
    """
    Handles a POST request to the /dynamic_query endpoint.

    Parameters:
    schema (str): The database schema to query.
    func_name (str): The name of the database function to call.
    limit (int): The maximum number of results to return.
    params (list[dict]): A list of dictionaries containing parameter names and values.

    Returns:
    dict: A dictionary containing the query results.
    """
    try:
        result = call_db_function(
            schema=request.db_schema,
            func_name=request.func_name,
            params=[{"column_name": param.column_name, "value": param.value} for param in request.params],
            limit=request.limit
        )
        return {"payload": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
