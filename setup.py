import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='steam-review-scraper',
    version='0.1.0',
    author='Zhihan Zhu',
    author_email='garyzhu.zz@gmail.com',
    description='A package to scrape game reviews from Steam.',
    keywords=['steam', 'review', 'scrape', 'crawl'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/woctezuma/download-steam-reviews',
    download_url='https://github.com/woctezuma/download-steam-reviews/archive/0.9.5.tar.gz',
    packages=setuptools.find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
        'pandas'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3',
)