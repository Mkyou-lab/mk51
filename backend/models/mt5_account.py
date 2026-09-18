from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from ..database import Base
from ..core.security import encrypt_mt5

class MT5Account(Base):
    __tablename__ = "mt5_accounts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    broker = Column(String, nullable=False)
    server = Column(String, nullable=False)
    login = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)
    account_type = Column(String, default="live")  # live or demo
    is_active = Column(Boolean, default=True)
    balance = Column(Float, default=0.0)
    equity = Column(Float, default=0.0)
    magic_number = Column(Integer, default=12345678)

    def set_password(self, password: str):
        self.encrypted_password = encrypt_mt5(password)

    def get_password(self):
        from ..core.security import decrypt_mt5
        return decrypt_mt5(self.encrypted_password)