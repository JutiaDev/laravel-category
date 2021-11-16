#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 00:05:48 2020

@author: abdelhamid abouhassane
"""


def build_tree(tree_dict, tree_list):
    if tree_list:
        if tree_list[0] not in tree_dict:
            tree_dict[tree_list[0]] = {}
        build_tree(tree_dict[tree_list[0]], tree_list[1:])
    return {}


taxonomy = open('taxonomy.en-US-2019-07-10.txt', 'r')
Lines = taxonomy.readlines()

CategoryDictionary = {}

count = 0
# Strips the newline character
for line in Lines:
    count += 1
    if count > 1:
        Categories = line.strip().split(" > ")
        build_tree(CategoryDictionary, Categories)

print(CategoryDictionary)
