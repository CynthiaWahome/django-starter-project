from apps.misc.choices import Choices


# ...existing code...
def test_choices():
    class AccessoryType(Choices):
        WIG = "WIG"
        NECKLACE = ("NC", "Necklace")
        BRACELET = ("BR", "Bracelet")
        EARRINGS = ("EA", "Earrings")
        HANDBAG = ("HB", "Handbag")

    assert set(AccessoryType.keys()) == {"WIG", "NC", "BR", "EA", "HB"}

    assert set(AccessoryType.choices()) == {
        ("WIG", "WIG"),
        ("NC", "Necklace"),
        ("BR", "Bracelet"),
        ("EA", "Earrings"),
        ("HB", "Handbag"),
    }


def test_choices_accessor():
    class AccessoryType(Choices):
        WIG = "WIG"
        NECKLACE = ("NC", "Necklace")
        BRACELET = ("BR", "Bracelet")
        EARRINGS = ("EA", "Earrings")
        HANDBAG = ("HB", "Handbag")

    assert AccessoryType.WIG == "WIG"
    assert AccessoryType.NECKLACE == "NC"
# ...existing code...
