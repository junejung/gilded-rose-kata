# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, ConcertItem, GildedRose

SELL_IN_DUE = 0
MAX_QUANTITY = 50
MIN_QUANTITY = 0

class GildedRoseTest(unittest.TestCase):

    def setUp(self):
        self.aged_item_name = "Aged Brie"
        self.legendary_item_name = "Sulfuras, Hand of Ragnaros"
        self.concert_item_name = "Backstage passes to a TAFKAL80ETC concert"
        self.standard_item_name = "+5 Dexterity Vest"
        self.conjured_item_name = "Conjured Mana Cake"

    # Concert Item tests
    def test_concert_item_update_returns_updated_quality_under_max_quantity(self):
        set_quality = 48
        set_sell_in = 4
        concert_item = ConcertItem(Item(self.concert_item_name, set_sell_in, set_quality))

        concert_item.update()

        self.assertEquals(concert_item.quality, MAX_QUANTITY)

    def test_concert_item_update_returns_updated_quality(self):
        set_quality = 30
        set_sell_in = 4
        expected_increase = 3
        concert_item = ConcertItem(Item(self.concert_item_name, set_sell_in, set_quality))

        concert_item.update()

        self.assertEquals(concert_item.quality, set_quality + expected_increase)

    # gilded rose requirements to tests
    def test_item_when_update_quality_called_sell_in_reduces(self):
        items = [Item("foo", SELL_IN_DUE, 1)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].sell_in, -1)

    def test_item_when_update_quality_called_quality_decrease(self):
        items = [Item("foo", SELL_IN_DUE, 1)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, MIN_QUANTITY)

    def test_item_quality_can_not_be_negative(self):
        items = [Item(self.standard_item_name, SELL_IN_DUE, MIN_QUANTITY)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, MIN_QUANTITY)

    def test_item_when_sell_in_date_passed_quality_degrades_by_two(self):
        set_quantity = 10
        expected_decrease = 2
        items = [Item(self.standard_item_name, SELL_IN_DUE, set_quantity)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, set_quantity - expected_decrease)

    def test_aged_item_when_sell_by_date_passed_increases_quality_by_two(self):
        set_quantity = 10
        expected_incremental = 2
        items = [Item(self.aged_item_name, SELL_IN_DUE, set_quantity)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, set_quantity + expected_incremental)

    def test_aged_item_quality_can_not_exceed_fifty(self):
        items = [Item(self.aged_item_name, SELL_IN_DUE, MAX_QUANTITY)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, MAX_QUANTITY)

    def test_legendary_item_never_decreases_quality(self):
        set_quantity = 80
        items = [Item(self.legendary_item_name, SELL_IN_DUE, set_quantity)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, set_quantity)

    def test_concert_item_when_sell_in_more_than_ten_days_quality_increase_by_one(self):
        set_quantity = 20
        set_sell_in = 15
        expected_incremental = 1
        items = [Item(self.concert_item_name, set_sell_in, set_quantity)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, set_quantity + expected_incremental)

    def test_concert_item_when_sell_in_less_than_ten_days_quality_increase_by_two(self):
        set_quantity = 20
        ten_days_left = 10
        expected_incremental = 2
        items = [Item(self.concert_item_name, ten_days_left, set_quantity)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, set_quantity + expected_incremental)


    def test_concert_item_when_sell_in_left_five_days_quality_increase_by_three(self):
        set_quantity = 20
        five_days_left = 5
        expected_incremental = 3
        items = [Item(self.concert_item_name, five_days_left, set_quantity)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, set_quantity + expected_incremental)

    def test_concert_item_when_date_passes_quality_set_zero(self):
        set_quantity = 20
        items = [Item(self.concert_item_name, SELL_IN_DUE, set_quantity)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, MIN_QUANTITY)

    @unittest.skip("functionality has not implemented yet")
    def test_conjured_item_drops_value_faster(self):
        set_sell_in = 10
        set_quality = 20
        expected_decrease = 2
        items = [Item(self.conjured_item_name, set_sell_in, set_quality)]
        gilded_rose = GildedRose(items)

        gilded_rose.update_quality()

        self.assertEquals(items[0].quality, set_quality - expected_decrease)

if __name__ == '__main__':
    unittest.main()
