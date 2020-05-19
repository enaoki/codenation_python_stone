from main import classify_by_phone_number, records


class TestChallenge1:

    def test_len(self):
        result = classify_by_phone_number(records)
        print(result)
        assert len(result) == 6

x = TestChallenge1()
x.test_len()