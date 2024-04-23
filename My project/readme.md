# Web Crawling for Quotes and Search Application through similarity indexing

## Abstract
This project involves the development of a web crawling and search application using Scrapy, Flask, and Scikit-Learn. The application allows users to crawl web documents, index them, and perform free-text queries to retrieve relevant documents(quotes). Optional features include query spelling correction/suggestion and query expansion using NLTK and WordNet.

## Overview
The project comprises three main components: a Scrapy-based web crawler (`quotes.py`) which crawls web pages for quotes, a Scikit-Learn-based indexer (`app.py`), and a Flask-based processor for query handling. The web crawler is responsible for downloading web documents in HTML format, while the indexer constructs an inverted index using TF-IDF representation and cosine similarity for search indexing. The Flask processor handles free-text queries and provides top-K ranked results.

## Design
The system is designed to be modular and scalable. Each component operates independently but seamlessly integrates with others. The web crawler utilizes Scrapy's asynchronous architecture for efficient crawling. The indexer employs Scikit-Learn's TfidfVectorizer for vectorization and cosine similarity calculation. The Flask processor serves as the frontend interface, interacting with users and executing search queries.

## Architecture
- **Web Crawler (quotes.py)**: Initializes with seed URL/Domain, Max Pages, and Max Depth. Optional features include Concurrent crawling and Distributed crawling.
- **Indexer (app.py)**: Constructs an inverted index using TF-IDF representation and cosine similarity. Optional features include Vector embedding representation and Neural/Semantic search kNN similarity.
- **Processor (Flask)**: Handles free-text queries in JSON format, performs query validation/error-checking, and returns top-K ranked results. Optional features include Query spelling-correction/suggestion and query expansion.

## Operation
1. Clone the repository and navigate to the project directory.
2. Set up a Python virtual environment using `python -m venv .venv`.
3. Activate the virtual environment using `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows).
4. Install dependencies using `pip install -r requirements.txt`.
5. Run the Flask app using `python app.py`.
6. Access the application in a web browser at `http://localhost:5000`.

## Conclusion
The project successfully implements a web crawling and search application using Scrapy, Flask, and Scikit-Learn. It provides essential functionalities such as web document crawling, indexing, and free-text query processing. The optional features enhance the search experience by offering query spelling correction/suggestion and query expansion.

## Data Sources
- http://quotes.toscrape.com/ - Quotes to Scrape through scrapy spider

## Test Cases
- Unit tests are provided in `test.py` to ensure the functionality of the Flask app.
- Run tests using `python test.py`.

## Source Code
- Source code for the project is available in the repository.

## Bibliography
- Wang, D., Zhang, Q., & Hong, S. (2021). Research on Crawling Network Information Data with Scrapy Framework. International Journal of Network Security, 23(2), 326-331.
- Grinberg, M. (2018). Flask web development. " O'Reilly Media, Inc.".
- Copperwaite, M., & Leifer, C. (2015). Learning flask framework. Packt Publishing Ltd.
- Aliyev, E. (2021). Similarity-Based Patent Selection using Natural Language Processing.
