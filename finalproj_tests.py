import unittest
from finalproj import *

class DataGrab(unittest.TestCase):
    def testGetSections(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        sections_list = get_sections()
        self.assertTrue(len(sections_list) == 4)
        self.assertTrue(type(sections_list) == list)
        self.assertTrue(type(sections_list[0]) == Section)

    def testGetArticles(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        sections_list = get_sections()
        articles_list = get_articles(sections_list)
        self.assertTrue(len(articles_list) > 100)
        self.assertTrue(type(articles_list) == list)
        self.assertTrue(type(articles_list[0]) == tuple)

class DataStore(unittest.TestCase):
    def test_section_data(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        cur.execute('SELECT SectionName FROM Sections')
        y = cur.fetchall()
        self.assertTrue(len(y) != 0)

        cur.execute('SELECT Id FROM Sections WHERE SectionName = "Opinions"')
        y = cur.fetchall()
        self.assertEqual(y[0][0], 1)

        cur.execute('SELECT Id FROM Sections WHERE SectionName = "Politics"')
        y = cur.fetchall()
        self.assertEqual(y[0][0], 2)

        cur.execute('SELECT Id FROM Sections WHERE SectionName = "World"')
        y = cur.fetchall()
        self.assertEqual(y[0][0], 3)

        cur.execute('SELECT Id FROM Sections WHERE SectionName = "Home"')
        y = cur.fetchall()
        self.assertEqual(y[0][0], 4)

class DataProcess(unittest.TestCase):
    def test_interactive_fns(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        world_test = get_world()
        self.assertEqual(type(world_test), list)
        self.assertEqual(len(world_test[0]), 2)
        self.assertEqual(type(world_test[0]), tuple)

    def test_most_pop_author(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()
        most_pop_author = get_most_pop_authors()
        t = (most_pop_author,)
        cur.execute('SELECT Id FROM Articles WHERE Author = ?', t)
        x = cur.fetchall()
        self.assertTrue(len(x) > 0)

    def test_plotly_charts(self):
        conn = sqlite3.connect('final_project.db')
        cur = conn.cursor()

        test_pie = countSectionArticles()
        self.assertEqual(len(test_pie), 4)

        test_headline_lengths = plotHeadlineLengths()
        keys = list(test_headline_lengths.keys())
        first = keys[0]
        first_value = test_headline_lengths[first]
        self.assertTrue(len(first_value) != 0)

        test_unique_author = uniqueAuthorsBySection()
        keys = list(test_unique_author.keys())
        first = keys[0]
        first_value = test_unique_author[first]
        self.assertEqual(type(first_value), int)

        test_time_by_section = timeOfDayBySection()
        keys = list(test_time_by_section.keys())
        first = keys[0]
        first_value = test_time_by_section[first]
        self.assertEqual(len(list(first_value.keys())), 4)






unittest.main()
