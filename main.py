import uvicorn
import os
import shutil

from config import settings

if os.name != 'nt':
    from gunicorn_runner import GunicornApplication

def main():
    """
    Application entry point.
    """
    uvicorn.run(
        "app.core.application:get_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
        factory=True
    )


def set_multiproc_dir() -> None:
    """
    Sets mutiproc_dir env variable.

    This function cleans up the multiprocess directory
    and recreates it. This actions are required by prometheus-client
    to share metrics between processes.

    """
    shutil.rmtree(settings.PROMETHEUS_DIR, ignore_errors=True)
    os.makedirs(settings.PROMETHEUS_DIR, exist_ok=True)
    os.environ["prometheus_multiproc_dir"] = str(
        settings.PROMETHEUS_DIR.expanduser().absolute(),
    )
    os.environ["PROMETHEUS_MULTIPROC_DIR"] = str(
        settings.PROMETHEUS_DIR.expanduser().absolute(),
    )


def main() -> None:
    """Entrypoint of the application."""
    set_multiproc_dir()
    if settings.ENVIRONMENT == "development":
        uvicorn.run(
            "app.core.application:get_app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            workers=settings.WORKERS,
            factory=True,
        )
    else:
        # sử dụng file gunicorn.config vì ko nhận forwarded_allow_ips = "*"
        GunicornApplication(
            "app.core.application:get_app",
            host=settings.HOST,
            port=settings.PORT,
            workers=settings.WORKERS,
            threads=4,
            factory=True,
            loglevel=settings.LOG_LEVEL.lower(),
            accesslog="-",
            access_log_format = '%(h)s %(l)s %(u)s [%(t)s] "%(r)s" %(s)s %(b)s',
            forwarded_allow_ips = "*",
            proxy_allow_from = "*",
            secure_scheme_headers = {'X-Forwarded-Proto': 'https'},
            timeout = 120

        ).run()


if __name__ == "__main__":
    main()
