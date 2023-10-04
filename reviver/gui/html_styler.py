from pathlib import Path
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from reviver.conversation import Conversation
from reviver import ROOT
import markdown
import reviver.log

log = reviver.log.get(__name__)

with open(Path(ROOT, "reviver", "gui", "conversation.css")) as f:
    CONTENT_CSS = f.read()


def style_conversation(conversation: Conversation) -> str:
    # combine html into larger doc
    convo_html = "<style>" + CONTENT_CSS + "</style>"
    for position, msg in conversation.messages.items():
        convo_html += style_message(msg._id, msg.role, msg.content)

    return convo_html


def style_message(msg_id: str, role: str, content: str) -> str:
    cleaned_content = close_backticks(content)
    cleaned_content = escape_special_characters(cleaned_content)
    html_content = markdown2html(cleaned_content)

    div_html = f"""<div id='{msg_id}' class='message {role}'>
                        {"<p>SYSTEM PROMPT</p>" if role == "system" else ""}
                        {html_content}
                    </div>
                    """

    styled_html = style_code_blocks(div_html)

    return styled_html


def close_backticks(content: str) -> str:
    """
    Used to make sure that the stylized html will render python correctly when it is in the middle
    of being drafted by the bot. Sticks another set of ``` if one is opened without being closed
    """
    # check if the content has an odd number of triple backticks
    if content.count("```") % 2 != 0:
        # if so, append a set of triple backticks to the end

        return content + "\n```"
    else:
        return content


def escape_special_characters(content: str) -> str:
    """
    The presence of some characters in the content string will undermine the correct styling.
    These are fixed here
    """
    content = content.replace("{", "{{")
    content = content.replace("}", "}}")

    return content


def markdown2html(content: str) -> str:
    html_version = markdown.markdown(content, extensions=["fenced_code"])
    return html_version


def style_code_blocks(html) -> str:
    soup = BeautifulSoup(html, "html.parser")

    formatter = HtmlFormatter(style="monokai", full=False, cssstyles="overflow:auto;")

    code_css = formatter.get_style_defs(".highlight")

    for block in soup.find_all("code"):
        if block.parent.name == "pre":  # full code block
            language = block.get("class", [None])[0]
            code = block.string
            if code is not None:
                if language is not None:
                    language = language[9:]  # remove 'language-' prefix
                    lexer = get_lexer_by_name(language)
                else:
                    try:
                        lexer = guess_lexer(code)
                    except Exception as e:
                        log.warn(f"New exception {e}")
                        lexer = get_lexer_by_name(
                            "python"
                        )  # default to python if guess fails

                highlighted_code = highlight(code, lexer, formatter)
                block.string.replace_with(
                    BeautifulSoup(highlighted_code, "html.parser")
                )
        else:
            # inline code
            block["style"] = "font-family: monospace;"

    return f"<style>{code_css}</style>" + str(soup)
