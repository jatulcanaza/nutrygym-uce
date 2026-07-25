from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC


def test_edit_plan(driver):

    wait = WebDriverWait(driver, 60)

    # ==========================
    # LOGIN
    # ==========================

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

    # ==========================
    # ESPERAR BOTÓN EDIT
    # ==========================

    edit_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(text(),'Edit nutrition form')]"
            )
        )
    )

    edit_button.click()

    # ==========================
    # ESPERAR MODAL
    # ==========================

    preferences = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='e.g. vegetarian, no seafood']"
            )
        )
    )

    # ==========================
    # MODIFICAR DATOS
    # ==========================

    preferences.clear()
    preferences.send_keys("High protein, chicken")

    allergies = driver.find_element(
        By.XPATH,
        "//input[@placeholder='e.g. lactose, peanuts']"
    )

    allergies.clear()
    allergies.send_keys("Peanuts")

    meals = Select(
        driver.find_element(
            By.XPATH,
            "(//select)[1]"
        )
    )

    meals.select_by_visible_text("5")

    diet = Select(
        driver.find_element(
            By.XPATH,
            "(//select)[2]"
        )
    )

    diet.select_by_visible_text("High")

    calories = driver.find_element(
        By.XPATH,
        "//input[@placeholder='e.g. 2200']"
    )

    calories.clear()
    calories.send_keys("2600")

    water = driver.find_element(
        By.XPATH,
        "//input[@placeholder='e.g. 2.5']"
    )

    water.clear()
    water.send_keys("3")

    # ==========================
    # REGENERAR PLAN
    # ==========================

    regenerate = driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Regenerate plan')]"
    )

    regenerate.click()

    # ==========================
    # ESPERAR FIN
    # ==========================

    wait.until_not(
        EC.text_to_be_present_in_element(
            (
                By.XPATH,
                "//button[contains(@class,'btn-primary')]"
            ),
            "Generating..."
        )
    )

    # ==========================
    # VERIFICAR PLAN
    # ==========================

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//h2[contains(@class,'') or contains(text(),'Nutrition')] | //div[contains(@class,'panel')]"
            )
        )
    )

    # ==========================
    # SCREENSHOT
    # ==========================

    driver.save_screenshot(
        "tests/screenshots/edit_plan.png"
    )