import unittest
import animehd
import os


class TestAnimehd(unittest.TestCase):

    def test_generate_name(self):
        sample_url="https://animehd47.com/naruto-dub/s1-m1/"
        self.assertEqual(animehd.generate_name(sample_url,1),'naruto-dub')
        self.assertEqual(animehd.generate_name(sample_url,2),'s1-m1')

    def test_get_video_folder(self):
        self.assertEqual(animehd.get_video_folder(),os.path.expanduser("~")+'/Videos/')



if __name__ == '__main__':
    unittest.main()