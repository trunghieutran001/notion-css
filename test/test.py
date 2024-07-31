from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Tạo một đối tượng Service cho ChromeDriver
service = Service(ChromeDriverManager().install())

# Tạo đối tượng Options cho Chrome
options = webdriver.ChromeOptions()
# Nếu muốn chạy ở chế độ không đầu, uncomment dòng sau:
# options.add_argument("--headless")

# Khởi tạo WebDriver với Service và Options
driver = webdriver.Chrome(service=service, options=options)

try:
    while True:
        # Truy cập trang web
        driver.get("https://www.notion.so/Nissin-R-D-a166d0a2263c440b80c048416dfa7c96")

        try:
            # Cuộn đến vị trí cụ thể (x, y)
            driver.execute_script("window.scrollTo(0, 900);")

            # Hoặc cuộn đến phần tử <a> mục tiêu
            a_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/A-1-1-e6b80bbe37bb41a88945844e7a8c8fad']"))
            )

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", a_element)

            # Tìm thẻ <div> bên trong thẻ <a>
            div_element = a_element.find_element(By.CSS_SELECTOR, "div[spellcheck='true'][contenteditable='false']")

            # Lấy nội dung của thẻ <div>
            div_text = div_element.text.strip()

            # Thay đổi kích thước font, căn giữa chữ và màu chữ nếu nội dung là "A-1-1"
            if div_text == "A-1-1":
                driver.execute_script("""
                    arguments[0].style.fontSize = '32px';
                    arguments[0].style.padding = '10px 45px 10px';
                """, div_element)

            # Thay đổi màu nền của thẻ <a> dựa trên nội dung của thẻ <span>
            span_element = a_element.find_element(By.TAG_NAME, 'span')
            span_text = span_element.text.strip()

            if span_text == "Trống":
                driver.execute_script("arguments[0].style.backgroundColor = 'white';", a_element)
                driver.execute_script("arguments[0].style.display = 'none';", span_element)
            elif span_text == "Tồn kho":
                driver.execute_script("arguments[0].style.backgroundColor = '#DBEDDB';", a_element)
                driver.execute_script("arguments[0].style.display = 'none';", span_element)
            else:
                driver.execute_script("arguments[0].style.backgroundColor = 'gray';", a_element)

            # Thay đổi vị trí của thẻ <div> thành absolute
            driver.execute_script("arguments[0].style.position = 'absolute';", div_element)

        except Exception as e:
            print(f"Đã xảy ra lỗi khi tìm hoặc thay đổi phần tử: {e}")

        # Đợi để quan sát thay đổi
        time.sleep(2)  # Đợi 5 giây trước khi reload trang

        # Reload trang sau khoảng thời gian định sẵn
        print("Reloading trang...")
        time.sleep(300)  # Thay đổi mỗi 5 phút nếu cần

finally:
    # Đóng trình duyệt
    driver.quit()
