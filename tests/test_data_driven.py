
import pytest
from pages.login_page import LoginPage

class TestLoginDataDriven:
    
    @pytest.mark.parametrize("username,password,deveria_funcionar", [
        
        ("tomsmith", "SuperSecretPassword!", True),   # ✅ Credenciais válidas
        ("admin", "SuperSecretPassword!", False),     # ❌ Usuário errado
        ("tomsmith", "senha123", False),              # ❌ Senha errada  
        ("", "SuperSecretPassword!", False),          # ❌ Usuário vazio
        ("tomsmith", "", False),                      # ❌ Senha vazia
        ("", "", False),                              # ❌ Ambos vazios
        ("user@test.com", "SuperSecretPassword!", False), # ❌ Email em vez de nome
    ])
    def test_login_com_diferentes_credenciais(self, driver, username, password, deveria_funcionar):
        """
        EXPLICAÇÃO:
        Este teste vai rodar 7 vezes, uma para cada linha de dados
        É como testar a fechadura com 7 chaves diferentes
        
        PARÂMETROS:
        - @pytest.mark.parametrize: Marca que teste vai rodar múltiplas vezes
        - Cada tupla vira uma execução diferente
        - deveria_funcionar: True se espera sucesso, False se espera erro
        """
        
        print(f"\n🧪 Testando login: '{username}' / '{password}' (espera sucesso: {deveria_funcionar})")
        
        login_page = LoginPage(driver)
        
        login_page.navegar_para_login()
        login_page.fazer_login(username, password)
        
        
        if deveria_funcionar:
            assert login_page.login_foi_bem_sucedido(), f"Login deveria ter funcionado para {username}/{password}"
            print(f"✅ Sucesso esperado e obtido para {username}")
        else:
            assert login_page.login_falhou(), f"Login deveria ter falhado para {username}/{password}"
            print(f"❌ Falha esperada e obtida para {username}")


@pytest.fixture
def cenarios_de_teste():
    """
    EXPLICAÇÃO:
    Fixture que fornece dados mais complexos para os testes
    Como ter uma "caixa de ferramentas" com diferentes cenários
    """
    return {
        "usuario_valido": {
            "dados": {"username": "tomsmith", "password": "SuperSecretPassword!"},
            "expectativa": "sucesso",
            "descricao": "Usuário padrão do sistema"
        },
        "usuario_inexistente": {
            "dados": {"username": "naoexiste", "password": "SuperSecretPassword!"}, 
            "expectativa": "erro",
            "descricao": "Usuário que não existe no sistema"
        },
        "senha_incorreta": {
            "dados": {"username": "tomsmith", "password": "senhaerrada"},
            "expectativa": "erro", 
            "descricao": "Senha incorreta para usuário válido"
        },
        "sql_injection": {
            "dados": {"username": "admin'--", "password": "qualquer"},
            "expectativa": "erro",
            "descricao": "Tentativa de SQL injection"
        },
        "xss_attempt": {
            "dados": {"username": "<script>alert('xss')</script>", "password": "test"},
            "expectativa": "erro",
            "descricao": "Tentativa de XSS attack"
        }
    }

class TestLoginComCenarios:
    
    def test_usuario_valido(self, driver, cenarios_de_teste):
        """Teste específico para usuário válido"""
        cenario = cenarios_de_teste["usuario_valido"]
        self._executar_cenario_login(driver, cenario)
    
    def test_usuario_inexistente(self, driver, cenarios_de_teste):
        """Teste específico para usuário inexistente"""
        cenario = cenarios_de_teste["usuario_inexistente"]
        self._executar_cenario_login(driver, cenario)
    
    def test_senha_incorreta(self, driver, cenarios_de_teste):
        """Teste específico para senha incorreta"""
        cenario = cenarios_de_teste["senha_incorreta"]
        self._executar_cenario_login(driver, cenario)
    
    @pytest.mark.security
    def test_tentativa_sql_injection(self, driver, cenarios_de_teste):
        """Teste de segurança - SQL injection"""
        cenario = cenarios_de_teste["sql_injection"]
        self._executar_cenario_login(driver, cenario)
    
    @pytest.mark.security  
    def test_tentativa_xss(self, driver, cenarios_de_teste):
        """Teste de segurança - XSS"""
        cenario = cenarios_de_teste["xss_attempt"]
        self._executar_cenario_login(driver, cenario)
    
    def _executar_cenario_login(self, driver, cenario):
        """
        EXPLICAÇÃO:
        Método auxiliar que executa qualquer cenário de login
        Como ter um "roteiro padrão" que funciona para qualquer caso
        """
        
        print(f"\n📋 Cenário: {cenario['descricao']}")
        print(f"🎯 Expectativa: {cenario['expectativa']}")
        
        login_page = LoginPage(driver)
        login_page.navegar_para_login()
        
        dados = cenario["dados"]
        login_page.fazer_login(dados["username"], dados["password"])
        
        if cenario["expectativa"] == "sucesso":
            assert login_page.login_foi_bem_sucedido(), f"Cenário '{cenario['descricao']}' deveria ter sucesso"
            print("✅ Cenário passou como esperado")
        else:
            assert login_page.login_falhou(), f"Cenário '{cenario['descricao']}' deveria falhar"
            mensagem_erro = login_page.obter_mensagem_erro()
            if mensagem_erro:
                print(f"❌ Erro obtido: {mensagem_erro}")
            print("✅ Cenário falhou como esperado")


