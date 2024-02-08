# AIKitchen-API

An unofficial Python API designed for seamless interaction with Google AI Kitchen's Music and Image generation tools. Unlock the potential of creative content generation through programmatic access to cutting-edge AI capabilities.

## Features

### Music Generation

- Generate audio tracks from text prompts.
- Control the number of tracks and adjust their duration (up to 30 seconds).

### Image Generation

- Generate visually captivating images based on textual prompts.
- Customize the number of images and control aspect ratios.

## Key Features

- **Modular Architecture:** Clearly defined classes for Music and Image functionalities, promoting code organization and readability.
- **Automated Login:** Utilizes Selenium for automated login and token management, streamlining user interactions.
- **Error Handling:** Robust error handling and logging for improved reliability and user feedback.
- **Security Considerations:** Encourages secure storage practices for sensitive information; explore further enhancements for security.
- **Documentation:** Includes inline comments for code clarity; consider adding docstrings for comprehensive documentation.

## Potential Use Cases

- Creative Projects: Experiment with AI-generated music and images for artistic endeavors.
- Application Integration: Integrate AI-generated content into applications, websites, or workflows.
- Automation: Automate content creation tasks using the API's versatile features.

## Important Notes

- This API is unofficial and may not be officially supported by Google AI Kitchen.
- Responsible AI Practices: Adhere to ethical AI principles and practices when using AI-generated content.
- Security Best Practices: Implement robust security measures, considering the sensitivity of information stored.

**Note:** For optimal usage, it is recommended to keep Two-Factor Authentication (2FA) off for the Google AI Kitchen account associated with this API to avoid login issues.

## Further Enhancements

- **API Documentation:** Develop extensive API documentation to guide users effectively.
- **Authentication Improvements:** Implement advanced authentication methods, such as OAuth2, for enhanced security.
- **Error Handling Refinement:** Continuously refine error handling for a seamless user experience.
- **Thorough Testing:** Conduct comprehensive testing to ensure the API's reliability in various scenarios.

## Installation

```bash
pip install AIKitchen-API
```

## Getting Started

```python
from AIKitchen_API.AIKitchen import Login, Music, Image

# Login
login = Login(email="your_email@example.com", password="your_password")
token = login.token

#Music Generation
music = Music()
input = "Ambient, soft sounding music I can study to"
tracks = music.get_tracks(input, 2, token)

if isinstance(tracks, list):
    music.b64toMP3(tracks, input,)

#Image Generation 
image = Image()

input = 'Silver coin with a smiling cat, words "5 catnips" "handmade"'
images = image.get_image(input, 3, token)

if isinstance(images, list):
    image.b64toImg(images, input)
```

For more details, examples, and contribution guidelines, please refer to the [GitHub repository](https://github.com/mir-ashiq/AIKitchen-API).
