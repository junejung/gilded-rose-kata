# -*- coding: utf-8 -*-

MAX_QUALITY = 50
MIN_QUALITY = 0
STANDARD_QUALITY_DROP = 1
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

    def update(self):
        self.quality = self.quality - (STANDARD_QUALITY_DROP + self._extra())
        print(STANDARD_QUALITY_DROP + self._extra())

        return MIN_QUALITY if self.quality < MIN_QUALITY else self.quality

    def _extra(self):
        if self._expired():
            return STANDARD_QUALITY_DROP

        return 0

    def _expired(self):
        return self.sell_in < SELL_IN_DUE


    def _exceed_max_quality(self, quality):
        return True if quality > MAX_QUALITY else False


class ConcertItem(BaseItem):
    def __init__(self, item):
        super(self.__class__, self).__init__(item)

    def update(self):
        self.quality = self.quality + 1 + self._extra()

        if self._expired():
            self.quality = MIN_QUALITY

        if self._exceed_max_quality(self.quality):
            self.quality = MAX_QUALITY

        return self.quality

    def _extra(self):
        if self.sell_in < 6:
            return 2
        elif self.sell_in < 11:
            return 1

        return 0


class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def _is_standard_item(self, item):
        if item.name != "Aged Brie" and item.name != "Backstage passes to a TAFKAL80ETC concert":
                if item.name != "Sulfuras, Hand of Ragnaros":
                    return True
        return False

    def update_quality(self):
        for item in self.items:
            # sell_in update
            if item.name != "Sulfuras, Hand of Ragnaros":
                item.sell_in = item.sell_in - A_DAY_PASSED
            # standard item update
            if item.name == "Backstage passes to a TAFKAL80ETC concert":
                item.quality = ConcertItem(item).update()
            elif self._is_standard_item(item):
                item.quality =BaseItem(item).update()
            else:
                if item.quality < MAX_QUALITY:
                    # all none standard item quality increase
                    item.quality = item.quality + 1

            if item.sell_in < SELL_IN_DUE:
                if item.name == "Aged Brie":
                    # sell in passed - aged item quality increase
                    if item.quality < MAX_QUALITY:
                        item.quality = item.quality + 1