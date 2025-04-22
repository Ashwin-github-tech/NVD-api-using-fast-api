from sqlalchemy import Column, Integer, String, Date
from database import Base

class CPE(Base):
    __tablename__ = "cpes"

    id = Column(Integer, primary_key=True, index=True)  
    cpe_title = Column(String, nullable=False)
    cpe_22_uri = Column(String)
    cpe_23_uri = Column(String)
    reference_links = Column(String)  
    cpe_22_deprecation_date = Column(Date, nullable=True)
    cpe_23_deprecation_date = Column(Date, nullable=True)
