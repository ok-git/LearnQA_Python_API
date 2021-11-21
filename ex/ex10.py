
class TestPhrase:
    def test_phrase(self):
        phrase = input("Set a phrase: ")
        expected_lenght = 15
        assert len(phrase) < expected_lenght, "Phrase longer than 14 symbols"
