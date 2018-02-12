# -*- coding: utf-8 -*-

MAX_QUALITY = 50
MIN_QUALITY = 0
STANDARD_QUALITY_DELTA = 1
A_DAY_PASSED = 1
SELL_IN_DUE = 0

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class BaseItem:
    def __init__(self, item):
        self.name=item.name
        self.sell_in=item.sell_in
        self.quality=item.quality

        self._next_day()

    def update(self):
        self._drop_quality()
        self._extra()

        self._min_quality_check()

    def _extra(self):
        if self._expired():
            self._drop_quality()

    def _next_day(self):
        self.sell_in = self.sell_in - A_DAY_PASSED

    def _drop_quality(self):
        self.quality = self.quality - STANDARD_QUALITY_DELTA

    def _raise_quality(self):
        self.quality = self.quality + STANDARD_QUALITY_DELTA

    def _expired(self):
        return self.sell_in < SELL_IN_DUE

    def _max_quality_check(self):
        self.quality = MAX_QUALITY if self.quality > MAX_QUALITY else self.quality

    def _min_quality_check(self):
        self.quality = MIN_QUALITY if self.quality <= MIN_QUALITY else self.quality


class ConcertItem(BaseItem):
    def __init__(self, item):
        super(self.__class__, self).__init__(item)

    def update(self):
        self._raise_quality()
        self._extra()

        self._max_quality_check()
        if self._expired() : self.quality = MIN_QUALITY

    def _extra(self):
        if self.sell_in < 11:
            self._raise_quality()
            if self.sell_in < 6:
                self._raise_quality()


class AgedItem(BaseItem):
    def __init__(self, item):
        super(self.__class__, self).__init__(item)

    def update(self):
        self._raise_quality()
        self._aged()

        self._max_quality_check()

    def _aged(self):
        if self._expired():
            self.quality = self.quality + STANDARD_QUALITY_DELTA


class LegendaryItem(BaseItem):
    def __init__(self, item):
        super(self.__class__, self).__init__(item)

    def update(self):
        return self


class GildedRose(object):

    def __init__(self, items):
        self.items = items
        self._item_map = {
            "Aged Brie": AgedItem,
            "Backstage passes to a TAFKAL80ETC concert": ConcertItem,
            "Sulfuras, Hand of Ragnaros": LegendaryItem,
            "Elixir of the Mongoose": BaseItem,
            "+5 Dexterity Vest": BaseItem
        }

    def update_quality(self):
        for item in self.items:
            try:
                mapped_item = self._item_map[item.name](item)
                mapped_item.update()
                item.quality = mapped_item.quality
                item.sell_in = mapped_item.sell_in
            except:
                print("Unknown item {}. Please add to the item map".format(item.name))
