import uuid
import threading
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.logger.setup import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        # Attach the request ID to the request state
        request.state.request_id = request_id

        logger.info(
            f"Request: {request.method} {request.url.path} | ID: {request_id}#{threading.get_ident()}"
        )
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code} | ID: {request_id}#{threading.get_ident()}"
        )
        logger.info(f"Process time: {process_time} seconds")
        return response
