
"""
LoginPage - Page Object para página de login

ANALOGIA:
Se BasePage é o "manual básico de qualquer casa",
LoginPage é o "manual específico da sala de login"

RESPONSABILIDADES:
- Saber onde estão os campos de login
- Saber como fazer login
- Saber como verificar se login funcionou
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    EXPLICAÇÃO:
    Esta classe herda tudo da BasePage e adiciona
    funcionalidades específicas da página de login
    """
    
    """
    EXPLICAÇÃO DOS LOCATORS:
    São como "endereços" dos elementos na página.
    Em vez de decorar, criamos constantes.
    
    VANTAGEM: Se a página mudar, só precisa alterar aqui!
    """
    
    CAMPO_USERNAME = (By.ID, "username")
    CAMPO_PASSWORD = (By.ID, "password") 
    
    BOTAO_LOGIN = (By.CSS_SELECTOR, "button[type='submit']")
    BOTAO_LOGOUT = (By.XPATH, "//a[contains(text(), 'Logout')]")
    
    MENSAGEM_ERRO = (By.CSS_SELECTOR, ".flash.error")
    MENSAGEM_SUCESSO = (By.CSS_SELECTOR, ".flash.success")
    
    TITULO_PAGINA_LOGIN = (By.TAG_NAME, "h2")
    AREA_SEGURA = (By.CSS_SELECTOR, ".secure-area h2")
    
  
    LOGIN_URL = "https://the-internet.herokuapp.com/login"
    SECURE_URL = "https://the-internet.herokuapp.com/secure"
    

    def navegar_para_login(self):
        """
        EXPLICAÇÃO:
        Vai especificamente para a página de login
        Como pedir para ir até a "sala de login"
        """
        print("🏠 Navegando para página de login...")
        self.navegar_para(self.LOGIN_URL)
        self._verificar_se_esta_na_pagina_login()
    
    def fazer_login(self, username, password):
        """
        EXPLICAÇÃO:
        Faz o processo completo de login
        Como "entrar na casa" - usa chave e senha
        
        PARÂMETROS:
        - username: nome do usuário
        - password: senha
        """
        print(f"🔐 Fazendo login com usuário: {username}")
        
        # Passo 1: Digitar username
        self.digitar_texto(self.CAMPO_USERNAME, username)
        
        # Passo 2: Digitar password
        self.digitar_texto(self.CAMPO_PASSWORD, password)
        
        # Passo 3: Clicar no botão
        self.clicar(self.BOTAO_LOGIN)
        
        # Passo 4: Aguardar resposta da página
        self.aguardar_segundos(2)
        
        print("✅ Tentativa de login concluída")
    
    def login_valido(self, username="tomsmith", password="SuperSecretPassword!"):
        """
        EXPLICAÇÃO:
        Login com credenciais que sabemos que funcionam
        Como usar a "chave mestra" da casa
        """
        print("🔑 Fazendo login com credenciais válidas...")
        self.fazer_login(username, password)
    
    def login_invalido(self, username="usuario_errado", password="senha_errada"):
        """
        EXPLICAÇÃO:
        Login com credenciais inválidas para testar erro
        Como tentar abrir com chave errada
        """
        print("❌ Fazendo login com credenciais inválidas...")
        self.fazer_login(username, password)
    
    def fazer_logout(self):
        """
        EXPLICAÇÃO:
        Sai do sistema (faz logout)
        Como "sair da casa e trancar a porta"
        """
        print("🚪 Fazendo logout...")
        self.clicar(self.BOTAO_LOGOUT)
        self.aguardar_segundos(2)
        print("✅ Logout concluído")
    
  
    def esta_na_pagina_login(self):
        """
        EXPLICAÇÃO:
        Verifica se está realmente na página de login
        Como ver se você está na "porta da frente"
        """
        try:
            titulo = self.obter_texto(self.TITULO_PAGINA_LOGIN)
            esta_na_pagina = "Login Page" in titulo
            
            print(f"📍 Está na página de login? {esta_na_pagina}")
            return esta_na_pagina
            
        except Exception as e:
            print(f"❌ Erro ao verificar página de login: {str(e)}")
            return False
    
    def login_foi_bem_sucedido(self):
        """
        EXPLICAÇÃO:
        Verifica se o login deu certo
        Como ver se conseguiu "entrar na casa"
        """
        try:
            if self.elemento_esta_visivel(self.MENSAGEM_SUCESSO, timeout=5):
                mensagem = self.obter_texto(self.MENSAGEM_SUCESSO)
                sucesso = "You logged into a secure area!" in mensagem
                print(f"✅ Login bem-sucedido (por mensagem): {sucesso}")
                return sucesso
            
            if self.elemento_esta_visivel(self.AREA_SEGURA, timeout=5):
                print("✅ Login bem-sucedido (está na área segura)")
                return True
            
            url_atual = self.obter_url_atual()
            if self.SECURE_URL in url_atual:
                print("✅ Login bem-sucedido (URL correta)")
                return True
            
            print("❌ Login não foi bem-sucedido")
            return False
            
        except Exception as e:
            print(f"❌ Erro ao verificar sucesso do login: {str(e)}")
            return False
    
    def login_falhou(self):
        """
        EXPLICAÇÃO:
        Verifica se o login deu erro
        Como ver se a "porta não abriu"
        """
        try:
            if self.elemento_esta_visivel(self.MENSAGEM_ERRO, timeout=5):
                mensagem = self.obter_texto(self.MENSAGEM_ERRO)
                print(f"❌ Login falhou com mensagem: {mensagem}")
                return True
            
            if not self.elemento_esta_visivel(self.AREA_SEGURA, timeout=5):
                print("❌ Login falhou (não está na área segura)")
                return True
            
            url_atual = self.obter_url_atual()
            if self.SECURE_URL not in url_atual:
                print("❌ Login falhou (URL incorreta)")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erro ao verificar falha do login: {str(e)}")
            return False
    
    def obter_mensagem_erro(self):
        """
        EXPLICAÇÃO:
        Pega a mensagem de erro que apareceu
        Como ler o "aviso na porta"
        """
        try:
            if self.elemento_esta_visivel(self.MENSAGEM_ERRO, timeout=5):
                mensagem = self.obter_texto(self.MENSAGEM_ERRO)
                return mensagem
            return None
        except Exception:
            return None
    
    def botao_logout_esta_visivel(self):
        """
        EXPLICAÇÃO:
        Verifica se botão de logout apareceu
        Como ver se a "chave de sair" está disponível
        """
        return self.elemento_esta_visivel(self.BOTAO_LOGOUT, timeout=5)

    
    def _verificar_se_esta_na_pagina_login(self):
        """
        EXPLICAÇÃO:
        Método privado (começa com _) para verificação interna
        Como "conferir se chegou no lugar certo"
        """
        if not self.esta_na_pagina_login():
            print("❌ ATENÇÃO: Pode não estar na página de login!")
        else:
            print("✅ Confirmado: Está na página de login")

