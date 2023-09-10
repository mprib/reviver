
from markdown import markdown
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

CONTENT_CSS = """
<style>

/* General styles for all messages */
.message {
    font-family: Arial, sans-serif;
    padding-top: 10px;
    padding-bottom: 10px;
    padding-left: 20px;
    padding-right: 20px;
    margin-bottom: 5px;
    border-radius: 5px;
}

/* User message styles */
.user {
    background-color: #95defb; 
    color: #000; /* Black */
    margin-right: 5%; /* Shift to left */
}

/* Bot message styles */
.assistant {
    background-color: #a8ffa4; 
    color: #000; /* Black */
    margin-left: 5%; /* Shift to right */
}

/* System message styles */
.system {
    background-color: #dcdcdc; /* Gray*/
    color: #000; /* Black */
    font-style: italic;
}

.bot_name {
    font-family: monospace;
    font-style: bold;
    margin-left: 5%; /* Shift to right */
  
}

h1 {
  font-size: 1.5em; 
  color: #444;
}

h2, h3, h4, h5, h6 {
  color: #444;
}

a {
  color: #0645ad;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

code, pre {
  font-family: 'ui-monospace', 'Cascadia Mono', 'Segoe UI Mono', 'Liberation Mono', Menlo, Monaco, Consolas, monospace;
  border-radius: 3px;
  padding: 0.2em 0.4em;
}

pre {
  padding: 1em;
  overflow: auto;
}

pre code {
  background: none;
  border: none;
  padding: 0

</style>
"""

def style_code_blocks(html)->str:
    soup = BeautifulSoup(html, 'html.parser')

    formatter = HtmlFormatter(style='monokai', full=False, cssstyles='overflow:auto;')

    code_css = formatter.get_style_defs('.highlight')

    for block in soup.find_all('code'):
        language = block.get('class', [None])[0]
        if language is not None:
            language = language[9:]  # remove 'language-' prefix
        code = block.string

        if language is None:
            lexer = guess_lexer(code)
        else:
            lexer = get_lexer_by_name(language)

        highlighted_code = highlight(code, lexer, formatter)
        block.string.replace_with(BeautifulSoup(highlighted_code, 'html.parser'))
    # Add the CSS to the beginning of the HTML string
    return f'{CONTENT_CSS}<style>{code_css}</style>' + str(soup)