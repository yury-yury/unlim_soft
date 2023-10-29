import uvicorn

from python_test.settings import settings


uvicorn.run('src.python_test.main:app',
            host=settings.server_host,
            port=settings.server_port,
            reload=True)
