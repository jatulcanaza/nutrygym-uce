from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_login(driver):

    wait = WebDriverWait(driver, 20)

    # Abrir aplicación
    driver.get("http://localhost:8080")

    # Ir al login
    login_link = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Login / Sign up")
        )
    )
    login_link.click()

    # Esperar campo email
    email = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Enter your email']")
        )
    )

    # Campo contraseña
    password = driver.find_element(
        By.XPATH,
        "//input[@placeholder='Enter your password']"
    )

    # Ingresar credenciales
    email.send_keys("juan@uce.edu.ec")
    password.send_keys("12345678")

    # Botón Login
    login_button = driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Login')]"
    )

    login_button.click()

    # Esperar redirección
    wait.until(
        EC.url_contains("/nutrigym")
    )

    # Verificar que realmente ingresó
    assert "/nutrigym" in driver.current_url

    # Guardar evidencia
    driver.save_screenshot("tests/screenshots/login_ok.png")