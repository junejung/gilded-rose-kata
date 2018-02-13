# -*- coding: utf-8 -*-

MAX_QUALITY = 50
MIN_QUALITY = 0
STANDARD_QUALITY_DELTA = 1
A_DAY_PASSED = 1
SELL_IN_DUE = 0

#Special Concert item magic number
ElEVEN = 11
SIX = 6

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class BaseItem:
    def __init__(self, item):
        self.item  = item

        self._next_day()

    def update(self):
        self._drop_quality()
        self._extra()

        self._min_quality_check()

        return self.item

    def _extra(self):
        if self._expired():
            self._drop_quality()

    def _next_day(self):
        self.item.sell_in = self.item.sell_in - A_DAY_PASSED

    def _drop_quality(self):
        self.item.quality = self.item.quality - STANDARD_QUALITY_DELTA

    def _raise_quality(self):
        self.item.quality = self.item.quality + STANDARD_QUALITY_DELTA

    def _expired(self):
        return self.item.sell_in < SELL_IN_DUE

    def _max_quality_check(self):
        self.item.quality = MAX_QUALITY if self.item.quality > MAX_QUALITY else self.item.quality

    def _min_quality_check(self):
        self.item.quality = MIN_QUALITY if self.item.quality <= MIN_QUALITY else self.item.quality


class ConcertItem(BaseItem):
    def __init__(self, item):
        super(self.__class__, self).__init__(item)

    def update(self):
        self._raise_quality()
        self._close_to_due_day()

        self._max_quality_check()
        if self._expired() : self.item.quality = MIN_QUALITY

        return self.item

    def _close_to_due_day(self):
        if self._sell_in_less_than(ElEVEN):
            self._raise_quality()
            if self._sell_in_less_than(SIX):
                self._raise_quality()

    def _sell_in_less_than(self, day):
        return True if self.item.sell_in < day else False

class AgedItem(BaseItem):
    def __init__(self, item):
        super(self.__class__, self).__init__(item)

    def update(self):
        self._raise_quality()
        self._aged()

        self._max_quality_check()

        return self.item

    def _aged(self):
        if self._expired():
            self._raise_quality()


class ConjuredItem(BaseItem):
    def __init__(self, item):
        super(self.__class__, self).__init__(item)

    def update(self):
        self._drop_quality()
        self._drop_quality()
        self._min_quality_check()

        return self.item


class LegendaryItem(BaseItem):
    def __init__(self, item):
        super(self.__class__, self).__init__(item)

    def update(self):
        return self.item


class GildedRose(object):

    def __init__(self, items):
        self.items = items
        self._item_map = {
            "Aged Brie": AgedItem,
            "Backstage passes to a TAFKAL80ETC concert": ConcertItem,
            "Sulfuras, Hand of Ragnaros": LegendaryItem,
            "Conjured Mana Cake": ConjuredItem
        }

    def update_quality(self):
        for item in self.items:
            try:
                mapped = self._item_map[item.name](item)
            except:
                mapped = BaseItem(item)

            item = mapped.update()