
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_abrir_google_basico(driver):
    """Este deve funcionar perfeitamente"""
    driver.get("https://www.google.com")
    assert "Google" in driver.title
    print("✅ Google carregou corretamente!")


def test_abrir_google_basico(driver):
    """
    PROBLEMA ANTERIOR: Título do Google muda de forma imprevisível
    SOLUÇÃO: Vamos verificar coisas mais confiáveis
    """
    
    driver.get("https://www.google.com")
    
    time.sleep(2)
    
    
    try:
        campo_busca = None
        
        try:
            campo_busca = driver.find_element(By.NAME, "q")
        except:
            pass
            
        if not campo_busca:
            try:
                campo_busca = driver.find_element(By.CSS_SELECTOR, "input[title='Pesquisar']")
            except:
                pass
                
        if not campo_busca:
            campo_busca = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        
        
        campo_busca.send_keys("selenium python")
        campo_busca.send_keys(Keys.RETURN)  
        
       
        time.sleep(3)
        
        titulo_atual = driver.title.lower()
        assert ("selenium" in titulo_atual or "python" in titulo_atual), f"Título atual: {driver.title}"
        
        print(f"✅ Busca realizada! Título: {driver.title}")
        
    except Exception as e:
        print(f"❌ Erro na busca: {str(e)}")
        print(f"Título atual: {driver.title}")
        print(f"URL atual: {driver.current_url}")
        raise

def test_buscar_google_wait_robusto(driver):
    """
    PROBLEMA ANTERIOR: Seletor muito específico
    SOLUÇÃO: Usar seletores mais flexíveis e múltiplas tentativas
    """
    
    driver.get("https://www.google.com")
    
    wait = WebDriverWait(driver, 15)  
    
    try:
        
        campo_busca = None
        
        try:
            campo_busca = wait.until(
                EC.element_to_be_clickable((By.NAME, "q"))
            )
            print("✅ Campo encontrado por NAME")
        except:
            print("⚠️ Campo não encontrado por NAME, tentando CSS...")
            
        if not campo_busca:
            try:
                campo_busca = wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[title*='Pesquis'], input[title*='Search']"))
                )
                print("✅ Campo encontrado por CSS")
            except:
                print("⚠️ Campo não encontrado por CSS, tentando XPath...")
        
        if not campo_busca:
            campo_busca = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='text' and @maxlength]"))
            )
            print("✅ Campo encontrado por XPath")
        
        
        campo_busca.clear()  
        campo_busca.send_keys("pytest selenium")
        campo_busca.send_keys(Keys.RETURN)
        
        wait.until(lambda driver: "google.com/search" in driver.current_url)
        
        print(f"✅ Busca com wait funcionou! URL: {driver.current_url}")
        
    except Exception as e:
        print(f"❌ Erro no teste de wait: {str(e)}")
        print(f"URL atual: {driver.current_url}")
        print(f"Título atual: {driver.title}")
        
        try:
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"Inputs encontrados: {len(inputs)}")
            for i, inp in enumerate(inputs[:3]):  
                print(f"Input {i}: type='{inp.get_attribute('type')}', name='{inp.get_attribute('name')}'")
        except:
            pass
            
        raise

def test_site_confiavel_para_testes(driver):
    """
    EXPLICAÇÃO:
    Google pode mudar, vamos usar um site feito para automação
    """

    driver.get("https://the-internet.herokuapp.com/login")
    
    wait = WebDriverWait(driver, 10)

    username_field = wait.until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_field.send_keys("tomsmith")
    password_field.send_keys("SuperSecretPassword!")
    login_button.click()

    success_message = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    )
    
    assert "You logged into a secure area!" in success_message.text
    print("✅ Login no site de testes funcionou perfeitamente!")

def test_debug_google_elementos(driver):
    """
    EXPLICAÇÃO:
    Este teste só explora o Google para entendermos sua estrutura
    """
    
    driver.get("https://www.google.com")
    time.sleep(3)  
    
    print(f"🔍 Título da página: {driver.title}")
    print(f"🔍 URL atual: {driver.current_url}")
    
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"🔍 Total de inputs encontrados: {len(inputs)}")
    
    for i, inp in enumerate(inputs):
        input_type = inp.get_attribute('type')
        input_name = inp.get_attribute('name')
        input_id = inp.get_attribute('id')
        input_class = inp.get_attribute('class')
        
        print(f"  Input {i}: type='{input_type}', name='{input_name}', id='{input_id}', class='{input_class[:50]}...'")
    
    assert True



