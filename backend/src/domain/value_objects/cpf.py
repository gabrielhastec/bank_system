

from dataclasses import dataclass
import re

@dataclass(frozen=True, slots=True)
class CPF:
    value: str

    def __post_init__(self):
        if not self._is_valid(self.value):
            raise ValueError("CPF inválido")
    
    @staticmethod
    def _is_valid(cpf: str) -> bool:
        cpf = re.sub(r"\D", "", cpf)
        if len(cpf) != 11 or len(set(cpf)) == 1:
            return False
        # validação dos dígitos verificadores
        def calc_digit(cpf_part: str) -> int:
            s = sum(int(cpf_part[i]) * (len(cpf_part) + 1 - i) for i in range(len(cpf_part)))
            return (s * 10 % 11) % 10
        return calc_digit(cpf[:9]) == int(cpf[9]) and calc_digit(cpf[:10]) == int(cpf[10])
    
    def __str__(self) -> str:
        c = self.value
        return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}"
    