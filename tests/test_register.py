import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_register(driver):

    wait = WebDriverWait(driver, 20)

    # Abrir aplicación
    driver.get("http://localhost:8080")

    # Ir a Login / Sign up
    wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Login / Sign up")
        )
    ).click()

    # Cambiar a Register
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'Register')]")
        )
    ).click()

    # Esperar el formulario
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Enter your full name']")
        )
    )

    # Datos únicos para evitar conflicto con usuarios existentes
    timestamp = int(time.time())

    name = driver.find_element(
        By.XPATH,
        "//input[@placeholder='Enter your full name']"
    )

    email = driver.find_element(
        By.XPATH,
        "//input[@placeholder='Enter your @uce.edu.ec email']"
    )

    password = driver.find_element(
        By.XPATH,
        "//input[@placeholder='Enter your password']"
    )

    name.send_keys("Usuario Selenium")

    email.send_keys(f"selenium{timestamp}@uce.edu.ec")

    password.send_keys("12345678")

    # Botón Register
    driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Register')]"
    ).click()

    # Esperar mensaje de éxito
    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(),'Account created successfully')]"
            )
        )
    )

    # Evidencia
    driver.save_screenshot(
        "tests/screenshots/register_ok.png"
    )