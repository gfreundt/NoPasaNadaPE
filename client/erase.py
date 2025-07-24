import base64

# # Start WebDriver (example with Chrome)
# driver = webdriver.Chrome()
# driver.get("https://example.com")

# # Locate the element
# element = driver.find_element(
#     "css selector", "#your-element"
# )  # Change selector as needed

# # Take screenshot as binary PNG data
# png_bytes = element.screenshot_as_png

# # Encode PNG to base64
# encoded = base64.b64encode(png_bytes)

# Step 1: Read image and encode to base64
with open("test.pdf", "rb") as f:
    encoded = base64.b64encode(f.read())

# Step 2: Write base64 string to text file
with open("test.txt", "w") as f:
    f.write(encoded.decode("utf-8"))

# Step 3: Read base64 string from text file
with open("test.txt", "r") as f:
    decoded = base64.b64decode(f.read())

# Step 4: Write decoded bytes back to PNG
with open("fin.pdf", "wb") as f:
    f.write(decoded)
