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

    def test_to_mb(self):
        self.assertEqual(animehd.to_mb(1024*1024),1)

    def test_get_download_link(self):
        with open('Naruto Shippuuden (Dub) - Animehd47.com.html') as f:
            html=f.read()
        self.assertEqual(animehd.get_download_link(html),'https://lh3.googleusercontent.com/IOfN537nexgkvYZ9hEDnX9BayKRiaidbYtMhxkTMfYmqbxMNEA-jc2pYOmclgUXrUogqnSkWuiN1JpNkVCYiwzH6X0vWdSYPYcG1PSrYO9xpDI-Xr-M41JvpY_78qfqQ8jR455oT=m22')



if __name__ == '__main__':
    unittest.main()