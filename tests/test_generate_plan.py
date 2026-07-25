from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def test_generate_plan(driver):

    wait = WebDriverWait(driver, 40)

    # =====================================
    # LOGIN
    # =====================================

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

    wait.until(EC.url_contains("/nutrigym"))

    # Esperar que cargue la página
    wait.until(
        EC.visibility_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    # =====================================
    # ABRIR EL FLUJO
    # =====================================

    wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(text(),'Get my nutrition plan')]"
            )
        )
    ).click()

    # =====================================
    # ¿Apareció PROFILE?
    # =====================================

    profile = driver.find_elements(
        By.XPATH,
        "//h3[contains(text(),'Create user profile')]"
    )

    if profile:

        # First name
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//input[@placeholder='First name']"
                )
            )
        ).send_keys("Ariel")

        # Last name
        driver.find_element(
            By.XPATH,
            "//input[@placeholder='Last name']"
        ).send_keys("Perez")

        # Birth date
        driver.find_element(
            By.XPATH,
            "//input[@type='date']"
        ).send_keys("2000-01-01")

        # Gender
        Select(
            driver.find_element(
                By.XPATH,
                "(//select)[1]"
            )
        ).select_by_visible_text("Male")

        # Height
        driver.find_element(
            By.XPATH,
            "//input[@placeholder='e.g. 170']"
        ).send_keys("175")

        # Weight
        driver.find_element(
            By.XPATH,
            "//input[@placeholder='e.g. 70']"
        ).send_keys("75")

        # Goal
        Select(
            driver.find_element(
                By.XPATH,
                "(//select)[2]"
            )
        ).select_by_visible_text("Gain muscle")

        # Activity
        Select(
            driver.find_element(
                By.XPATH,
                "(//select)[3]"
            )
        ).select_by_visible_text("Moderate")

        # Continue
        driver.find_element(
            By.XPATH,
            "//button[contains(text(),'Continue')]"
        ).click()

    # =====================================
    # ESPERAR NUTRITION FORM
    # =====================================

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='e.g. vegetarian, no seafood']"
            )
        )
    )

    # Preferences

    pref = driver.find_element(
        By.XPATH,
        "//input[@placeholder='e.g. vegetarian, no seafood']"
    )

    pref.clear()
    pref.send_keys("High protein")

    # Allergies

    allergies = driver.find_element(
        By.XPATH,
        "//input[@placeholder='e.g. lactose, peanuts']"
    )

    allergies.clear()
    allergies.send_keys("None")

    # Meals

    Select(
        driver.find_element(
            By.XPATH,
            "(//select)[1]"
        )
    ).select_by_visible_text("4")

    # Diet

    Select(
        driver.find_element(
            By.XPATH,
            "(//select)[2]"
        )
    ).select_by_visible_text("Medium")

    # Calories

    calories = driver.find_element(
        By.XPATH,
        "//input[@placeholder='e.g. 2200']"
    )

    calories.clear()
    calories.send_keys("2200")

    # Water

    water = driver.find_element(
        By.XPATH,
        "//input[@placeholder='e.g. 2.5']"
    )

    water.clear()
    water.send_keys("2.5")

    # =====================================
    # GENERAR PLAN
    # =====================================

    driver.find_element(
        By.XPATH,
        "//button[contains(text(),'Generate plan')]"
    ).click()

    # Esperar que desaparezca el modal

    wait.until(
        EC.invisibility_of_element_located(
            (
                By.XPATH,
                "//h3[contains(text(),'Nutrition form')]"
            )
        )
    )

    # Esperar el panel del plan

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//h2[contains(@class,'') or contains(text(),'Plan')]"
            )
        )
    )

    # Screenshot

    driver.save_screenshot(
        "tests/screenshots/generate_plan.png"
    )

    assert "nutrition" in driver.page_source.lower()