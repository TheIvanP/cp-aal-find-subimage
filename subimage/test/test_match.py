from subimage import SubImgSearch

subimg = SubImgSearch()


def test_img_coords():
    """Test image coordinates match expected position"""
    coords_found = subimg.find_subimage(
        image_to_search="burgers.png",
        matching_image="image_to_find.png",
    )
    assert coords_found == (334, 665)
