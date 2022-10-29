import ply.lex as lex
from ply.lex import TOKEN

class XMLLexer(object):
    # List of token names.   This is always required
    tokens = (
        'STATES_LIST_START',
        'STATES_LIST_END',
        'STATE_OPEN',
        'STATE_CLOSE',
        'STATE_NAME',
        'SHAPE_LIST_START',
        'SHAPE_LIST_END',
        'SHAPE_OPEN',
        'SHAPE_CLOSE',
        'SHAPE_NAME',
        'EVENT_START',
        'EVENT_END',
        'LINK_OPEN',
        'LINK_CLOSE',
        'URL',
        'DATE_OPEN',
        'DATE_CLOSE',
        'DATE',
        'UNKNOWN_DATE',
        'TIME_OPEN',
        'TIME_CLOSE',
        'TIME',
        'UNKNOWN_TIME',
        'CITY_OPEN',
        'CITY_CLOSE',
        'CITY',
        'COUNTRY_OPEN',
        'COUNTRY_CLOSE',
        'COUNTRY',
        'DURATION_OPEN',
        'DURATION_CLOSE',
        'DURATION',
        'SUMMARY_OPEN',
        'SUMMARY_CLOSE',
        'SUMMARY_VALUE',
        'POSTED_OPEN',
        'POSTED_CLOSE',
        'POSTED',
        'IMAGES_OPEN',
        'IMAGES_CLOSE',
        'IMAGES',
    )

    # Regular expression rules for simple tokens
    t_STATES_LIST_START = r'<states_list>'
    t_STATES_LIST_END = r'<\/states_list>'
    t_STATE_OPEN = r'<state>'
    t_STATE_CLOSE = r'<\/state>'
    t_STATE_NAME = r'(?<=<state>)[A-Z ]+(?=<\/state>)'
    t_SHAPE_LIST_START = r'<shape_list>'
    t_SHAPE_LIST_END = r'<\/shape_list>'
    t_SHAPE_OPEN = r'<shape>'
    t_SHAPE_CLOSE = r'<\/shape>'
    t_SHAPE_NAME = r'(?<=<shape>)[A-Za-z]+(?=<\/shape>)'
    t_EVENT_START = r'<event>'
    t_EVENT_END = r'<\/event>'
    t_LINK_OPEN = r'<link>'
    t_LINK_CLOSE = r'<\/link>'
    t_URL = r'(https://)[a-z]+(\.)[a-z]+(\/)[a-z]+(\/)[a-z]+(\/)[0-9]+(\/)[a-zA-z0-9]+(\.html)'
    t_DATE_OPEN = r'<date>'
    t_DATE_CLOSE = r'<\/date>'
    # t_DATE = r'(?<=<date>)[A-Za-z0-9-\?\/\'\s]+(?=<\/date>)'
    t_DATE = r'(?<=<date>).+(?=<\/date>)'
    t_TIME_OPEN = r'<time>'
    t_TIME_CLOSE = r'<\/time>'
    t_TIME = r'(?<=<time>).+(?=<\/time>)'
    t_CITY_OPEN = r'<city>'
    t_CITY_CLOSE = r'<\/city>'
    t_CITY = r'((?<=<city>)\s*.+(?=<\/city>))'
    t_COUNTRY_OPEN = r'<country>'
    t_COUNTRY_CLOSE = r'<\/country>'
    t_COUNTRY = r'(?<=(<country>))[A-Za-z\s]+(?=<\/country>)'
    t_DURATION_OPEN = r'<duration>'
    t_DURATION_CLOSE = r'<\/duration>'
    t_DURATION = r'(?<=<duration>)\s*.*(?=<\/duration>)'
    t_SUMMARY_OPEN = r'<summary>'
    t_SUMMARY_CLOSE = r'<\/summary>'
    t_SUMMARY_VALUE = r'(?<=<summary>)\s*.*(?=<\/summary>)'
    t_POSTED_OPEN = r'<posted>'
    t_POSTED_CLOSE = r'<\/posted>'
    t_POSTED = r'(?<=<posted>)([0-9]{1,2}\/){2}[0-9]{2}(?=<\/posted>)'
    t_IMAGES_OPEN = r'<images>'
    t_IMAGES_CLOSE = r'<\/images>'
    t_IMAGES = r'(?<=(<images>))Yes|No(?=<\/images>)'
    t_ignore = ' \n'
    literals = '$%^'

    def __init__(self):
        self.lexer = None

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


# m = XMLLexer()
# m.build()
# with open("../../../UFO_Report_2022_original.xml", 'r') as f:
#     # Build the lexer
#     m.test(f.read())