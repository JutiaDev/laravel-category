#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:05:48 2020

@author: abdelhamid abouhassane
"""

import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select

browser = webdriver.Chrome('./chromedriver')

options = [
    "search-alias=arts-crafts-intl-ship",  # srefinment ul ( Get just li with class => s-navigation-indent-2 )
    "search-alias=automotive-intl-ship",  # srefinment ul
    "search-alias=baby-products-intl-ship",  # srefinment ul
    "search-alias=beauty-intl-ship",  # srefinment ul
    "search-alias=stripbooks-intl-ship",  # ul within ul
    "search-alias=computers-intl-ship",  # srefinment ul
    # "search-alias=digital-music",
    "search-alias=electronics-intl-ship",  # srefinment ul
    # "search-alias=digital-text",
    # "search-alias=instant-video",
    "search-alias=fashion-womens-intl-ship",  # srefinment ul
    "search-alias=fashion-mens-intl-ship",  # srefinment ul
    "search-alias=fashion-girls-intl-ship",  # srefinment ul
    "search-alias=fashion-boys-intl-ship",  # srefinment ul
    # "search-alias=deals-intl-ship",
    "search-alias=hpc-intl-ship",  # srefinment ul
    "search-alias=kitchen-intl-ship",  # srefinment ul
    "search-alias=industrial-intl-ship",  # srefinment ul
    "search-alias=luggage-intl-ship",
    # "search-alias=movies-tv-intl-ship",
    # "search-alias=music-intl-ship",
    "search-alias=pets-intl-ship",  # srefinment ul
    "search-alias=software-intl-ship",  # srefinment ul
    "search-alias=sporting-intl-ship",  # srefinment ul
    "search-alias=tools-intl-ship",  # srefinment ul
    "search-alias=toys-and-games-intl-ship",  # srefinment ul
    "search-alias=videogames-intl-ship"  # srefinment ul
]


def build_tree(browser_instance, tree_dict, ul, index):
    if ul:
        for el in ul:
            key = el.text
            tree_dict[key] = {}
            elhref = el.find_element_by_tag_name('a')
            if elhref:
                browser_instance.get(elhref.get_attribute('href'))
                time.sleep(2)
                ull = browser_instance.find_element_by_css_selector('#s-refinements ul')
                if ull:
                    liElements = ull.find_elements_by_tag_name('li')
                    if liElements and len(liElements) > index + 1:
                        index += 1
                        build_tree(browser_instance, tree_dict[key], liElements[index:], index)
    return {}


def buildBaseDepth():
    BaseCategoryDictionary = {}

    for option in options:
        select = Select(browser.find_element_by_id('searchDropdownBox'))
        select.select_by_value(option)
        parentCategory = select.first_selected_option.text
        print('parentCategory: {}'.format(parentCategory))

        elem = browser.find_element_by_xpath('//*[@id="nav-search-submit-text"]/input')
        elem.click()
        time.sleep(5)

        BaseCategoryDictionary[parentCategory] = {
            "link": browser.current_url,
            "childs": {}
        }

        time.sleep(2)

        if parentCategory == 'Books' or parentCategory == 'Toys & Games':
            ul = browser.find_element_by_css_selector('#leftNav > ul:nth-child(5) > ul').find_elements_by_tag_name('li')
        elif parentCategory == 'Women\'s Fashion' or parentCategory == 'Men\'s Fashion':
            ul = browser.find_element_by_css_selector('div.left_nav.browseBox > ul').find_elements_by_tag_name('li')
            ul = ul[0:len(ul) - 3]
        elif parentCategory == 'Girls\' Fashion' or parentCategory == 'Boys\' Fashion' or parentCategory == 'Luggage':
            ul = browser.find_element_by_css_selector('div.left_nav.browseBox > ul').find_elements_by_tag_name('li')
            ul = ul[0:len(ul) - 4]
            if parentCategory != 'Luggage':
                print('todo: add school uniforms category later')
        elif parentCategory == 'Software':
            ul = browser.find_element_by_css_selector('#leftNav > ul:nth-child(7) > ul').find_elements_by_tag_name('li')
        else:
            ul = browser.find_element_by_css_selector('#leftNav > ul:nth-child(2) > ul').find_elements_by_tag_name('li')

        for el in ul:
            el_link = el.find_element_by_tag_name('a').get_attribute('href')
            BaseCategoryDictionary[parentCategory]["childs"][el.text] = {
                "link": el_link,
                "childs": {}
            }
    return BaseCategoryDictionary


def buildTreeType1(subCategoriesDict, subCategoriesLink):
    print(subCategoriesLink)
    browser.get(subCategoriesLink)
    time.sleep(2)
    categoryElementsWrapper = browser.find_element_by_css_selector('#s-refinements ul')
    if categoryElementsWrapper:
        categoryElements = categoryElementsWrapper.find_elements_by_css_selector('li.s-navigation-indent-2')
        print(categoryElements)
        if categoryElements and len(categoryElements) > 0:
            print('entered condition 1')
            for categoryElement in categoryElements:
                print(categoryElement.text)
                categoryElementLink = categoryElement.find_element_by_tag_name('a').get_attribute('href')
                categoryElementChilds = {}
                # subCategoriesDict[categoryElement.text] = {
                #     "link": categoryElementLink,
                #     "childs": categoryElementChilds
                # }
                subCategoriesDict[categoryElement.text] = buildTreeType1(categoryElementChilds, categoryElementLink)
        else:
            print('entered condition 2')
            nextCategoryElement = backwardParentTree(categoryElementsWrapper)

            if nextCategoryElement:
                print(nextCategoryElement.text)

                nextCategoryElementLink = nextCategoryElement.find_element_by_tag_name('a').get_attribute('href')
                nextCategoryElementChilds = {}

                subCategoriesDict[nextCategoryElement.text] = {
                    "link": nextCategoryElementLink,
                    "childs": nextCategoryElementChilds
                }

                return buildTreeType1(nextCategoryElementChilds, nextCategoryElementLink)
            else:
                return {}
    else:
        return {}


def backwardParentTree(categoryElementsWrapper):
    currentCategory = categoryElementsWrapper.find_element_by_css_selector('li.s-navigation-indent-1').text
    currentCategoryParents = categoryElementsWrapper.find_elements_by_css_selector(
        'li.a-spacing-micro:not(.s-navigation-indent-1):not(.s-navigation-indent-2)')
    if len(currentCategoryParents)>1:
        lastCategoryParent = currentCategoryParents[len(currentCategoryParents) - 1]
        lastCategoryParentLink = lastCategoryParent.find_element_by_tag_name('a').get_attribute('href')
        print('lastCategoryParent: {}'.format(lastCategoryParent.text))
        print('lastCategoryParentLink: {}'.format(lastCategoryParentLink))

        browser.get(lastCategoryParentLink)
        time.sleep(5)

        lastCategoryParentWrapper = browser.find_element_by_css_selector('#s-refinements ul')
        lastCategoryParentElements = lastCategoryParentWrapper.find_elements_by_css_selector('li.s-navigation-indent-2')
        lastCategoryParentTextElements = list(map(lambda x: x.text, lastCategoryParentElements))
        print('currentCategory: {}'.format(currentCategory))
        print('new block: {}'.format(lastCategoryParentTextElements))

        currentCategoryIndex = lastCategoryParentTextElements.index(currentCategory)
        print(currentCategoryIndex == len(lastCategoryParentElements) - 1)

        if currentCategoryIndex == len(lastCategoryParentElements) - 1:
            return backwardParentTree(lastCategoryParentWrapper)
        else:
            return lastCategoryParentElements[currentCategoryIndex + 1]
    else:
        return None


if __name__ == '__main__':
    browser.get('https://www.amazon.com')

    # CategoryDictionary = buildBaseDepth()
    CategoryDictionary = {
        'Arts & Crafts': {
            'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Darts-crafts-intl-ship&field-keywords=',
            'childs': {'Beading & Jewelry Making': {
                'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_0?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A12896081&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
                'childs': {}}}
        }
    }
    # CategoryDictionary = {'Arts & Crafts': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Darts-crafts-intl-ship&field-keywords=',
    #     'childs': {'Beading & Jewelry Making': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_0?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A12896081&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Crafting': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_1?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A378733011&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Fabric': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_2?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A12899121&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Fabric Decorating': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_3?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A12896841&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Gift Wrapping Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_4?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A723452011&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Knitting & Crochet': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_5?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A12897221&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Needlework': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_6?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A2237329011&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Organization, Storage & Transport': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_7?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A2237594011&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Painting, Drawing & Art Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_8?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A2747968011&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Party Decorations & Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_9?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A723469011&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Printmaking': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_10?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A12898451&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Scrapbooking & Stamping': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_11?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A12898821&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}, 'Sewing': {
    #         'link': 'https://www.amazon.com/s/ref=lp_4954955011_nr_n_12?fst=as%3Aoff&rh=n%3A4954955011%2Cn%3A%212617942011%2Cn%3A12899091&bbn=4954955011&ie=UTF8&qid=1604870650&rnid=2617942011',
    #         'childs': {}}}}, 'Automotive': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dautomotive-intl-ship&field-keywords=',
    #     'childs': {'Car Care': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_0?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15718271&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Car Electronics & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_1?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A2230642011&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Exterior Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_2?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15857511&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Interior Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_3?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15857501&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Lights & Lighting Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_4?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15736321&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Motorcycle & Powersports': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_5?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A346333011&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Oils & Fluids': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_6?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15718791&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Paint & Paint Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_7?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A13591416011&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Performance Parts & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_8?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15710351&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Replacement Parts': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_9?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15719731&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'RV Parts & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_10?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A2258019011&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Tires & Wheels': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_11?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15706571&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Tools & Equipment': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_12?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15706941&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Automotive Enthusiast Merchandise': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_13?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A2204830011&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}, 'Heavy Duty & Commercial Vehicle Equipment': {
    #         'link': 'https://www.amazon.com/s/ref=lp_2562090011_nr_n_14?fst=as%3Aoff&rh=n%3A2562090011%2Cn%3A%2115690151%2Cn%3A15682003011&bbn=2562090011&ie=UTF8&qid=1604870665&rnid=15690151',
    #         'childs': {}}}}, 'Baby': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dbaby-products-intl-ship&field-keywords=',
    #     'childs': {'Activity & Entertainment': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_0?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A239225011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Apparel & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_1?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A7147444011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Baby & Toddler Toys': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_2?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A196601011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Baby Care': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_3?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A17720255011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Baby Stationery': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_4?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A405369011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Car Seats & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_5?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A166835011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Diapering': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_6?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A166764011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Feeding': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_7?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A166777011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Gifts': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_8?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A239226011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Nursery': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_9?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A695338011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Potty Training': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_10?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A166887011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Pregnancy & Maternity': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_11?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A166804011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Safety': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_12?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A166863011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Strollers & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_13?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A8446318011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}, 'Travel Gear': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225005011_nr_n_14?fst=as%3Aoff&rh=i%3Ababy-products-intl-ship%2Cn%3A%2116225005011%2Cn%3A17726796011&bbn=16225005011&ie=UTF8&qid=1604870679&rnid=16225005011',
    #         'childs': {}}}}, 'Beauty & Personal Care': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dbeauty-intl-ship&field-keywords=',
    #     'childs': {'Makeup': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_0?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A11058281&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}, 'Skin Care': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_1?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A11060451&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}, 'Hair Care': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_2?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A11057241&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}, 'Fragrance': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_3?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A11056591&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}, 'Foot, Hand & Nail Care': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_4?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A17242866011&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}, 'Tools & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_5?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A11062741&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}, 'Shave & Hair Removal': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_6?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A3778591&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}, 'Personal Care': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_7?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A3777891&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}, 'Oral Care': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225006011_nr_n_8?fst=as%3Aoff&rh=i%3Abeauty-intl-ship%2Cn%3A%2116225006011%2Cn%3A10079992011&bbn=16225006011&ie=UTF8&qid=1604870716&rnid=16225006011',
    #         'childs': {}}}}, 'Books': {'link': 'https://www.amazon.com/b?node=283155', 'childs': {
    #     'Arts & Photography': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_0?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A1&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Biographies & Memoirs': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_1?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A2&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Business & Money': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_2?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A3&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Calendars': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_3?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A3248857011&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, "Children's Books": {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_4?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A4&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Christian Books & Bibles': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_5?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A12290&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Comics & Graphic Novels': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_6?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A4366&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Computers & Technology': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_7?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A5&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Cookbooks, Food & Wine': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_8?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A6&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Crafts, Hobbies & Home': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_9?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A48&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Education & Teaching': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_10?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A8975347011&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Engineering & Transportation': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_11?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A173507&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Health, Fitness & Dieting': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_12?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A10&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'History': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_13?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A9&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Humor & Entertainment': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_14?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A86&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Law': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_15?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A10777&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Lesbian, Gay, Bisexual & Transgender Books': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_16?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A301889&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Literature & Fiction': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_17?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A17&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Medical Books': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_18?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A173514&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Mystery, Thriller & Suspense': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_19?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A18&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Parenting & Relationships': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_20?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A20&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Politics & Social Sciences': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_21?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A3377866011&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Reference': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_22?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A21&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Religion & Spirituality': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_23?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A22&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Romance': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_24?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A23&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Science & Math': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_25?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A75&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Science Fiction & Fantasy': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_26?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A25&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Self-Help': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_27?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A4736&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Sports & Outdoors': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_28?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A26&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Teen & Young Adult': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_29?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A28&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Test Preparation': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_30?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A5267710011&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}, 'Travel': {
    #         'link': 'https://www.amazon.com/s/ref=lp_283155_nr_n_31?fst=as%3Aoff&rh=n%3A283155%2Cn%3A%211000%2Cn%3A27&bbn=1000&ie=UTF8&qid=1604870748&rnid=1000',
    #         'childs': {}}}}, 'Computers': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dcomputers-intl-ship&field-keywords=',
    #     'childs': {'Computer Accessories & Peripherals': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_0?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A172456&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Computer Components': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_1?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A193870011&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Computers & Tablets': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_2?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A13896617011&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Data Storage': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_3?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A1292110011&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Laptop Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_4?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A3011391011&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Monitors': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_5?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A1292115011&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Networking Products': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_6?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A172504&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Power Strips & Surge Protectors': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_7?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A17854127011&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Printers': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_8?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A172635&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Scanners': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_9?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A172584&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Servers': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_10?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A11036071&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Tablet Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_11?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A2348628011&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Tablet Replacement Parts': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_12?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A15524379011&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}, 'Warranties & Services': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225007011_nr_n_13?fst=as%3Aoff&rh=n%3A16225007011%2Cn%3A16285851&bbn=16225007011&ie=UTF8&qid=1604870894&rnid=16225007011',
    #         'childs': {}}}}, 'Electronics': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Delectronics-intl-ship&field-keywords=',
    #     'childs': {'Accessories & Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_0?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A281407&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Camera & Photo': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_1?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A502394&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Car & Vehicle Electronics': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_2?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A3248684011&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Cell Phones & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_3?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A2811119011&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Computers & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_4?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A541966&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Electronics Warranties': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_5?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A2242348011&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'GPS, Finders & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_6?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A172526&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Headphones': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_7?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A172541&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Home Audio': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_8?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A667846011&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Office Electronics': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_9?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A172574&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Portable Audio & Video': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_10?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A172623&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Security & Surveillance': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_11?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A524136&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Service Plans': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_12?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A16285901&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Television & Video': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_13?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A1266092011&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Video Game Consoles & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_14?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A7926841011&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Video Projectors': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_15?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A300334&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'Wearable Technology': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_16?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A10048700011&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}, 'eBook Readers & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225009011_nr_n_17?fst=as%3Aoff&rh=i%3Aelectronics-intl-ship%2Cn%3A%2116225009011%2Cn%3A2642125011&bbn=16225009011&ie=UTF8&qid=1604870918&rnid=16225009011',
    #         'childs': {}}}}, "Women's Fashion": {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dfashion-womens-intl-ship&field-keywords=',
    #     'childs': {'Clothing': {
    #         'link': 'https://www.amazon.com/s/ref=amb_link_1?ie=UTF8&bbn=16225018011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225018011%2Cn%3A1040660&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_t=101&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_i=16225018011',
    #         'childs': {}}, 'Shoes': {
    #         'link': 'https://www.amazon.com/s/ref=amb_link_2?ie=UTF8&bbn=16225018011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225018011%2Cn%3A679337011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_t=101&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_i=16225018011',
    #         'childs': {}}, 'Jewelry': {
    #         'link': 'https://www.amazon.com/s/ref=amb_link_3?ie=UTF8&bbn=16225018011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225018011%2Cn%3A7192394011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_t=101&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_i=16225018011',
    #         'childs': {}}, 'Watches': {
    #         'link': 'https://www.amazon.com/s/ref=amb_link_4?ie=UTF8&bbn=16225018011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225018011%2Cn%3A6358543011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_t=101&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_i=16225018011',
    #         'childs': {}}, 'Handbags': {
    #         'link': 'https://www.amazon.com/s/ref=amb_link_5?ie=UTF8&bbn=16225018011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225018011%2Cn%3A15743631&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_t=101&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_i=16225018011',
    #         'childs': {}}, 'Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=amb_link_6?ie=UTF8&bbn=16225018011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225018011%2Cn%3A2474936011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_r=WPBYVDR6K3T64W20XCKE&pf_rd_t=101&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_p=0909843d-7d3a-40a7-8b35-6c3da8755bbd&pf_rd_i=16225018011',
    #         'childs': {}}}}, "Men's Fashion": {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dfashion-mens-intl-ship&field-keywords=',
    #     'childs': {'Clothing': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Men_Clothing?ie=UTF8&bbn=16225019011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225019011%2Cn%3A1040658&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=W6Q9G8RZESECX9Y30MT3&pf_rd_r=W6Q9G8RZESECX9Y30MT3&pf_rd_t=101&pf_rd_p=5cd8272b-5ce4-4c26-bfcb-d6dca0c1e427&pf_rd_p=5cd8272b-5ce4-4c26-bfcb-d6dca0c1e427&pf_rd_i=16225019011',
    #         'childs': {}}, 'Shoes': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Men_Shoes?ie=UTF8&bbn=16225019011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225019011%2Cn%3A679255011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=W6Q9G8RZESECX9Y30MT3&pf_rd_r=W6Q9G8RZESECX9Y30MT3&pf_rd_t=101&pf_rd_p=5cd8272b-5ce4-4c26-bfcb-d6dca0c1e427&pf_rd_p=5cd8272b-5ce4-4c26-bfcb-d6dca0c1e427&pf_rd_i=16225019011',
    #         'childs': {}}, 'Watches': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Men_Watches?ie=UTF8&bbn=16225019011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225019011%2Cn%3A6358539011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=W6Q9G8RZESECX9Y30MT3&pf_rd_r=W6Q9G8RZESECX9Y30MT3&pf_rd_t=101&pf_rd_p=5cd8272b-5ce4-4c26-bfcb-d6dca0c1e427&pf_rd_p=5cd8272b-5ce4-4c26-bfcb-d6dca0c1e427&pf_rd_i=16225019011',
    #         'childs': {}}, 'Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Men_Accessories?ie=UTF8&bbn=16225019011&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225019011%2Cn%3A2474937011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=W6Q9G8RZESECX9Y30MT3&pf_rd_r=W6Q9G8RZESECX9Y30MT3&pf_rd_t=101&pf_rd_p=5cd8272b-5ce4-4c26-bfcb-d6dca0c1e427&pf_rd_p=5cd8272b-5ce4-4c26-bfcb-d6dca0c1e427&pf_rd_i=16225019011',
    #         'childs': {}}}}, "Girls' Fashion": {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dfashion-girls-intl-ship&field-keywords=',
    #     'childs': {'Clothing': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Girls_Clothing?bbn=16225020011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225020011%2Cn%3A1040664&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_t=101&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_i=16225020011',
    #         'childs': {}}, 'Shoes': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Girls_Shoes?bbn=16225020011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225020011%2Cn%3A679217011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_t=101&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_i=16225020011',
    #         'childs': {}}, 'Jewelry': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Girls_Jewelry?bbn=16225020011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225020011%2Cn%3A3880961&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_t=101&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_i=16225020011',
    #         'childs': {}}, 'Watches': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Girls_Watches?bbn=16225020011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225020011%2Cn%3A6358547011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_t=101&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_i=16225020011',
    #         'childs': {}}, 'Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Girls_Accessories?bbn=16225020011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225020011%2Cn%3A2474938011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_r=WF083YKW1N05G4TMSWRB&pf_rd_t=101&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_p=590edd7e-7bd2-4b3d-b0e0-acc975fc0961&pf_rd_i=16225020011',
    #         'childs': {}}}}, "Boys' Fashion": {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dfashion-boys-intl-ship&field-keywords=',
    #     'childs': {'Clothing': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Boys_Clothing?bbn=16225021011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225021011%2Cn%3A1040666&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_t=101&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_i=16225021011',
    #         'childs': {}}, 'Shoes': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Boys_Shoes?bbn=16225021011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225021011%2Cn%3A679182011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_t=101&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_i=16225021011',
    #         'childs': {}}, 'Jewelry': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Boys_Jewelry?bbn=16225021011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225021011%2Cn%3A3880611&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_t=101&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_i=16225021011',
    #         'childs': {}}, 'Watches': {
    #         'link': 'https://www.amazon.com/s/ref=AE_boys_Watches?bbn=16225021011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225021011%2Cn%3A6358551011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_t=101&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_i=16225021011',
    #         'childs': {}}, 'Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=AE_boys_Accessories?bbn=16225021011&ie=UTF8&rh=i%3Aspecialty-aps%2Cn%3A7141123011%2Cn%3A16225021011%2Cn%3A2474939011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_r=ZN972RF6Y819S25618KP&pf_rd_t=101&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_p=9b25e25c-9d57-4900-b288-95d6b1ed8fc8&pf_rd_i=16225021011',
    #         'childs': {}}}}, 'Health & Household': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dhpc-intl-ship&field-keywords=', 'childs': {
    #         'Baby & Child Care': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_0?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A10787321&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Health Care': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_1?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A3760941&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Household Supplies': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_2?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A15342811&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Medical Supplies & Equipment': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_3?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A3775161&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Oral Care': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_4?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A10079992011&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Personal Care': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_5?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A3777891&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Sexual Wellness': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_6?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A3777371&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Sports Nutrition': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_7?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A6973663011&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Stationery & Gift Wrapping Supplies': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_8?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A723418011&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Vision Care': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_9?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A10079994011&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Vitamins & Dietary Supplements': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_10?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A3764441&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}, 'Wellness & Relaxation': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225010011_nr_n_11?fst=as%3Aoff&rh=i%3Ahpc-intl-ship%2Cn%3A%2116225010011%2Cn%3A10079996011&bbn=16225010011&ie=UTF8&qid=1604870998&rnid=16225010011',
    #             'childs': {}}}}, 'Home & Kitchen': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dkitchen-intl-ship&field-keywords=',
    #     'childs': {"Kids' Home Store": {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_0?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A3206325011&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Kitchen & Dining': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_1?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A284507&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Bedding': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_2?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A1063252&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Bath': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_3?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A1063236&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Furniture': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_4?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A1063306&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Home Décor': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_5?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A1063278&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Wall Art': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_6?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A3736081&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Lighting & Ceiling Fans': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_7?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A16510975011&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Seasonal Décor': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_8?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A13679381&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Event & Party Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_9?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A901590&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Heating, Cooling & Air Quality': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_10?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A3206324011&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Irons & Steamers': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_11?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A510240&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Vacuums & Floor Care': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_12?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A510106&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Storage & Organization': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_13?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A3610841&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}, 'Cleaning Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225011011_nr_n_14?fst=as%3Aoff&rh=i%3Akitchen-intl-ship%2Cn%3A%2116225011011%2Cn%3A10802561&bbn=16225011011&ie=UTF8&qid=1604871036&rnid=16225011011',
    #         'childs': {}}}}, 'Industrial & Scientific': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dindustrial-intl-ship&field-keywords=',
    #     'childs': {'Abrasive & Finishing Products': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_0?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A256167011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Additive Manufacturing Products': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_1?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A6066126011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Adhesives, Sealants & Lubricants': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_2?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A256225011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Agricultural Irrigation Equipment': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_3?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A13400231&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Commercial Door Products': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_4?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A10773802011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Commercial Lighting': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_5?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A5772192011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Cutting Tools': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_6?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A383598011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Fasteners': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_7?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A383599011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Filtration': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_8?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A3061625011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Food Service Equipment & Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_9?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A6054382011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Hydraulics, Pneumatics & Plumbing': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_10?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A3021479011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Industrial Electrical': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_11?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A306506011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Industrial Hardware': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_12?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A16412251&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Janitorial & Sanitation Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_13?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A317971011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Lab & Scientific Products': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_14?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A317970011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Material Handling Products': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_15?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A256346011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Occupational Health & Safety Products': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_16?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A318135011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Packaging & Shipping Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_17?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A8553197011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Power & Hand Tools': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_18?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A3021459011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Power Transmission Products': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_19?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A16310181&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Professional Dental Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_20?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A8297371011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Professional Medical Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_21?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A8297370011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Raw Materials': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_22?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A16310191&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Retail Store Fixtures & Equipment': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_23?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A8615538011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Robotics': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_24?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A8498884011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Science Education': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_25?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A393459011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}, 'Test, Measure & Inspect': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225012011_nr_n_26?fst=as%3Aoff&rh=i%3Aindustrial-intl-ship%2Cn%3A%2116225012011%2Cn%3A256409011&bbn=16225012011&ie=UTF8&qid=1604871051&rnid=16225012011',
    #         'childs': {}}}}, 'Luggage': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dluggage-intl-ship&field-keywords=',
    #     'childs': {'Carry Ons': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A15743261&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Backpacks': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A360832011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Garment Bags': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A15743271&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Travel Totes': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743241&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Luggage Sets': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A15743291&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Laptop Bags': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A9971584011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Suitcases': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A2477388011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Kids Luggage': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnavn?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743251%2Cn%3A2477386011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Messenger Bags': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743231&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Umbrellas': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15744111&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Duffles': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743211&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}, 'Travel Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=AE_Luggage_leftnav?bbn=16225017011&ie=UTF8&rh=n%3A7141123011%2Cn%3A16225017011%2Cn%3A15743971&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-left-2&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_r=ZTPETT11KJH8XJ2V54VQ&pf_rd_t=101&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_p=92f6b9f6-45a8-4a56-916b-6d695966ee4a&pf_rd_i=16225017011',
    #         'childs': {}}}}, 'Pet Supplies': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dpets-intl-ship&field-keywords=', 'childs': {
    #         'Dogs': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225013011_nr_n_0?fst=as%3Aoff&rh=i%3Apets-intl-ship%2Cn%3A%2116225013011%2Cn%3A2975312011&bbn=16225013011&ie=UTF8&qid=1604871084&rnid=16225013011',
    #             'childs': {}}, 'Cats': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225013011_nr_n_1?fst=as%3Aoff&rh=i%3Apets-intl-ship%2Cn%3A%2116225013011%2Cn%3A2975241011&bbn=16225013011&ie=UTF8&qid=1604871084&rnid=16225013011',
    #             'childs': {}}, 'Fish & Aquatic Pets': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225013011_nr_n_2?fst=as%3Aoff&rh=i%3Apets-intl-ship%2Cn%3A%2116225013011%2Cn%3A2975446011&bbn=16225013011&ie=UTF8&qid=1604871084&rnid=16225013011',
    #             'childs': {}}, 'Birds': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225013011_nr_n_3?fst=as%3Aoff&rh=i%3Apets-intl-ship%2Cn%3A%2116225013011%2Cn%3A2975221011&bbn=16225013011&ie=UTF8&qid=1604871084&rnid=16225013011',
    #             'childs': {}}, 'Horses': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225013011_nr_n_4?fst=as%3Aoff&rh=i%3Apets-intl-ship%2Cn%3A%2116225013011%2Cn%3A2975481011&bbn=16225013011&ie=UTF8&qid=1604871084&rnid=16225013011',
    #             'childs': {}}, 'Reptiles & Amphibians': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225013011_nr_n_5?fst=as%3Aoff&rh=i%3Apets-intl-ship%2Cn%3A%2116225013011%2Cn%3A2975504011&bbn=16225013011&ie=UTF8&qid=1604871084&rnid=16225013011',
    #             'childs': {}}, 'Small Animals': {
    #             'link': 'https://www.amazon.com/s/ref=lp_16225013011_nr_n_6?fst=as%3Aoff&rh=i%3Apets-intl-ship%2Cn%3A%2116225013011%2Cn%3A2975520011&bbn=16225013011&ie=UTF8&qid=1604871084&rnid=16225013011',
    #             'childs': {}}}}, 'Software': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dsoftware-intl-ship&field-keywords=',
    #     'childs': {'Accounting & Finance': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_0?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A5223260011&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Antivirus & Security': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_1?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229677&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Business & Office': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_2?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229535&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, "Children's": {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_3?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229548&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Education & Reference': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_4?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229563&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Lifestyle & Hobbies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_5?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229624&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Music': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_6?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A497022&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Networking & Servers': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_7?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229637&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Operating Systems': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_8?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229653&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Photography & Graphic Design': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_9?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229614&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Programming & Web Development': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_10?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A5223262011&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Tax Preparation': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_11?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229545&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Utilities': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_12?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A229672&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}, 'Video': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225008011_nr_n_13?fst=as%3Aoff&rh=i%3Asoftware-intl-ship%2Cn%3A%2116225008011%2Cn%3A290542&bbn=16225008011&ie=UTF8&qid=1604871099&rnid=16225008011',
    #         'childs': {}}}}, 'Sports & Outdoors': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dsporting-intl-ship&field-keywords=',
    #     'childs': {'Outdoor Recreation': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225014011_nr_n_0?fst=as%3Aoff&rh=i%3Asporting-intl-ship%2Cn%3A%2116225014011%2Cn%3A706814011&bbn=16225014011&ie=UTF8&qid=1604871119&rnid=16225014011',
    #         'childs': {}}, 'Sports & Fitness': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225014011_nr_n_1?fst=as%3Aoff&rh=i%3Asporting-intl-ship%2Cn%3A%2116225014011%2Cn%3A10971181011&bbn=16225014011&ie=UTF8&qid=1604871119&rnid=16225014011',
    #         'childs': {}}, 'Fan Shop': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225014011_nr_n_2?fst=as%3Aoff&rh=i%3Asporting-intl-ship%2Cn%3A%2116225014011%2Cn%3A3386071&bbn=16225014011&ie=UTF8&qid=1604871119&rnid=16225014011',
    #         'childs': {}}}}, 'Tools & Home Improvement': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dtools-intl-ship&field-keywords=',
    #     'childs': {'Appliances': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_0?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A13397451&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Building Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_1?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A551240&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Electrical': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_2?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A495266&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Hardware': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_3?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A511228&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Kitchen & Bath Fixtures': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_4?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A3754161&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Light Bulbs': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_5?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A322525011&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Lighting & Ceiling Fans': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_6?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A495224&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Measuring & Layout Tools': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_7?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A553244&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Paint, Wall Treatments & Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_8?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A228899&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Power & Hand Tools': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_9?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A328182011&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Rough Plumbing': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_10?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A13749581&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Safety & Security': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_11?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A3180231&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Storage & Home Organization': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_12?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A13400631&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}, 'Welding & Soldering': {
    #         'link': 'https://www.amazon.com/s/ref=lp_256643011_nr_n_13?fst=as%3Aoff&rh=n%3A256643011%2Cn%3A%21468240%2Cn%3A8106310011&bbn=256643011&ie=UTF8&qid=1604871140&rnid=468240',
    #         'childs': {}}}}, 'Toys & Games': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dtoys-and-games-intl-ship&field-keywords=',
    #     'childs': {'Arts & Crafts': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_0?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166057011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Baby & Toddler Toys': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_1?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A196601011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Building Toys': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_2?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166092011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Collectible Toys': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_3?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A19431275011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Dolls & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_4?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166118011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Dress Up & Pretend Play': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_5?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166316011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Games & Accessories': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_6?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166220011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Hobbies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_7?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A276729011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, "Kids' Electronics": {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_8?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166164011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, "Kids' Furniture, Décor & Storage": {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_9?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166210011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Learning & Education': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_10?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166269011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Novelty & Gag Toys': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_11?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166027011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Party Supplies': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_12?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A1266203011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Play Vehicles': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_13?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166508011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Puppets & Puppet Theaters': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_14?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166333011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Puzzles': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_15?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166359011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Sports & Outdoor Play': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_16?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166420011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Stuffed Animals & Plush Toys': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_17?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A166461011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Toy Figures & Playsets': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_18?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A165993011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}, 'Tricycles, Scooters & Wagons': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225015011_nr_n_19?fst=as%3Aoff&rh=i%3Atoys-and-games-intl-ship%2Cn%3A%2116225015011%2Cn%3A256994011&bbn=16225015011&ie=UTF8&qid=1604871158&rnid=16225015011',
    #         'childs': {}}}}, 'Video Games': {
    #     'link': 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dvideogames-intl-ship&field-keywords=',
    #     'childs': {'PlayStation 5': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_0?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A20972781011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'PlayStation 4': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_1?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A6427814011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Xbox Series X & S': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_2?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A20972798011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Xbox One': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_3?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A6469269011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Nintendo Switch': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_4?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A16227128011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'PC': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_5?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A229575&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Mac': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_6?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A229647&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Nintendo 3DS & 2DS': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_7?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A2622269011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'PlayStation Vita': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_8?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A3010556011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Legacy Systems': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_9?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A294940&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Online Game Services': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_10?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A17596052011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Microconsoles': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_11?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A19497043011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}, 'Virtual Reality': {
    #         'link': 'https://www.amazon.com/s/ref=lp_16225016011_nr_n_12?fst=as%3Aoff&rh=i%3Avideogames-intl-ship%2Cn%3A%2116225016011%2Cn%3A21479453011&bbn=16225016011&ie=UTF8&qid=1604871185&rnid=16225016011',
    #         'childs': {}}}}}

    for parentCategory, parentItem in CategoryDictionary.items():
        for subCategory, subItem in parentItem['childs'].items():
            print('subCategory: {}'.format(subCategory))
            if parentCategory == 'Books':
                print('build tree type 2')
            else:
                buildTreeType1(subItem['childs'], subItem['link'])

    print(CategoryDictionary)
