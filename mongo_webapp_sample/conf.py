import pydantic
import pydantic_settings

_CONF = None


class Config(pydantic_settings.BaseSettings):
    debug: bool = False
    mongo_url: pydantic.MongoDsn = pydantic.Field(
        default="mongodb://localhost:27017/")
    mongo_db_name: str = "sample_app"
    # The timeouts are expressed in seconds.
    mongo_conn_timeout: int = 5
    mongo_op_timeout: int = 10

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix='sampleapp_')


def get_cfg():
    global _CONF
    if not _CONF:
        _CONF = Config()

    return _CONF
