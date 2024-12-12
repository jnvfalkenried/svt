# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

project = 'TikTok Fakenews Detection'
copyright = '2024, Elise, Rustam, Anand, Just'
author = 'Elise, Rustam, Anand, Just'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google/NumPy style docstrings
    'sphinx.ext.viewcode', # Adds links to source code
    # 'sphinx.ext.intersphinx', # Links to external documentation
    # 'sphinx_autodoc_typehints', # Type hint support
    "autoapi.extension",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../../webapp'))

autodoc_mock_imports = [
    "cv2",
    "aio_pika",
    "vertexai",
    "scenedetect",
    "ratelimit",
    "google",
    "loguru",
    "sqlalchemy",
    "dotenv",
    "TikTokApi",
    "pgvector",
    "fastapi",
    "bcrypt",
    "jwt",
    "pydantic",
]

autoapi_type = 'python'
autoapi_dirs = ['../../webapp/backend']
autoapi_options = ['members', 'inherited-members', 'undoc-members', 'show-inheritance', 'show-module-summary']
autoapi_format = 'html'
autoapi_add_toctree = False
