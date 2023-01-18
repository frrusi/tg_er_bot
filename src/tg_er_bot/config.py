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
    tg_bot: TgBot
    database: DatabaseConfig


def load_config(path: str):
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
