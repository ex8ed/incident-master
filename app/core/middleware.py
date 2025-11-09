# -*- coding: UTF-8 -*-
import time
from fastapi import Request, Response
from .config import setup_logs


logger = setup_logs()


async def log_requests_middleware(request: Request, call_next):
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Request failed: {request.method} {request.url.path} - Error: {str(e)}")
        raise
    
    process_time = time.time() - start_time
    logger.info(f"Response: {request.method} {request.url.path} - Status: {response.status_code} - Duration: {process_time:.3f}s")
    
    return response
