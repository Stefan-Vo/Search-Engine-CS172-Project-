# Project Summary: Search Engine Built with Flask and PyLucene
This project is a lightweight search engine developed using Flask as the web framework and PyLucene for search capabilities. The goal of the project is to create an efficient, scalable, and user-friendly search platform capable of indexing and retrieving textual data.

## Key Features:
Lucene Integration via PyLucene:

PyLucene, a Python wrapper for Apache Lucene, provides robust full-text search and indexing capabilities.
Supports powerful querying with Boolean, Phrase, Fuzzy, and Range queries.
Web Interface with Flask:

Flask provides a minimal and intuitive interface for users to input queries and view results.
The interface supports real-time search and pagination of results.
Indexing System:

Handles text data parsing and stores documents in Lucene's index format for optimized searching.
Includes methods for updating and rebuilding the index as data changes.
Search Functionality:

Returns highly relevant results using Lucene's scoring and ranking algorithms.
Provides advanced search features, such as filters and sorting.
Extensibility:

## Designed to easily integrate additional features like autocomplete, faceted search, or multi-language support.
Use Cases:
Creating searchable document repositories.
Building custom search tools for websites or applications.
Learning about integrating search technology with Python.

#Tech Stack:
Backend: Flask 
Search Engine: PyLucene 
Frontend: HTML, CSS, JavaScript
