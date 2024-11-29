from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Функция для запуска драйвера
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Уберите эту строку, если хотите видеть браузер
    return webdriver.Chrome(options=options)

# Функция для получения текста статьи
def get_paragraphs(driver):
    paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")
    for i, paragraph in enumerate(paragraphs):
        text = paragraph.text.strip()
        if text:  # Показываем только непустые параграфы
            yield f"Параграф {i + 1}:\n{text}"

# Функция для получения ссылок на связанные страницы
def get_links(driver):
    links = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > ul li a")
    result = {}
    for i, link in enumerate(links, start=1):
        href = link.get_attribute("href")
        if href and "wikipedia.org/wiki/" in href:  # Только внутренние ссылки
            result[i] = (link.text, href)
    return result

# Основная функция
def wikipedia_console():
    driver = setup_driver()
    try:
        print("Добро пожаловать в Википедию!")
        query = input("Введите запрос: ").strip()
        search_url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
        driver.get(search_url)

        if "не существует" in driver.page_source:
            print(f"Статья по запросу '{query}' не найдена.")
            return

        while True:
            print(f"\nВы на странице: {driver.title}")
            print("1. Читать параграфы статьи")
            print("2. Перейти на связанную страницу")
            print("3. Выйти из программы")
            action = input("Выберите действие (1/2/3): ").strip()

            if action == "1":
                content_gen = get_paragraphs(driver)
                for paragraph in content_gen:
                    print(paragraph)
                    more = input("\nНажмите Enter для следующего параграфа или введите 'q' для выхода: ").strip()
                    if more.lower() == 'q':
                        break

            elif action == "2":
                links = get_links(driver)
                if not links:
                    print("Связанных страниц нет.")
                    continue

                print("\nСвязанные страницы:")
                for num, (title, url) in links.items():
                    print(f"{num}. {title}")

                choice = input("Введите номер связанной страницы или 'q' для отмены: ").strip()
                if choice.lower() == 'q':
                    continue
                if choice.isdigit() and int(choice) in links:
                    _, href = links[int(choice)]
                    driver.get(href)
                else:
                    print("Некорректный выбор.")

            elif action == "3":
                print("Выход из программы. До свидания!")
                break

            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

    finally:
        driver.quit()

if __name__ == "__main__":
    wikipedia_console()
