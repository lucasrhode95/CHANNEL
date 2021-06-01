from logging import lastResort
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from utils import *
from time import sleep
import datetime

def logar_horas(
    RDA,
    USER,
    PASSWORD,
    START_DATE,
    END_DATE,
    LOG_WEEKENDS = False,
    DEV_MODE = False,
    HOURS_OF_WORK = 8
):
    # start Channel
    driver = startup('https://channel.certi.org.br/channel/projeto.do?action=projetosUsuario')

    # login
    fill_text_field('username', USER)
    fill_text_field_and_enter('password', PASSWORD)

    # search bar
    fill_text_field_and_enter('ATV_buscaSimples', RDA)
    sleep(1)

    # first <tr>
    table_elem = driver.find_element_by_id('tblAtividadesPendentes')
    tr_elem = table_elem.find_element_by_tag_name('tr')
    actions = ActionChains(driver)
    actions.move_to_element(tr_elem).perform()
    sleep(0.1) # because of the scroll

    # last <td>
    td_elems = retry(lambda: list(tr_elem.find_elements_by_tag_name('td')), max_tries=100)
    last_td_elem = td_elems[-1]

    # last <a>
    a_elems = retry(lambda: last_td_elem.find_elements_by_tag_name('a'), max_tries=100)
    last_a_elem = None
    for last_a in a_elems:
        last_a_elem = last_a

    # open modal
    last_a_elem.click()

    def is_weekend(test_date):
        weekno = test_date.weekday()
        return weekno >= 5

    # WORKLOG
    log_date = START_DATE
    days_to_log = (END_DATE - START_DATE).days
    for i in range(days_to_log):
        date_str = log_date.strftime('%d/%m/%Y')
        if is_weekend(log_date) and not LOG_WEEKENDS:
            print(f'Ignoring weekend @ {date_str}')
            log_date = log_date + datetime.timedelta(days=1)
            continue

        # add work log click
        wait_and_click('incluirApontamentoListar')

        # set date
        retry(lambda: fill_text_field('dataApontamento', date_str), max_tries=100)

        # set hours
        fill_text_field('duracaoApontamento', str(HOURS_OF_WORK))

        # save
        if (DEV_MODE):
            wait_and_click('btn_cancelar_apontamento')
        else:
            wait_and_click('btn_salvar_apontamento')

        log_date = log_date + datetime.timedelta(days=1)

    # driver.close()

def retry(action, max_tries=None, delay=0.1):
    """
    This helps us to retry stuff for when the VPN is slow
    """
    tries = 0
    last_exception = None
    while (max_tries is None) or (tries < max_tries):
        tries += 1
        try:
            return action()
        except Exception as ex:
            sleep(delay)
            last_exception = ex
    else:
        raise last_exception
