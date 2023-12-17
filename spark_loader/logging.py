import rapidjson as json
import structlog


def logger_factory(level: int):
    structlog.configure(
        processors=[
         
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.processors.KeyValueRenderer(
            key_order=["event", "timestamp"]
        ),
        structlog.processors.JSONRenderer(json.dumps),
        ],
    )
    return structlog.getLogger()
