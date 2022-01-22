#!/usr/bin/python3

import cairo
import re
import sys
import math

EXTRACT_WORD_RE = re.compile(r'^[^\t]*\t *([^\t\n]+?) *(?:\t|$)')

POINTS_PER_MM = 2.8346457

PAGE_WIDTH = 210
PAGE_HEIGHT = 297

# Card size in mm. They are square
CARD_SIZE = 60

COLUMNS_PER_PAGE = 3
LINES_PER_PAGE = 4
CARDS_PER_PAGE = COLUMNS_PER_PAGE * LINES_PER_PAGE
WORDS_PER_CARD = 2
WORDS_PER_PAGE = CARDS_PER_PAGE * WORDS_PER_CARD

CARDS_START = (PAGE_WIDTH / 2 -
               COLUMNS_PER_PAGE * CARD_SIZE / 2,
               PAGE_HEIGHT / 2 -
               LINES_PER_PAGE * CARD_SIZE / 2)

class CardGenerator:
    def __init__(self):
        self.surface = cairo.PDFSurface("krucindiko.pdf",
                                        PAGE_WIDTH * POINTS_PER_MM,
                                        PAGE_HEIGHT * POINTS_PER_MM)

        self.cr = cairo.Context(self.surface)

        # Use mm for the units from now on
        self.cr.scale(POINTS_PER_MM, POINTS_PER_MM)

        # Use ½mm line width
        self.cr.set_line_width(0.5)

        self.word_num = 0

    def _draw_outlines(self):
        self.cr.set_source_rgb(0, 0, 0)

        self.cr.rectangle(0, 0,
                          CARD_SIZE * COLUMNS_PER_PAGE,
                          CARD_SIZE * LINES_PER_PAGE)

        for i in range(1, COLUMNS_PER_PAGE):
            self.cr.move_to(CARD_SIZE * i, 0)
            self.cr.rel_line_to(0, CARD_SIZE * LINES_PER_PAGE)

        for i in range(1, LINES_PER_PAGE):
            self.cr.move_to(0, CARD_SIZE * i)
            self.cr.rel_line_to(CARD_SIZE * COLUMNS_PER_PAGE, 0)

        self.cr.stroke()

    def add_word(self, word):
        word_in_card = self.word_num % WORDS_PER_CARD
        card_num = self.word_num // WORDS_PER_CARD
        card_in_page = card_num % CARDS_PER_PAGE

        self.cr.save()
        self.cr.translate(CARDS_START[0],
                          card_in_page //
                          COLUMNS_PER_PAGE *
                          CARD_SIZE +
                          CARDS_START[1])

        if word_in_card == 0 and card_in_page == 0:
            if card_num != 0:
                self.cr.show_page()

            self._draw_outlines()

        page_num = card_num // CARDS_PER_PAGE
        column = card_num % COLUMNS_PER_PAGE

        # Flip the column on odd pages so that the cards on the last
        # page will be behind the cards on the second-to-last page
        if (page_num & 1) == 1:
            column = COLUMNS_PER_PAGE - 1 - column

        self.cr.translate(column * CARD_SIZE, 0.0)

        self.cr.save()
        self.cr.set_dash([3, 1])
        self.cr.move_to(CARD_SIZE / 8, CARD_SIZE / 2)
        self.cr.rel_line_to(CARD_SIZE * 6 / 8, 0)
        self.cr.stroke()
        self.cr.restore()

        if word_in_card == 1:
            self.cr.translate(CARD_SIZE / 2.0, CARD_SIZE * 0.75)
            self.cr.rotate(math.pi)
            self.cr.translate(-CARD_SIZE / 2.0, -CARD_SIZE / 4.0)

        self.cr.set_font_size(CARD_SIZE / 9.0)

        font_extents = self.cr.font_extents()
        ascent = font_extents[0]
        descent = font_extents[1]
        extents = self.cr.text_extents(word)

        self.cr.move_to(CARD_SIZE / 2.0 -
                        extents.x_bearing -
                        extents.width / 2,
                        CARD_SIZE / 4.0 -
                        (ascent + descent) / 2.0 +
                        ascent)
        self.cr.show_text(word)

        self.cr.restore()

        self.word_num += 1

line_num = 0
all_words = set()
word_list = []

with open('vortoj.tsv', 'rt') as f:
    for line in f:
        line_num += 1

        if line_num == 1:
            continue

        md = EXTRACT_WORD_RE.match(line)
        if md is None:
            continue

        word = md.group(1)

        if word in all_words:
            print("Ripetita vorto “{}” trovita ĉe linio {}".
                  format(word, line_num),
                  file=sys.stderr)
        else:
            all_words.add(word)
            word_list.append(word)

n_words_second_to_last_page = WORDS_PER_PAGE

# If there are enough words to cover two pages then try to balance the
# number of words on the last two pages so that if it is printed
# double-sided then there will be a card on each side of the page in
# the same location.

if len(word_list) > WORDS_PER_PAGE * 2:
    words_in_last_two_pages = len(word_list) % WORDS_PER_PAGE + WORDS_PER_PAGE
    n_words_second_to_last_page = words_in_last_two_pages // 2

n_pages = (len(word_list) + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE

generator = CardGenerator()

for word_num, word in enumerate(word_list):
    page_num = word_num // WORDS_PER_PAGE

    if page_num == n_pages - 2:
        word_in_page = word_num % WORDS_PER_PAGE

        if word_in_page == n_words_second_to_last_page:
            generator.word_num += WORDS_PER_PAGE - n_words_second_to_last_page

    generator.add_word(word)
