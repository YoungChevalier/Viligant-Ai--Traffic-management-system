from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
import sys
import os

# Add libs to python path to handle imports. 
# Depending on your setup, you may need to rename 'common-utils' to 'common_utils'.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../libs/common-utils")))

try:
    import db_naming
    NAMING_CONVENTION = db_naming.NAMING_CONVENTION
except ImportError:
    # Fallback standard convention if the hyphenated import fails
    NAMING_CONVENTION = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)
