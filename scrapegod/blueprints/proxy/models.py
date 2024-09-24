from scrapegod.extensions import db
from lib.util_sqlalchemy import ResourceMixin, BaseEnum
from enum import Enum
from sqlalchemy import Enum


class ProtocolEnum(BaseEnum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    SOCKS4 = "SOCKS4"
    SOCKS5 = "SOCKS5"

    @staticmethod
    def name():
        """It returns the name of enum.

        Returns
        -------
            The name of the stage.

        """
        return "protocol_enum"


class AnonymityEnum(BaseEnum):
    ELITE = "ELITE"
    ANONYMOUS = "ANONYMOUS"
    TRANSPARENT = "TRANSPARENT"

    @staticmethod
    def name():
        """It returns the name of enum.

        Returns
        -------
            The name of the stage.

        """
        return "anonymity_enum"


class FreeProxy(db.Model, ResourceMixin):
    __tablename__ = "free_proxy"
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(100), nullable=False, unique=True)
    port = db.Column(db.String(10), nullable=False)
    protocol = db.Column(
        db.Enum(*ProtocolEnum.member_values(), name=ProtocolEnum.name()),
        nullable=True,
    )
    country = db.Column(db.String(100), nullable=True)
    anonymity = db.Column(
        db.Enum(*AnonymityEnum.member_values(), name=AnonymityEnum.name()),
        nullable=True,
    )
    response_time = db.Column(db.Float, nullable=True)
    last_checked = db.Column(db.DateTime, nullable=True)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Proxy {self.ip_address}:{self.port} ({self.protocol})>"
