import configparser
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_json: bool


@dataclass
class Config:
    database: DatabaseConfig
    tg_bot: TgBot = None


def load_bot_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            admin_id=tg_bot.getint("admin_id"),
            use_json=tg_bot.getboolean("use_json"),
        ),
        database=DatabaseConfig(**config["database"])
    )


def load_exchanger_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    return Config(
        database=DatabaseConfig(**config["database"])
    )
