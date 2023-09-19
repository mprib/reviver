
from markdown import markdown
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from reviver import ROOT
from pathlib import Path
import reviver.log
log = reviver.log.get(__name__)

with open(Path(ROOT, "reviver", "gui", "conversation.css")) as f:
    CONTENT_CSS = f.read()

def style_code_blocks(html)->str:
    soup = BeautifulSoup(html, 'html.parser')

    formatter = HtmlFormatter(style='monokai', full=False, cssstyles='overflow:auto;')

    code_css = formatter.get_style_defs('.highlight')

    for block in soup.find_all('code'):
        
        if block.parent.name == "pre": # full code block
            language = block.get('class', [None])[0]
            code = block.string
            if language is not None:
                language = language[9:]  # remove 'language-' prefix
                lexer = get_lexer_by_name(language)
            else:

                try:
                    lexer = guess_lexer(code)
                except Exception as e:
                    log.warn(f"New exception {e}") 
                    lexer = get_lexer_by_name('python')  # default to python if guess fails 

            highlighted_code = highlight(code, lexer, formatter)
            block.string.replace_with(BeautifulSoup(highlighted_code, 'html.parser'))
        else:
          # inline code 
          block['style'] = 'font-family: monospace;'
          
    # Add the CSS to the beginning of the HTML string
    # return f'{CONTENT_CSS}<style>{code_css}</style>' + str(soup)
    return f'<style>{code_css}</style>' + str(soup)