@pytest.fixture
def dados_do_arquivo():
    """
    EXPLICAÇÃO:
    Em projetos reais, dados podem vir de arquivos externos
    Como ter uma "planilha" com todos os casos de teste
    """
    
    return [
        {"nome": "Teste Básico", "user": "tomsmith", "pwd": "SuperSecretPassword!", "deve_passar": True},
        {"nome": "Admin Falso", "user": "admin", "pwd": "admin123", "deve_passar": False},
        {"nome": "Campos Vazios", "user": "", "pwd": "", "deve_passar": False},
        {"nome": "Usuário com Espaços", "user": " tomsmith ", "pwd": "SuperSecretPassword!", "deve_passar": False},
        {"nome": "Senha com Caracteres Especiais", "user": "tomsmith", "pwd": "!@#$%^&*()", "deve_passar": False},
    ]

class TestLoginDadosExternos:
    
    def test_todos_cenarios_do_arquivo(self, driver, dados_do_arquivo):
        """
        EXPLICAÇÃO:
        Testa todos os cenários que vieram do "arquivo externo"
        Como seguir uma lista de instruções passo a passo
        """
        
        login_page = LoginPage(driver)
        
        for cenario in dados_do_arquivo:
            print(f"\n📁 Executando: {cenario['nome']}")
            
            login_page.navegar_para_login()
            
            
            login_page.fazer_login(cenario['user'], cenario['pwd'])
            
            
            if cenario['deve_passar']:
                assert login_page.login_foi_bem_sucedido(), f"Cenário '{cenario['nome']}' deveria passar"
                print(f"✅ {cenario['nome']}: PASSOU")
               
                if login_page.botao_logout_esta_visivel():
                    login_page.fazer_logout()
            else:
                assert login_page.login_falhou(), f"Cenário '{cenario['nome']}' deveria falhar"
                print(f"❌ {cenario['nome']}: FALHOU (como esperado)")


class TestLoginAvancado:
    
    @pytest.mark.parametrize(
        "username,password,tipo_teste",
        [
            ("tomsmith", "SuperSecretPassword!", "credenciais_validas"),
            ("TOMSMITH", "SuperSecretPassword!", "username_maiusculo"),
            ("tomsmith", "SUPERSECRETPASSWORD!", "senha_maiuscula"),
            ("tom smith", "SuperSecretPassword!", "username_com_espaco"),
            ("tomsmith", " SuperSecretPassword! ", "senha_com_espacos"),
            ("tomsmith123", "SuperSecretPassword!", "username_com_numeros"),
            ("admin", "admin", "credenciais_fracas"),
            ("guest", "guest", "usuario_generico"),
        ],
        ids=[
            "Válidas",
            "Username_Maiúsculo", 
            "Senha_Maiúscula",
            "Username_com_Espaço",
            "Senha_com_Espaços",
            "Username_com_Números",
            "Credenciais_Fracas",
            "Usuário_Genérico"
        ]
    )
    def test_variantes_de_login(self, driver, username, password, tipo_teste):
        """
        EXPLICAÇÃO:
        Testa variações comuns que usuários podem tentar
        O parâmetro 'ids' dá nomes descritivos para cada teste
        """
        
        print(f"\n🔍 Testando: {tipo_teste}")
        print(f"👤 Usuário: '{username}' | 🔐 Senha: '{password}'")
        
        login_page = LoginPage(driver)
        login_page.navegar_para_login()
        login_page.fazer_login(username, password)
        
        if tipo_teste == "credenciais_validas":
            assert login_page.login_foi_bem_sucedido()
            print("✅ Login válido funcionou")
        else:
            assert login_page.login_falhou()
            print(f"❌ Variação '{tipo_teste}' falhou como esperado")


@pytest.fixture
def perfis_de_usuario():
    """
    EXPLICAÇÃO:
    Diferentes tipos de usuário que o sistema pode ter
    Como ter "crachás" diferentes para pessoas diferentes
    """
    return {
        "admin": {
            "credenciais": {"username": "admin", "password": "admin123"},
            "pode_acessar": ["dashboard", "usuarios", "configuracoes"],
            "nao_pode_acessar": []
        },
        "usuario_comum": {
            "credenciais": {"username": "tomsmith", "password": "SuperSecretPassword!"},
            "pode_acessar": ["dashboard"],
            "nao_pode_acessar": ["usuarios", "configuracoes"]
        },
        "guest": {
            "credenciais": {"username": "guest", "password": "guest"},
            "pode_acessar": [],
            "nao_pode_acessar": ["dashboard", "usuarios", "configuracoes"]
        }
    }

class TestPerfisDeUsuario:
    
    @pytest.mark.parametrize("perfil_nome", ["usuario_comum"])  
    def test_acesso_por_perfil(self, driver, perfis_de_usuario, perfil_nome):
        """
        EXPLICAÇÃO:
        Testa se cada tipo de usuário consegue acessar o que deve
        Como verificar se cada "crachá" abre as portas certas
        """
        
        perfil = perfis_de_usuario[perfil_nome]
        print(f"\n👤 Testando perfil: {perfil_nome}")
        
        login_page = LoginPage(driver)
        login_page.navegar_para_login()
        
        credenciais = perfil["credenciais"]
        login_page.fazer_login(credenciais["username"], credenciais["password"])
        
       
        if perfil_nome == "usuario_comum":
            assert login_page.login_foi_bem_sucedido()
            print(f"✅ {perfil_nome} conseguiu fazer login")
        else:
            
            if login_page.login_foi_bem_sucedido():
                print(f"✅ {perfil_nome} conseguiu fazer login")
            else:
                print(f"❌ {perfil_nome} não conseguiu fazer login")

