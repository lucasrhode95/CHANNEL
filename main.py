import datetime
from logar_horas import *

# >CONECTE-SE NA VPN<

logar_horas(
    RDA = '1.2.6.1', # Pode ser o nome OU o código do apontamento
    USER = 'sigla da certi',
    PASSWORD = 'senha (mesma do email)',
    LOG_WEEKENDS = False, # logar nos finais de semana?
    START_DATE = datetime.date(2021, 4, 1), # ano, mês, dia inicial
    END_DATE = datetime.date(2021, 5, 1), # ano, mês, dia final (INTERVALO ABERTO -- não incluso no apontamento)
    DEV_MODE = True, # usar True quando quiser testar, sem cadastrar nada
    HOURS_OF_WORK = 8 # horas trabalhadas por dia
)
