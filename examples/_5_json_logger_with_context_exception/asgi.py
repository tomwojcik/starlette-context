import uvicorn

from examples._5_json_logger_with_context_exception.app import app

uvicorn.run(app, http="h11", loop="asyncio", access_log=True, log_level="debug")
