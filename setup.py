from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='AIKitchen-API',
    version='0.1.0',
    author='Ashiq Hussain Mir',
    author_email='imseldrith@gmail.com',
    description="This is an unofficial API designed to interact with Google AI Kitchen's Music and Image generation tools. It provides programmatic access to features like Music Generation and Image Generation.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mir-ashiq/AIKitchen-API',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv',
        'selenium',
        'undetected-chromedriver',
    ],
    entry_points={
        'console_scripts': [
            'aikitchen = AIKitchen_API:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='AI Kitchen API',
    project_urls={
        'Source': 'https://github.com/mir-ashiq/AIKitchen-API',
    },
    license='MIT',
)
