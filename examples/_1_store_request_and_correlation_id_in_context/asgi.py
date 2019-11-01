import uvicorn

from examples._1_store_request_and_correlation_id_in_context.app import app

uvicorn.run(app)
