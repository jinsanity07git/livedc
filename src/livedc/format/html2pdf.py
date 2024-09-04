from specs.hardware import ensure_libs
import os
import time
from PIL import Image
"""
webdriver_manager-4.0.2
"""
def render_html_to_pdf(html_path, output_path):
    """
    https://wkhtmltopdf.org/downloads.html
    """
    import pdfkit
    # Path to the wkhtmltopdf executable
    wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Change this to your actual path
    
    # Configuration for pdfkit
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    
    # Initialize the Chrome driver
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Set browser window size
        driver.set_window_size(1800, 1080)
        # Open the HTML file
        driver.get(f"file://{html_path}")
        
        # Wait for the page to render completely
        time.sleep(5)  # Adjust time if necessary
        
        # Get the page source
        rendered_html = driver.page_source
        
        # Save the rendered HTML to a temporary file
        with open("temp_rendered.html", "w", encoding="utf-8") as f:
            f.write(rendered_html)
        
        # Convert the temporary HTML file to a PDF
        pdfkit.from_file("temp_rendered.html", output_path, configuration=config)
        
    finally:
        driver.quit()
        os.remove("temp_rendered.html")  # Clean up the temporary file

@ensure_libs(["selenium == 4.22.0",
              "webdriver_manager==4.0.2"])
def render_html_to_png(html_path, output_path,wsize=(1800, 1080)):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    # Initialize the Chrome driver
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Set browser window size
        driver.set_window_size(*wsize)  # Set width to 1800px and height to 1080px
        # Set mobile screen size
        # driver.set_window_size(390, 844)
        # Open the HTML file
        driver.get(f"file://{html_path}")
        
        # Wait for the page to render completely
        time.sleep(5)  # Adjust time if necessary
        
        # Scroll to the bottom of the page to ensure all content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Give time for any lazy-loaded content
        
        # Get the dimensions of the page
        total_width = driver.execute_script("return document.body.scrollWidth")
        total_height = driver.execute_script("return document.body.scrollHeight")
        margin = 1.1
        total_width = total_width*margin
        total_height = total_height*margin
        # Set the window size to match the page dimensions
        print (f"exact size: {total_width}, {total_height}")
        driver.set_window_size(total_width, total_height)
        
        # Capture the screenshot
        screenshot_path = "screenshot.png"
        driver.save_screenshot(screenshot_path)
        
        # Convert screenshot to desired output format if needed
        image = Image.open(screenshot_path)
        image.save(output_path)
        
        # Clean up the screenshot file
        os.remove(screenshot_path)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    html_path   = "./html/day2_doc_7.html" 
    output_path = "./html/day2_c1s1.png"  
    render_html_to_png(html_path, output_path)
