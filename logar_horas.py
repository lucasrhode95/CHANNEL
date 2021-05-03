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
    DEV_MODE = False
):
    # start Channel
    driver = startup('https://channel.certi.org.br/channel/projeto.do?action=projetosUsuario')

    # login
    wait_for_element('username')
    wait_for_element('password')
    fill_text_field('username', USER)
    fill_text_field_and_enter('password', PASSWORD)

    # search bar
    wait_for_element('ATV_buscaSimples')
    fill_text_field_and_enter('ATV_buscaSimples', RDA)
    sleep(0.5) # couldn't get rid of this sleep because there is no clear indication that the search has finished

    # first <tr>
    table_elem = driver.find_element_by_id('tblAtividadesPendentes')
    tr_elem = table_elem.find_element_by_tag_name('tr')
    actions = ActionChains(driver)
    actions.move_to_element(tr_elem).perform()
    sleep(0.1) # because of the scroll

    # last <td>
    td_elems = tr_elem.find_elements_by_tag_name('td')
    last_td_elem = None
    for td_elem in td_elems:
        last_td_elem = td_elem

    # last <a>
    a_elems = last_td_elem.find_elements_by_tag_name('a')
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
        wait_for_element('incluirApontamentoListar')
        click('incluirApontamentoListar')

        # set date
        for j in range(10):
            try:
                wait_for_element('dataApontamento')
                date_elem = driver.find_element_by_id('dataApontamento')
                date_elem.clear()
                date_elem.send_keys(date_str)
                break
            except:
                pass

        # set hours
        fill_text_field('duracaoApontamento', '8')
        # save
        if (DEV_MODE):
            sleep(2)
            click('btn_cancelar_apontamento')
        else:
            click('btn_salvar_apontamento')
        log_date = log_date + datetime.timedelta(days=1)

    driver.close()
