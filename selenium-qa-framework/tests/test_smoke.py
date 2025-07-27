import pytest

def test_smoke():
    """
    Teste básico para verificar se a configuração do ambiente está funcionando
    """
    assert True

@pytest.mark.smoke
def test_smoke_selenium(driver):
    """
    Teste básico para verificar se o Selenium está funcionando
    """
    driver.get("https://www.python.org")
    assert "Python" in driver.title
