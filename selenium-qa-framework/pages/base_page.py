
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BasePage:
    """
    EXPLICAÇÃO:
    Esta classe tem tudo que QUALQUER página precisa.
    Outras páginas vão "herdar" essas funcionalidades.
    """
    
    def __init__(self, driver):
        """
        EXPLICAÇÃO:
        Quando criar uma página, precisa passar o driver
        É como dar as "chaves da casa" para a página
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)  # Espera até 15 segundos
        self.short_wait = WebDriverWait(driver, 5)  # Espera curta
    
    def navegar_para(self, url):
        """
        EXPLICAÇÃO:
        Método para ir até uma página
        Como pedir para o motorista ir até um endereço
        """
        print(f"🧭 Navegando para: {url}")
        self.driver.get(url)
        self.aguardar_pagina_carregar()
    
    def aguardar_pagina_carregar(self):
        """
        EXPLICAÇÃO:
        Espera a página carregar completamente
        Como esperar o elevador chegar no andar
        """
        try:
            
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("✅ Página carregada completamente")
        except TimeoutException:
            print("⚠️ Página pode não ter carregado completamente")
    
    def encontrar_elemento(self, locator, timeout=15):
        """
        EXPLICAÇÃO:
        Encontra um elemento na página
        Como procurar um interruptor na parede
        
        PARÂMETROS:
        - locator: "endereço" do elemento (By.ID, "nome-do-id")
        - timeout: quanto tempo esperar (padrão 15 segundos)
        """
        try:
            elemento = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            print(f"✅ Elemento encontrado: {locator}")
            return elemento
        except TimeoutException:
            print(f"❌ Elemento não encontrado: {locator}")
            raise
    
    def encontrar_elemento_clicavel(self, locator, timeout=15):
        """
        EXPLICAÇÃO:
        Encontra elemento que pode ser clicado
        Como procurar um botão que funciona
        """
        try:
            elemento = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            print(f"✅ Elemento clicável encontrado: {locator}")
            return elemento
        except TimeoutException:
            print(f"❌ Elemento não está clicável: {locator}")
            raise
    
    def clicar(self, locator):
        """
        EXPLICAÇÃO:
        Clica em um elemento
        Como apertar um botão
        """
        elemento = self.encontrar_elemento_clicavel(locator)
        elemento.click()
        print(f"🖱️ Clicou em: {locator}")
    
    def digitar_texto(self, locator, texto):
        """
        EXPLICAÇÃO:
        Digita texto em um campo
        Como escrever numa folha de papel
        """
        elemento = self.encontrar_elemento(locator)
        elemento.clear()  # Limpa o campo primeiro
        elemento.send_keys(texto)
        print(f"⌨️ Digitou '{texto}' em: {locator}")
    
    def obter_texto(self, locator):
        """
        EXPLICAÇÃO:
        Pega o texto de um elemento
        Como ler o que está escrito numa placa
        """
        elemento = self.encontrar_elemento(locator)
        texto = elemento.text
        print(f"📖 Texto obtido: '{texto}' de {locator}")
        return texto
    
    def elemento_esta_visivel(self, locator, timeout=5):
        """
        EXPLICAÇÃO:
        Verifica se elemento está visível na tela
        Como ver se a luz está acesa
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            print(f"👁️ Elemento visível: {locator}")
            return True
        except TimeoutException:
            print(f"🙈 Elemento não visível: {locator}")
            return False
    
    def aguardar_elemento_desaparecer(self, locator, timeout=10):
        """
        EXPLICAÇÃO:
        Espera um elemento sumir da tela
        Como esperar o loading terminar
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            print(f"🫥 Elemento desapareceu: {locator}")
            return True
        except TimeoutException:
            print(f"⏰ Elemento ainda visível após {timeout}s: {locator}")
            return False
    
    def obter_titulo_pagina(self):
        """
        EXPLICAÇÃO:
        Pega o título da página (que aparece na aba do navegador)
        Como ler o nome na porta da casa
        """
        titulo = self.driver.title
        print(f"📋 Título da página: '{titulo}'")
        return titulo
    
    def obter_url_atual(self):
        """
        EXPLICAÇÃO:
        Pega a URL atual da página
        Como ver o endereço onde você está
        """
        url = self.driver.current_url
        print(f"🌐 URL atual: {url}")
        return url
    
    def tirar_screenshot(self, nome_arquivo=None):
        """
        EXPLICAÇÃO:
        Tira uma foto da tela
        Como tirar uma selfie da página
        """
        if not nome_arquivo:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"screenshot_{timestamp}.png"
        
        caminho = f"reports/screenshots/{nome_arquivo}"
        self.driver.save_screenshot(caminho)
        print(f"📸 Screenshot salvo: {caminho}")
        return caminho
    
    def rolar_pagina_para_elemento(self, locator):
        """
        EXPLICAÇÃO:
        Rola a página até mostrar o elemento
        Como descer a escada até chegar no andar certo
        """
        elemento = self.encontrar_elemento(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", elemento)
        print(f"📜 Rolou página até: {locator}")
    
    def aguardar_segundos(self, segundos):
        """
        EXPLICAÇÃO:
        Espera alguns segundos (use com moderação!)
        Como contar até 10 antes de fazer algo
        """
        print(f"⏳ Aguardando {segundos} segundos...")
        time.sleep(segundos)
    
    def pagina_contem_texto(self, texto):
        """
        EXPLICAÇÃO:
        Verifica se a página contém determinado texto
        Como procurar uma palavra numa página de livro
        """
        try:
            self.wait.until(
                EC.text_to_be_present_in_element((By.TAG_NAME, "body"), texto)
            )
            print(f"✅ Texto encontrado na página: '{texto}'")
            return True
        except TimeoutException:
            print(f"❌ Texto não encontrado na página: '{texto}'")
            return False
