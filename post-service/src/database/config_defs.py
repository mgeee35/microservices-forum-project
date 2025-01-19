from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

import omegaconf
from omegaconf import OmegaConf


class DatabaseTag(Enum):
    MONGODB = "mongodb"
    POSTGRES = "postgres"
    MYSQL = "mysql"


@dataclass
class DatabaseConfig:
    database_tag: DatabaseTag = omegaconf.MISSING


@dataclass
class MongoConfig:
    database_url: str = omegaconf.MISSING
    database_name: str = omegaconf.MISSING
    posts_collection_name: str = omegaconf.MISSING
    stats_collection_name: str = omegaconf.MISSING


@dataclass
class DatabaseMainConfig:
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    mongo: Optional[MongoConfig] = None

    @staticmethod
    def from_file(yaml_path: str) -> "DatabaseMainConfig":
        conf = OmegaConf.structured(DatabaseMainConfig)
        conf = OmegaConf.merge(conf, OmegaConf.load(yaml_path))

        return conf
