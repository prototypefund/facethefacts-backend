# default
import unittest
from unittest.mock import patch
import datetime

# local
import src.api.crud as crud
from tests.db.mock_up_database import mockup_session
import src.db.models as models


class TestCrudFunctions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCrudFunctions, self).__init__(*args, **kwargs)
        self.session = mockup_session

    # unittest
    def test_get_sidejobs_by_politician_id(self):
        actual = []
        results = crud.get_sidejobs_by_politician_id(self.session, 1)
        for result in results:
            item = {
                "id": result.id,
                "label": result.label,
                "income_level": result.income_level,
            }
            actual.append(item)
        expected = [
            {
                "id": 1,
                "label": "Member of the County Council",
                "income_level": "1.000 € bis 3.500 €",
            },
            {
                "id": 2,
                "label": "Chairman",
                "income_level": "3.500 € bis 7.000 €",
            },
        ]

        self.assertListEqual(actual, expected)

    # unittest
    def test_get_latest_bundestag_polls(self):
        actual = []
        results = crud.get_latest_bundestag_polls(self.session)
        for result in results:
            item = {
                "id": result.id,
                "field_legislature_id": result.field_legislature_id,
                "label": result.label,
                "field_intro": result.field_intro,
                "field_poll_date": result.field_poll_date,
            }
            actual.append(item)
        expected = [
            {
                "id": 5,
                "field_legislature_id": 132,
                "label": "Mockup Poll 5",
                "field_intro": "Intro to mockup poll 5.",
                "field_poll_date": datetime.datetime(2021, 10, 5),
            },
            {
                "id": 6,
                "field_legislature_id": 132,
                "label": "Mockup Poll 6",
                "field_intro": "Intro to mockup poll 6.",
                "field_poll_date": datetime.datetime(2021, 10, 6),
            },
            {
                "id": 7,
                "field_legislature_id": 132,
                "label": "Mockup Poll 7",
                "field_intro": "Intro to mockup poll 7.",
                "field_poll_date": datetime.datetime(2021, 10, 7),
            },
        ]
        self.assertEqual(actual, expected)

    # unittest
    def test_get_vote_result_by_poll_id(self):
        result = crud.get_vote_result_by_poll_id(self.session, 5)
        actual = {
            "id": result.id,
            "yes": result.yes,
            "no": result.no,
            "abstain": result.abstain,
            "no_show": result.no_show,
            "poll_id": result.poll_id,
        }
        expected = {
            "id": 1,
            "yes": 5,
            "no": 10,
            "abstain": 10,
            "no_show": 0,
            "poll_id": 5,
        }
        not_expected = {
            "id": 3,
            "yes": 10,
            "no": 10,
            "abstain": 0,
            "no_show": 2,
            "poll_id": 10,
        }
        self.assertEqual(actual, expected)
        self.assertNotEqual(actual, not_expected)

    # integration test
    def test_integration_test_get_polls_total(self):
        results = crud.get_polls_total(self.session)
        result_first = results[0]
        actual = {
            "poll": {
                "field_legislature_id": result_first["poll"]["field_legislature_id"],
                "id": result_first["poll"]["id"],
                "label": result_first["poll"]["label"],
                "field_intro": result_first["poll"]["field_intro"],
                "field_poll_date": result_first["poll"]["field_poll_date"],
                "poll_passed": result_first["poll"]["poll_passed"],
            },
            "result": {
                "yes": result_first["result"].yes,
                "no": result_first["result"].no,
                "abstain": result_first["result"].abstain,
                "no_show": result_first["result"].no_show,
            },
        }
        expected = {
            "poll": {
                "field_legislature_id": 132,
                "id": 5,
                "label": "Mockup Poll 5",
                "field_intro": "Intro to mockup poll 5.",
                "field_poll_date": datetime.datetime(2021, 10, 5),
                "poll_passed": False,
            },
            "result": {"yes": 5, "no": 10, "abstain": 10, "no_show": 0},
        }
        self.assertEqual(actual, expected)

    # unittest
    @patch(
        "src.api.crud.load_json_from_url",
        return_value={"meta": {"results": {"count": 0, "total": 0}}},
    )
    def test_get_politician_speech_empty(self, empty_data):
        actual = crud.get_politician_speech(119742, 1)
        expected = None
        self.assertEqual(actual, expected)

    @patch(
        "src.api.crud.load_json_from_url",
        return_value={
            "meta": {"results": {"count": 1, "total": 10}},
            "data": [
                {
                    "attributes": {"videoFileURI": "url_1", "dateStart": "2022-01-01"},
                    "relationships": {
                        "agendaItem": {"data": {"attributes": {"title": "title_1"}}}
                    },
                }
            ],
        },
    )
    def test_get_politician_speech(self, data):
        actual = crud.get_politician_speech(119742, 1)
        expected = {
            "items": [
                {"videoFileURI": "url_1", "title": "title_1", "date": "2022-01-01"}
            ],
            "total": 10,
            "page": 1,
            "size": 1,
            "politician_id": 119742,
            "is_last_page": True,
        }
        self.assertEqual(actual, expected)

    # integration_test
    def test_integration_test_get_politician_speech(self):
        actual = crud.get_politician_speech(119742, 1)
        actual_items = actual["items"]
        actual_is_last_page = actual["is_last_page"]
        expected = [
            {
                "videoFileURI": "https://cldf-od.r53.cdn.tv1.eu/1000153copo/ondemand/app144277506/145293313/7531965/7531965_h264_720_400_2000kb_baseline_de_2192.mp4",
                "title": "Vereinbarte Debatte zur Situation in Deutschland",
                "date": "2021-09-07T08:24:16",
            },
            {
                "videoFileURI": "https://cldf-od.r53.cdn.tv1.eu/1000153copo/ondemand/app144277506/145293313/7531848/7531848_h264_720_400_2000kb_baseline_de_2192.mp4",
                "title": "Regierungserklärung der BKn zur Lage in Afghanistan, Bundeswehreinsatz zur Evakuierung aus Afghanistan",
                "date": "2021-08-25T10:54:47",
            },
            {
                "videoFileURI": "https://cldf-od.r53.cdn.tv1.eu/1000153copo/ondemand/app144277506/145293313/7530596/7530596_h264_720_400_2000kb_baseline_de_2192.mp4",
                "title": "Regierungserklärung zum Europäischen Rat",
                "date": "2021-06-24T07:37:40",
            },
        ]
        for item in expected:
            assert item in actual_items
        self.assertEqual(actual_is_last_page, False)


if __name__ == "__main__":
    unittest.main()
