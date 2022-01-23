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

CROSSHAIR_SIZE = 5

class CardGenerator:
    def __init__(self, filename):
        self.surface = cairo.PDFSurface(filename,
                                        PAGE_WIDTH * POINTS_PER_MM,
                                        PAGE_HEIGHT * POINTS_PER_MM)

        self.cr = cairo.Context(self.surface)

        # Use mm for the units from now on
        self.cr.scale(POINTS_PER_MM, POINTS_PER_MM)

        # Use ½mm line width
        self.cr.set_line_width(0.5)

        self.word_num = 0

    def _draw_crosshairs(self):
        self.cr.save()

        self.cr.set_source_rgb(0.5, 0.5, 0.5)

        for y in range(0, LINES_PER_PAGE + 1):
            for x in range(0, COLUMNS_PER_PAGE + 1):
                self.cr.move_to(CARD_SIZE * x,
                                CARD_SIZE * y - CROSSHAIR_SIZE / 2.0)
                self.cr.rel_line_to(0, CROSSHAIR_SIZE)
                self.cr.rel_move_to(CROSSHAIR_SIZE / 2.0,
                                    -CROSSHAIR_SIZE / 2.0)
                self.cr.rel_line_to(-CROSSHAIR_SIZE, 0.0)

        self.cr.stroke()

        self.cr.restore()

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

            self._draw_crosshairs()

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

    def skip_to_page_start(self):
        self.word_num = (self.word_num // WORDS_PER_PAGE + 1) * WORDS_PER_PAGE

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

def generate_pdf(filename, word_list, skip_points=None):
    generator = CardGenerator(filename)

    for word in word_list:
        if skip_points is not None and generator.word_num in skip_points:
            generator.skip_to_page_start()

        generator.add_word(word)

generate_pdf("krucindiko-unuflanke.pdf", word_list)

skip_points = set()

# If there are enough words to cover two pages then try to balance the
# number of words on the last pair of pages so that if it is printed
# double-sided then there will be a card on each side of the page in
# the same location.

n_pages = (len(word_list) + WORDS_PER_PAGE - 1) // WORDS_PER_PAGE

if n_pages >= 2:
    words_in_last_two_pages = len(word_list) % WORDS_PER_PAGE + WORDS_PER_PAGE
    last_page_pair = (n_pages & ~1) - 2
    page_split_point = words_in_last_two_pages // 2
    skip_points.add(last_page_pair * WORDS_PER_PAGE + page_split_point)
    skip_points.add((last_page_pair + 1) * WORDS_PER_PAGE +
                    page_split_point)

# If there is an odd number of pages then split the last page too
if (n_pages & 1) == 1:
    skip_points.add((n_pages - 1) * WORDS_PER_PAGE + WORDS_PER_PAGE // 2)

generate_pdf("krucindiko-duflanke.pdf", word_list, skip_points)
