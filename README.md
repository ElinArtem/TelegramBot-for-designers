
### `openai_connection.py` - README.md


# OpenAI Connection

This script provides a function to generate descriptions for interior design photos using OpenAI's API. It allows the user to specify the type of description required (e.g., for a buyer, designer, etc.) and returns a detailed description of the design, specifically tailored for Russian-speaking users.

## Features
- Connects to OpenAI API to create context-specific descriptions for interior design images.
- Ensures accurate content by limiting responses to relevant design imagery.

## Requirements
- `openai` library
- Configuration file (`cfg.py`) with OpenAI API key

## Usage
1. Import the `description_by_image` function.
2. Pass the image URL and description type to get a description.

```python
from openai_connection import description_by_image

description = description_by_image("image_url_here", "for buyer")
print(description)
```

## Configuration
Ensure `cfg.py` file has `CONFIG` dictionary with your OpenAI API key.

```
CONFIG = {
    "OpenAI_API": "your_openai_api_key"
}
```
```

---

### `read_photo.py` - README.md

```markdown
# Image Encoding for Base64

This utility script encodes images into a Base64 format, enabling images to be transmitted or stored in encoded text form. Useful for applications requiring image upload or sharing without direct file attachments.

## Features
- Encodes images to Base64 format.
- Converts images into a text-friendly format for integration into various applications.

## Usage
1. Import the `encode_image` function.
2. Provide the image path to receive the encoded string.

```python
from read_photo import encode_image

encoded_image = encode_image("path_to_image.jpg")
print(encoded_image)
```

## Requirements
No additional libraries are required.
```

---

### `telegram_connection.py` - README.md

```markdown
# Telegram Bot with Image Description Feature

A Telegram bot built using `pyTelegramBotAPI` and integrated with OpenAI to generate descriptions for user-uploaded images. Users can log in, submit images, and request tailored descriptions.

## Features
- User authentication with a password prompt.
- Customizable descriptions generated based on image content and specified description type.
- Handles user interactions such as login, help requests, and description requests.

## Setup
1. Ensure `pyTelegramBotAPI` is installed:
   ```bash
   pip install pyTelegramBotAPI
   ```
2. Update `cfg.py` with `Telegram_API`, `OpenAI_API`, and `Password` keys.
3. Add a `USER_FILE` path for storing user data in JSON format.

## Usage
Run `telegram_connection.py` to start the bot. Users can interact through commands like `/start` to log in, then submit images to receive a description.

### Example
```bash
python telegram_connection.py
```

After starting, the bot will await user input for login, photo upload, and other text-based commands.

## Commands
- **/start**: Begin interaction and login.
- **Help**: Sends a help request to the support team.
- **Generate Description**: Upload an image to receive a description.
```

These files provide clear instructions for each project, covering setup, usage, and main functionality. Let me know if you'd like any adjustments!
