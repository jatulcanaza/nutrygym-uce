from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_end_plan(driver):

    wait = WebDriverWait(driver, 60)

    # ======================================
    # LOGIN
    # ======================================

    driver.get("http://localhost:8080")

    wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Login / Sign up")
        )
    ).click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Enter your email']")
        )
    ).send_keys("ariel@uce.edu.ec")

    driver.find_element(
        By.XPATH,
        "//input[@placeholder='Enter your password']"
    ).send_keys("TortugaNinja$53")

    driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Login')]"
    ).click()

    wait.until(
        EC.url_contains("/nutrigym")
    )

    # ======================================
    # VERIFICAR QUE EXISTA UN PLAN
    # ======================================

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//button[contains(text(),'End plan')]"
            )
        )
    )

    # ======================================
    # CLIC EN END PLAN
    # ======================================

    driver.find_element(
        By.XPATH,
        "//button[contains(text(),'End plan')]"
    ).click()

    # ======================================
    # ESPERAR MODAL DE CONFIRMACIÓN
    # ======================================

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//button[contains(text(),'Yes, end plan')]"
            )
        )
    )

    # ======================================
    # CONFIRMAR
    # ======================================

    driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Yes, end plan')]"
    ).click()

    # ======================================
    # ESPERAR A QUE DESAPAREZCA EL MODAL
    # ======================================

    wait.until(
        EC.invisibility_of_element_located(
            (
                By.XPATH,
                "//button[contains(text(),'Yes, end plan')]"
            )
        )
    )

    # ======================================
    # ESPERAR MENSAJE DE ÉXITO
    # ======================================

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[contains(text(),'Plan completed successfully')]"
            )
        )
    )

    # ======================================
    # VERIFICAR QUE YA NO EXISTA PLAN ACTIVO
    # ======================================

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//button[contains(text(),'Get my nutrition plan')]"
            )
        )
    )

    # ======================================
    # SCREENSHOT
    # ======================================

    driver.save_screenshot(
        "tests/screenshots/end_plan.png"
    )