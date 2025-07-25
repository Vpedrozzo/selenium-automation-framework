

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    """
    EXPLICAÇÃO:
    - Esta função vai ser chamada antes de cada teste
    - Ela prepara um navegador Chrome limpo
    - Depois do teste, fecha tudo automaticamente
    """
    

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized") 
    
    service = Service(ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    
    yield driver
    

    driver.quit()  


@pytest.fixture 
def driver_melhorado():
    """
    MELHORIAS EXPLICADAS:
    1. Adicionamos mais configurações úteis
    2. Evitamos detecção de automação
    3. Configuramos timeouts
    """
    
    chrome_options = Options()
    
   
    chrome_options.add_argument("--start-maximized")
    
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    
    driver.implicitly_wait(10)  # 10 segundos
    
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    yield driver
    driver.quit()



def pytest_addoption(parser):
    """
    EXPLICAÇÃO:
    Permite que você passe opções na linha de comando
    Exemplo: pytest --browser=chrome --headless
    """
    parser.addoption(
        "--browser", 
        action="store", 
        default="chrome",
        help="Qual navegador usar: chrome, firefox"
    )
    parser.addoption(
        "--headless", 
        action="store_true", 
        default=False,
        help="Executar sem interface gráfica (mais rápido)"
    )

@pytest.fixture
def driver_configuravel(request):
    """
    EXPLICAÇÃO:
    Agora o driver pode ser configurado por parâmetros
    """
    
    
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    print(f"Iniciando {browser} (sem interface: {headless})")
    
    if browser == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        
        if headless:
            chrome_options.add_argument("--headless")
            
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    else:
        raise ValueError(f"Navegador {browser} não suportado ainda")
    
    driver.implicitly_wait(10)
    
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    EXPLICAÇÃO:
    Esta função "observa" todos os testes
    Se um teste falhar, tira uma foto da tela
    Muito útil para debugar problemas
    """
    
    outcome = yield
    rep = outcome.get_result()
    
    
    if rep.when == "call" and rep.failed:
        
        driver = item.funcargs.get('driver')
        if driver:
            
            screenshot_name = f"screenshot_{item.name}_FALHA.png"
            
            
            driver.save_screenshot(screenshot_name)
            print(f"📸 Screenshot salvo: {screenshot_name}")


@pytest.fixture
def dados_de_teste():
    """
    EXPLICAÇÃO:
    Em vez de colocar dados "hardcoded" nos testes.
    """
    return {
        "usuario_valido": {
            "email": "teste@email.com",
            "senha": "senha123"
        },
        "usuario_invalido": {
            "email": "erro@email.com", 
            "senha": "senhaerrada"
        },
        "urls": {
            "login": "https://exemplo.com/login",
            "home": "https://exemplo.com/home"
        }
    }

