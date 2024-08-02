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

        # Thêm CSS để xóa các hiệu ứng :hover, :active và outline
        driver.execute_script("""
            var style = document.createElement('style');
            style.innerHTML = `
                a:active, a:hover {
                    outline: none !important; /* Xóa hiệu ứng outline */
                    background: none !important; /* Xóa hiệu ứng nền */
                    color: inherit !important; /* Đặt màu chữ thành mặc định */
                }
            `;
            document.head.appendChild(style);
        """)

        # Chờ cho trang tải và tìm tất cả các phần tử với class chính xác
        elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "notion-selectable.notion-page-block.notion-collection-item"))
        )

        # Tạo danh sách các giá trị div_text mong muốn
        target_div_texts = [f"{letter}-{num1}-{num2}" for letter in "ABCDE" for num1 in range(1, 6) for num2 in range(1, 11)]

        for element in elements:
            try:
                # Tìm phần tử div chứa văn bản bên trong thẻ <a>
                a_element = element.find_element(By.TAG_NAME, 'a')
                div_text_element = a_element.find_element(By.CSS_SELECTOR, "div[spellcheck='true'][contenteditable='false']")

                # Tìm phần tử cha của div_text_element và sửa padding
                parent_element = div_text_element.find_element(By.XPATH, "..")
                driver.execute_script("arguments[0].style.padding = '0px';", parent_element)

                # Kiểm tra nội dung của div_text
                div_text = div_text_element.text.strip()
                if div_text in target_div_texts:
                    driver.execute_script("""
                        arguments[0].style.fontSize = '32px';
                        arguments[0].style.padding = '1px 40px 1px';
                        arguments[0].style.margin = 'auto';
                        arguments[0].style.textAlign = 'center';
                        arguments[0].style.display = 'block';
                        arguments[0].style.position = 'relative';
                    """, div_text_element)

                # Thay đổi màu nền của thẻ <a> dựa trên nội dung của thẻ <span>
                span_element = a_element.find_element(By.TAG_NAME, 'span')
                span_text = span_element.text.strip()

                if span_text == "Trống":
                    driver.execute_script("arguments[0].style.backgroundColor = 'white';", a_element)
                    driver.execute_script("arguments[0].style.display = 'none';", span_element)
                elif span_text == "Tồn kho":
                    driver.execute_script("arguments[0].style.backgroundColor = '#DBEDDB';", a_element)
                    driver.execute_script("arguments[0].style.display = 'none';", span_element)
                elif span_text == "Chuẩn bị":
                    driver.execute_script("arguments[0].style.backgroundColor = '#FDECC8';", a_element)
                    driver.execute_script("arguments[0].style.display = 'none';", span_element)
                else:
                    driver.execute_script("arguments[0].style.backgroundColor = 'gray';", a_element)

            except Exception as e:
                print(f"Đã xảy ra lỗi khi tìm hoặc thay đổi phần tử: {e}")

        # Đợi để quan sát thay đổi
        time.sleep(2)  # Đợi 2 giây trước khi reload trang.

        # Reload trang sau khoảng thời gian định sẵn
        print("Reloading trang...")
        time.sleep(300)  # Thay đổi mỗi 5 phút nếu cần

finally:
    # Đóng trình duyệt
    driver.quit()
