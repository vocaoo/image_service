from dataclasses import dataclass, field

from di import bind_by_type
from di.dependent import Dependent
from didiator.interface.utils.di_builder import DiBuilder

from src.infrastructure.database import DBConfig
from src.infrastructure.dependencies import DiScope
from src.infrastructure.log import LoggingConfig


@dataclass
class APIConfig:
    host: str = "127.0.0.1"
    port: int = 5000
    debug: bool = __debug__


@dataclass
class Config:
    db: DBConfig = field(default_factory=DBConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    api: APIConfig = field(default_factory=APIConfig)


def setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: config, scope=DiScope.APP), Config))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=DiScope.APP), DBConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.logging, scope=DiScope.APP), LoggingConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.api, scope=DiScope.APP), APIConfig))
