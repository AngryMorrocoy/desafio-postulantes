from dataclasses import dataclass, field, fields, asdict
import datetime
from enum import Enum
from typing import List, Optional

# Fields
# number
# social_reason
# country
# registration_data (dr, res_number, date)
# expires_at
# last_update_data (dr, res_number, date)
# state (ACTUALIZADO, EXCLUIDO, PENDIENTE)


class PayrollState(Enum):
    UPDATED = "ACTUALIZADO"
    EXCLUDED = "EXCLUIDO"
    PENDING = "PENDIENTE"


@dataclass
class TaxData:
    dr: str = field()
    res_number: str = field()
    date: datetime.date = field()


@dataclass
class VoluntaryRegistrationPayroll:
    number: int = field()
    social_reason: str = field()
    country: str = field()
    expires_at: datetime.date = field()
    state: PayrollState = field()
    registration_data: Optional[TaxData] = field(default=None)
    last_update_data: Optional[TaxData] = field(default=None)

    def as_dict(self):
        def dict_factory(kv_tuple: List[tuple]):
            resulting_dict = {}
            for key, value in kv_tuple:
                if isinstance(value, datetime.date):
                    value = value.isoformat()
                elif isinstance(value, PayrollState):
                    value = value.value
                resulting_dict[key] = value

            return resulting_dict

        return asdict(self, dict_factory=dict_factory)
