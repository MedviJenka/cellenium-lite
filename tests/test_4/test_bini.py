from bini.engine.utils import BiniUtils


screenshot = r'C:\Users\medvi\OneDrive\Desktop\cellenium-lite\core\infrastructure\data\screenshots\a267d6e3-f1a8-4ca0-8eb3-00b8ca996343.png'
bini = BiniUtils()


def test() -> None:
    result = bini.run(image_path=screenshot, prompt='what do you see in this image?')
    assert 'Passed' in result
