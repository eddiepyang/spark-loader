import orjson as json
import structlog


def logger_factory(level: int):
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
            structlog.processors.JSONRenderer(serializer=json.dumps),
        ],
        context_class=dict,
        logger_factory=structlog.BytesLoggerFactory(),
        cache_logger_on_first_use=False,
    )
    return structlog.get_logger()
