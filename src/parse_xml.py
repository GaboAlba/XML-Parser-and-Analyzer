# Yacc example
import ply.yacc as yacc
from lexical_analyzer import XMLLexer
import pandas as pd
import re
import pprint


# Get the token map from the lexer.  This is required.
class XmlParser(object):
    tag_stack = []
    count = 0
    tokens = XMLLexer.tokens
    event_column_names = ["link", "date", "time", "city", "event_state",
                          "country", "event_shape", "duration", "summary",
                          "posted", "images"]

    def p_all_file(self, p):
        """all_file : state_list shape_list event"""
        p[0] = {
            'state_list': tuple(p[1]),
            'shape_list': tuple(p[2]),
            'events': pd.DataFrame(data=p[3])

        }
        print("Success parsed data")


    def p_state_list(self, p):
        """state_list : open_state_list state close_state_list"""
        p[0] = p[2].copy()

    def p_open_state_list(self, p):
        """open_state_list : STATES_LIST_START"""
        tag_state_list_name = re.sub('[<>]', '', p[1])
        self.tag_stack.append(tag_state_list_name)
        p[0] = tag_state_list_name

    def p_close_state_list(self, p):
        """close_state_list : STATES_LIST_END"""
        tag_state_list_name = re.sub('[</>]', '', p[1])
        n = self.tag_stack.pop()
        if tag_state_list_name != n:
            print('Close tag name ("%s") does not match the corresponding open tag ("%s").' % (p[2], n))
        p[0] = tag_state_list_name

    def p_state(self, p):
        """state : STATE_OPEN STATE_NAME STATE_CLOSE state
                | empty"""
        lexer_list = list(p)
        if len(lexer_list) != 2 and lexer_list[4] is None:
            state_list = [lexer_list[2]]
            p[0] = state_list
        elif len(lexer_list) > 2:
            state_list = lexer_list[2]
            lexer_list[4].append(state_list)
            p[0] = lexer_list[4].copy()


    def p_shape_list(self, p):
        """shape_list : open_shape_list shape close_shape_list"""
        p[0] = p[2].copy()

    def p_open_shape_list(self, p):
        """open_shape_list : SHAPE_LIST_START"""
        tag_shape_list_name = re.sub('[<>]', '', p[1])
        self.tag_stack.append(tag_shape_list_name)
        p[0] = tag_shape_list_name

    def p_close_shape_list(self, p):
        """close_shape_list : SHAPE_LIST_END"""
        tag_shape_list_name = re.sub('[</>]', '', p[1])
        n = self.tag_stack.pop()
        if tag_shape_list_name != n:
            print('Close tag name ("%s") does not match the corresponding open tag ("%s").' % (p[2], n))
        p[0] = tag_shape_list_name

    def p_shape(self, p):
        """shape : SHAPE_OPEN SHAPE_NAME SHAPE_CLOSE shape
                | empty"""
        lexer_list = list(p)
        if len(lexer_list) != 2 and lexer_list[4] is None:
            shape_list = [lexer_list[2]]
            p[0] = shape_list
        elif len(lexer_list) > 2:
            shape_list = lexer_list[2]
            lexer_list[4].append(shape_list)
            p[0] = lexer_list[4].copy()

    def p_event(self, p):
        """event : EVENT_START event_body EVENT_END event 
                | empty"""
        lexer_list = list(p)
        if len(lexer_list) != 2 and lexer_list[4] is None:
            dict_event = dict(zip(self.event_column_names, lexer_list[2]))
            p[0] = [dict_event]

        elif len(lexer_list) > 2:
            dict_event = dict(zip(self.event_column_names, lexer_list[2]))
            lexer_list[4].append(dict_event)
            p[0] = lexer_list[4].copy()

    def p_event_body(self, p):
        """event_body : link date time city event_state country event_shape duration summary posted images"""
        p[0] = [x for x in p[1:]]

    def p_link(self, p):
        """link : LINK_OPEN URL LINK_CLOSE"""
        if self.count == 121:
            print(p[2])
        p[0] = p[2]

    def p_date(self, p):
        """date : DATE_OPEN DATE DATE_CLOSE 
                | DATE_OPEN UNKNOWN_DATE DATE_CLOSE
                | DATE_OPEN DATE_CLOSE"""
        if len(p) < 4:
            p[0] = 'Unknown'
        else:
            p[0] = p[2]

    def p_time(self, p):
        """time : TIME_OPEN TIME TIME_CLOSE 
                | TIME_OPEN UNKNOWN_TIME TIME_CLOSE"""
        p[0] = p[2]

    def p_city(self, p):
        """city : CITY_OPEN CITY CITY_CLOSE
                | CITY_OPEN CITY_CLOSE"""
        if len(p) < 4:
            p[0] = 'Unknown'
        else:
            p[0] = p[2]

    def p_event_state(self, p):
        """event_state : STATE_OPEN STATE_NAME STATE_CLOSE"""
        p[0] = p[2]

    def p_country(self, p):
        """country : COUNTRY_OPEN COUNTRY COUNTRY_CLOSE"""
        p[0] = p[2]

    def p_event_shape(self, p):
        """event_shape : SHAPE_OPEN SHAPE_NAME SHAPE_CLOSE
                        | SHAPE_OPEN SHAPE_CLOSE"""
        if len(p) < 4:
            p[0] = 'Unknown'
        else:
            p[0] = p[2]

    def p_duration(self, p):
        """duration : DURATION_OPEN DURATION DURATION_CLOSE"""
        p[0] = p[2]

    def p_summary(self, p):
        """summary : SUMMARY_OPEN SUMMARY_VALUE SUMMARY_CLOSE"""
        p[0] = p[2]

    def p_posted(self, p):
        """posted : POSTED_OPEN POSTED POSTED_CLOSE"""
        p[0] = p[2]

    def p_images(self, p):
        """images : IMAGES_OPEN IMAGES IMAGES_CLOSE
                  | IMAGES_OPEN IMAGES_CLOSE"""
        if len(p) < 4:
            p[0] = 'No'
        else:
            p[0] = p[2]

    def p_empty(self, p):
        """empty :"""
        pass

    def p_error(self, p):
        print(f"Syntax error in line:{p.lineno}. Bad expression")

    def __init__(self):
        self.lexer = XMLLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    def parse_data(self, data):
        print("Start parsing data...")
        return self.parser.parse(data)


