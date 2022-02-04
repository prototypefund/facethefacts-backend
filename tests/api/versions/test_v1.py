from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_read_politician():
    def random_test():
        response = client.get("/v1/politician/178104")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.status_code == 200
        assert response.json()["id"] == 178104
        assert response.json()["entity_type"] == "politician"
        assert response.json()["label"] == "Thomas Frost"
        assert response.json()["first_name"] == "Thomas"
        assert response.json()["last_name"] == "Frost"
        assert response.json()["sex"] == "m"
        assert response.json()["year_of_birth"] == "1985"
        assert response.json()["deceased"] is None
        assert response.json()["deceased_date"] is None
        assert (
            response.json()["education"]
            == "Erzieher/ Kitaleiter, Werkzeugmechaniker, Waffenmechaniker"
        )
        assert response.json()["residence"] == "Mestlin "
        assert response.json()["statistic_questions"] is None
        assert response.json()["statistic_questions_answered"] is None
        assert response.json()["qid_wikidata"] is None
        assert response.json()["field_title"] is None

    def specific_elements_test1():
        # Testing past_party, statistic_questions and statistic_questions_answered
        response = client.get("/v1/politician/176101")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["statistic_questions"] == "10"
        assert response.json()["statistic_questions_answered"] == "9"

    def specific_elements_test_2():
        # Testing deceased, deceased_date and qid_wikidata
        response = client.get("/v1/politician/79107")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["deceased"] is True
        assert response.json()["deceased_date"] == "2020-10-25"
        assert response.json()["qid_wikidata"] == "Q90833"

    def specific_elements_test_3():
        # Testing field_title
        response = client.get("/v1/politician/79109")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["field_title"] == "Dr."

    def votes_and_polls_test():
        response = client.get("/v1/politician/73426?sidejobs_end=0")
        assert response.status_code == 200
        assert type(response.json()) is dict

        votes_and_polls = response.json()["votes_and_polls"]
        assert type(votes_and_polls) is list
        assert len(votes_and_polls) == 5

        for index in range(4):
            assert (
                votes_and_polls[index]["Poll"]["field_poll_date"]
                >= votes_and_polls[index + 1]["Poll"]["field_poll_date"]
            )

    def politician_id_not_found():
        response = client.get("/v1/politician/1")
        assert response.status_code == 404
        assert type(response.json()) is dict
        assert response.json() == {"detail": "Politician not found"}

    def occupations_test():
        response = client.get("/v1/politician/130072")
        response_items = [
            "Kanzlerkandidat",
            "Ministerpräsident NRW",
            "Parteivorsitzender",
            "MdL",
        ]

        for item in response_items:
            assert item in response.json()["occupations"]

    def test_topic_ids_of_latest_committee():
        response = client.get("/v1/politician/131019")
        expected_ids = [11, 19]
        assert expected_ids == response.json()["topic_ids_of_latest_committee"]

        response = client.get("/v1/politician/139064")
        expected_ids = [9, 11, 19, 20]
        assert expected_ids == response.json()["topic_ids_of_latest_committee"]

    random_test()
    specific_elements_test1()
    specific_elements_test_2()
    specific_elements_test_3()
    votes_and_polls_test()
    politician_id_not_found()
    occupations_test()
    test_topic_ids_of_latest_committee()


def test_read_top_candidates():
    response = client.get("/v1/top-candidates")
    assert response.status_code == 200
    assert type(response.json()) is list
    assert response.json() == [
        {
            "id": 130072,
            "label": "Armin Laschet",
            "party": {
                "id": 2,
                "label": "CDU",
                "party_style": {
                    "id": 2,
                    "display_name": "CDU",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#636363",
                    "border_color": None,
                },
            },
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/130072.jpg",
        },
        {
            "id": 79475,
            "label": "Annalena Baerbock",
            "party": {
                "id": 5,
                "label": "Bündnis 90/Die Grünen",
                "party_style": {
                    "id": 5,
                    "display_name": "Grüne",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#61A056",
                    "border_color": None,
                },
            },
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/79475.jpg",
        },
        {
            "id": 66924,
            "label": "Olaf Scholz",
            "party": {
                "id": 1,
                "label": "SPD",
                "party_style": {
                    "id": 1,
                    "display_name": "SPD",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#E95050",
                    "border_color": None,
                },
            },
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/66924.jpg",
        },
        {
            "id": 119742,
            "label": "Christian Lindner",
            "party": {
                "id": 4,
                "label": "FDP",
                "party_style": {
                    "id": 4,
                    "display_name": "FDP",
                    "foreground_color": "#333333",
                    "background_color": "#FAED0B",
                    "border_color": None,
                },
            },
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/119742.jpg",
        },
        {
            "id": 145755,
            "label": "Tino Chrupalla",
            "party": {
                "id": 9,
                "label": "AfD",
                "party_style": {
                    "id": 9,
                    "display_name": "AfD",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#3AA6F4",
                    "border_color": None,
                },
            },
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/145755.jpg",
        },
        {
            "id": 108379,
            "label": "Alice Weidel",
            "party": {
                "id": 9,
                "label": "AfD",
                "party_style": {
                    "id": 9,
                    "display_name": "AfD",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#3AA6F4",
                    "border_color": None,
                },
            },
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/108379.jpg",
        },
        {
            "id": 135302,
            "label": "Janine Wissler",
            "party": {
                "id": 8,
                "label": "DIE LINKE",
                "party_style": {
                    "id": 8,
                    "display_name": "Linke",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#CD3E72",
                    "border_color": None,
                },
            },
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/135302.jpg",
        },
        {
            "id": 79454,
            "label": "Dietmar Bartsch",
            "party": {
                "id": 8,
                "label": "DIE LINKE",
                "party_style": {
                    "id": 8,
                    "display_name": "Linke",
                    "foreground_color": "#FFFFFF",
                    "background_color": "#CD3E72",
                    "border_color": None,
                },
            },
            "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/79454.jpg",
        },
    ]


def test_read_politician_constituencies():
    def all_elements_have_values():
        response = client.get("/v1/politician/138540/constituencies")
        assert response.status_code == 200
        assert type(response.json()) is list
        assert response.json() == [
            {
                "id": 177853,
                "label": "Ute Elisabeth Weisang",
                "party": {
                    "id": 201,
                    "label": "dieBasis",
                    "party_style": {
                        "id": 201,
                        "display_name": "dieBasis",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#333333",
                        "border_color": None,
                    },
                },
                "image_url": None,
            },
            {
                "id": 138292,
                "label": "Maria Luise Herber",
                "party": {
                    "id": 5,
                    "label": "Bündnis 90/Die Grünen",
                    "party_style": {
                        "id": 5,
                        "display_name": "Grüne",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#61A056",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/138292.jpg",
            },
            {
                "id": 177232,
                "label": "Florian Spaniol",
                "party": {
                    "id": 8,
                    "label": "DIE LINKE",
                    "party_style": {
                        "id": 8,
                        "display_name": "Linke",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#CD3E72",
                        "border_color": None,
                    },
                },
                "image_url": None,
            },
            {
                "id": 176099,
                "label": "Evelyne Görlinger",
                "party": {
                    "id": 16,
                    "label": "Die PARTEI",
                    "party_style": {
                        "id": 16,
                        "display_name": "Die PARTEI",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#722B2B",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/176099.jpg",
            },
            {
                "id": 176057,
                "label": "Claus Jacob",
                "party": {
                    "id": 12,
                    "label": "ÖDP",
                    "party_style": {
                        "id": 12,
                        "display_name": "ÖDP",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#FD820B",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/176057.jpg",
            },
            {
                "id": 147500,
                "label": "Axel Kammerer",
                "party": {
                    "id": 7,
                    "label": "FREIE WÄHLER",
                    "party_style": {
                        "id": 7,
                        "display_name": "FREIE WÄHLER",
                        "foreground_color": "#2F5997",
                        "background_color": "#F8F8F8",
                        "border_color": "#FD820B",
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/147500.jpg",
            },
            {
                "id": 150296,
                "label": "Christian-Friedrich Wirth",
                "party": {
                    "id": 9,
                    "label": "AfD",
                    "party_style": {
                        "id": 9,
                        "display_name": "AfD",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#3AA6F4",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/150296.jpg",
            },
            {
                "id": 138540,
                "label": "Markus Uhl",
                "party": {
                    "id": 2,
                    "label": "CDU",
                    "party_style": {
                        "id": 2,
                        "display_name": "CDU",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#636363",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/138540.jpg",
            },
            {
                "id": 175796,
                "label": "Ralf Armbrüster",
                "party": {
                    "id": 4,
                    "label": "FDP",
                    "party_style": {
                        "id": 4,
                        "display_name": "FDP",
                        "foreground_color": "#333333",
                        "background_color": "#FAED0B",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/175796.jpg",
            },
            {
                "id": 138463,
                "label": "Esra Limbacher",
                "party": {
                    "id": 1,
                    "label": "SPD",
                    "party_style": {
                        "id": 1,
                        "display_name": "SPD",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#E95050",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/138463.jpg",
            },
        ]

    def null_constituencies_exist():
        response = client.get("/v1/politician/138124/constituencies")
        assert response.status_code == 200
        assert type(response.json()) is list
        assert response.json() == [
            {
                "id": 177845,
                "label": "Steffi Richter",
                "party": {
                    "id": 201,
                    "label": "dieBasis",
                    "party_style": {
                        "id": 201,
                        "display_name": "dieBasis",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#333333",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/177845.jpg",
            },
            {
                "id": 177566,
                "label": "Boris Huebner",
                "party": {
                    "id": 9,
                    "label": "AfD",
                    "party_style": {
                        "id": 9,
                        "display_name": "AfD",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#3AA6F4",
                        "border_color": None,
                    },
                },
                "image_url": None,
            },
            {
                "id": 148443,
                "label": "Rolf Tickert",
                "party": {
                    "id": 15,
                    "label": "MLPD",
                    "party_style": {
                        "id": 15,
                        "display_name": "MLPD",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#333333",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/148443.jpg",
            },
            {
                "id": 164999,
                "label": "Gerhard Wenz",
                "party": {
                    "id": 5,
                    "label": "Bündnis 90/Die Grünen",
                    "party_style": {
                        "id": 5,
                        "display_name": "Grüne",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#61A056",
                        "border_color": None,
                    },
                },
                "image_url": None,
            },
            {
                "id": 177290,
                "label": "Stephan Poss",
                "party": {
                    "id": 185,
                    "label": "parteilos",
                    "party_style": {
                        "id": 185,
                        "display_name": "parteilos",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#333333",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/177290.jpg",
            },
            {
                "id": 177230,
                "label": "Mark Baumeister",
                "party": {
                    "id": 8,
                    "label": "DIE LINKE",
                    "party_style": {
                        "id": 8,
                        "display_name": "Linke",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#CD3E72",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/177230.jpg",
            },
            {
                "id": 176255,
                "label": "Nico Herrmann",
                "party": {
                    "id": 12,
                    "label": "ÖDP",
                    "party_style": {
                        "id": 12,
                        "display_name": "ÖDP",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#FD820B",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/176255.jpg",
            },
            {
                "id": 176204,
                "label": "Luman Matheis Lukas",
                "party": {
                    "id": 16,
                    "label": "Die PARTEI",
                    "party_style": {
                        "id": 16,
                        "display_name": "Die PARTEI",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#722B2B",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/176204.jpg",
            },
            {
                "id": 176123,
                "label": "Hans-Peter Pflug",
                "party": {
                    "id": 7,
                    "label": "FREIE WÄHLER",
                    "party_style": {
                        "id": 7,
                        "display_name": "FREIE WÄHLER",
                        "foreground_color": "#2F5997",
                        "background_color": "#F8F8F8",
                        "border_color": "#FD820B",
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/176123.jpg",
            },
            {
                "id": 138124,
                "label": "Annegret Kramp-Karrenbauer",
                "party": {
                    "id": 2,
                    "label": "CDU",
                    "party_style": {
                        "id": 2,
                        "display_name": "CDU",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#636363",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/138124.jpg",
            },
            {
                "id": 175734,
                "label": "Helmut Isringhaus",
                "party": {
                    "id": 4,
                    "label": "FDP",
                    "party_style": {
                        "id": 4,
                        "display_name": "FDP",
                        "foreground_color": "#333333",
                        "background_color": "#FAED0B",
                        "border_color": None,
                    },
                },
                "image_url": None,
            },
            {
                "id": 146867,
                "label": "Josephine Ortleb",
                "party": {
                    "id": 1,
                    "label": "SPD",
                    "party_style": {
                        "id": 1,
                        "display_name": "SPD",
                        "foreground_color": "#FFFFFF",
                        "background_color": "#E95050",
                        "border_color": None,
                    },
                },
                "image_url": "https://candidate-images.s3.eu-central-1.amazonaws.com/146867.jpg",
            },
        ]

    all_elements_have_values()
    null_constituencies_exist()


def test_read_politician_positions():
    def selected_values_test():
        response = client.get("/v1/politician/177592/positions")
        assert response.status_code == 200
        assert type(response.json()) is dict
        assert response.json()["positions"].__contains__(
            {
                "id": 1281775921,
                "position": "neutral",
                "reason": "Das hohe Verkehrsaufkommen lässt eine höhere Durchschnittsgeschwindigkeit nach meinem Gefühl nicht zu. das ist rein subjketiv. ",
                "position_statement": {
                    "statement": "Auf den Autobahnen soll ein Tempolimit von 130km/h eingeführt werden."
                },
            }
        )
        assert response.json()["positions"].__contains__(
            {
                "id": 1281775926,
                "position": "neutral",
                "reason": None,
                "position_statement": {
                    "statement": "Der öffentlich-rechtliche Rundfunk soll sich auf Information und regionale Berichterstattung konzentrieren."
                },
            }
        )

    selected_values_test()


def test_read_politician_sidejobs():
    def whole_values_test():
        response = client.get("/v1/politician/119742/sidejobs?page=1&size=50")
        assert response.status_code == 200
        response_items = [
            {
                "id": 11693,
                "entity_type": "sidejob",
                "label": "Vortrag (Sommergespräch)",
                "income_level": "7.000 € bis 15.000 €",
                "interval": None,
                "created": "2021-09-10",
                "sidejob_organization": {
                    "id": 2668,
                    "entity_type": "sidejob_organization",
                    "label": "Lupus Alpha Asset Management GmbH",
                },
            },
            {
                "id": 11599,
                "entity_type": "sidejob",
                "label": "Vortrag - Executive Dinner, Donner & Reuschel AG, Hamburg",
                "income_level": "7.000 € bis 15.000 €",
                "interval": None,
                "created": "2021-08-05",
                "sidejob_organization": {
                    "id": 4086,
                    "entity_type": "sidejob_organization",
                    "label": "Galler & Company",
                },
            },
            {
                "id": 11600,
                "entity_type": "sidejob",
                "label": "Online-Vortrag - Keynote Human-Works-Kongress",
                "income_level": "3.500 € bis 7.000 €",
                "interval": None,
                "created": "2021-08-05",
                "sidejob_organization": {
                    "id": 4087,
                    "entity_type": "sidejob_organization",
                    "label": "Mercer Deutschland GmbH",
                },
            },
        ]
        for item in response_items:
            assert item in response.json()["items"]

    def selected_values_test():
        response = client.get("/v1/politician/119742/sidejobs?page=1&size=1")
        assert response.status_code == 200
        assert response.json()["items"][0]["sidejob_organization"] == {
            "id": 2668,
            "entity_type": "sidejob_organization",
            "label": "Lupus Alpha Asset Management GmbH",
        }

    def sidejob_not_found_test():
        response = client.get("/v1/politician/28881/sidejobs?page=2&size=1")
        assert response.status_code == 404
        assert response.json() == {"detail": "Sidejobs not found"}

    whole_values_test()
    selected_values_test()
    sidejob_not_found_test()


def test_read_politician_image_scanner():
    def label_and_id_test():
        response = client.get("/v1/image-scanner?text=ronald")
        assert response.status_code == 200
        assert type(response.json()) is list
        test_responses = [
            {"id": 137636, "label": "Ronald Kaufmann"},
            {"id": 178064, "label": "Ronald Günter Wetklo"},
            {
                "id": 177893,
                "label": "Ronald Rüdiger",
            },
        ]

        for item in test_responses:
            check_response = False
            for response_item in response.json():
                if (
                    item["id"] == response_item["id"]
                    and item["label"] == response_item["label"]
                ):
                    check_response = True
                    break
            assert check_response, "{} item not fount in the response".format(item)

    label_and_id_test()


def test_read_politician_search():
    def selected_values_test():
        response = client.get("/v1/search?text=55278")
        assert response.status_code == 200
        assert type(response.json()) is list
        test_responses = [
            {"id": 177457, "label": "Chiara Pohl"},
            {"id": 175546, "label": "Christian Engelke"},
            {"id": 176888, "label": "David Hess"},
        ]

        for item in test_responses:
            check_response = False
            for response_item in response.json():
                if (
                    item["id"] == response_item["id"]
                    and item["label"] == response_item["label"]
                ):
                    check_response = True
                    break
            assert check_response, "{} item not fount in the response".format(item)

    def test_response_size():
        response = client.get("/v1/search?text=Christian")
        assert len(response.json()) <= 10

    selected_values_test()
    test_response_size()


def test_read_politician_votes():
    def no_filters_random_test():
        response = client.get("/v1/politician/79454/votes")
        test_responses = [
            {
                "Vote": {
                    "id": 410777,
                    "entity_type": "vote",
                    "label": "Dietmar Bartsch - Unternehmerische Sorgfaltspflichten in Lieferketten",
                    "api_url": "https://www.abgeordnetenwatch.de/api/v2/votes/410777",
                    "mandate_id": 46023,
                    "fraction_id": 41,
                    "poll_id": 4199,
                    "vote": "abstain",
                    "reason_no_show": None,
                    "reason_no_show_other": None,
                },
                "Poll": {
                    "id": 4199,
                    "label": "Unternehmerische Sorgfaltspflichten in Lieferketten",
                    "field_intro": '<p>Der Gesetzentwurf der Bundesregierung soll die Sicherung von Menschenrechten und Umweltstandards für deutsche Unternehmen im internationalen Handel bedeuten. Lieferketten sollen nachweislich fair sein.</p>\r\n\r\n<p>Der Gesetzentwurf wurde mit den Stimmen der Fraktionen CDU/CSU, SPD und B90/DIE GRÜNEN angenommen. Ablehnung erhielt der Entwurf von den Fraktionen AfD und FDP. Entgegen des Fraktionsdrucks stimmten auch 10 Abgeordnete der CDU mit NEIN, darunter <a href="https://www.abgeordnetenwatch.de/profile/axel-eduard-fischer">Axel Eduard Fischer</a>, <a href="https://www.abgeordnetenwatch.de/profile/hans-juergen-irmer">Hans-Jürgen Irmer</a> und <a href="https://www.abgeordnetenwatch.de/profile/andreas-laemmel">Andreas Lämmel</a>. Die Fraktion DIE LINKE enthielt sich, mit Ausnahme von <a href="https://www.abgeordnetenwatch.de/profile/ulla-jelpke">Ulla Jelpke</a>, die mit JA stimmte. Insgesamt stimmten 412 Abgeordnete für den Antrag und 159 Abgeordnete dagegen.</p>\r\n\r\n<p>&nbsp;</p>\r\n',
                    "field_poll_date": "2021-06-11",
                    "poll_passed": True,
                },
            },
        ]

        for item in test_responses:
            assert item in response.json()["items"]

    def response_size_by_filters_test():
        complete_response_total = client.get("/v1/politician/119742/votes").json()[
            "total"
        ]
        single_filter_response_total = client.get(
            "/v1/politician/119742/votes?filters=2"
        ).json()["total"]
        double_filter_response_total = client.get(
            "/v1/politician/119742/votes?filters=2&filters=1"
        ).json()["total"]
        triple_filter_response_total = client.get(
            "/v1/politician/119742/votes?filters=2&filters=1&filters=6"
        ).json()["total"]

        assert complete_response_total >= triple_filter_response_total
        assert triple_filter_response_total >= double_filter_response_total
        assert double_filter_response_total >= single_filter_response_total

    no_filters_random_test()
    response_size_by_filters_test()


def test_read_poll_details():
    def random_test():
        response = client.get("/v1/poll/4217/details")
        assert response.status_code == 200
        response_items = [
            {
                "id": 7585,
                "poll_id": 4217,
                "fraction": {
                    "id": 14,
                    "full_name": "FDP",
                    "short_name": "FDP",
                    "label": "FDP (Bundestag 2017 - 2021)",
                },
                "total_yes": 0,
                "total_no": 71,
                "total_abstain": 0,
                "total_no_show": 9,
            },
            {
                "id": 7590,
                "poll_id": 4217,
                "fraction": {
                    "id": 153,
                    "full_name": "DIE GRÜNEN",
                    "short_name": "DIE GRÜNEN",
                    "label": "DIE GRÜNEN (Bundestag 2017 - 2021)",
                },
                "total_yes": 62,
                "total_no": 0,
                "total_abstain": 0,
                "total_no_show": 5,
            },
        ]
        for item in response_items:
            assert item in response.json()

    def test_unique_fractions_in_response():
        response = client.get("/v1/poll/4174/details")
        fraction_ids = []
        for item in response.json():
            fraction_id = item["fraction"]["id"]
            assert (
                fraction_id not in fraction_ids
            ), f"duplicate fraction of id {fraction_id} in response. All objects must have a unique fraction id"
            fraction_ids.append(fraction_id)

    def test_same_poll_id_in_response():
        poll_id = 713
        response = client.get(f"/v1/poll/{poll_id}/details")

        for item in response.json():
            assert (
                item["poll_id"] == poll_id
            ), f"Item of id {item['id']} is returned with poll_id {item['poll_id']}. Only items with poll_id {poll_id} should be returned"

    random_test()
    test_unique_fractions_in_response()
    test_same_poll_id_in_response()


def test_read_politician_media():
    def selected_values_test():
        response = client.get("/v1/politician/119742/speeches?page=5")
        response_items = [
            {
                "videoFileURI": "https://cldf-od.r53.cdn.tv1.eu/1000153copo/ondemand/app144277506/145293313/7227221/7227221_h264_720_400_2000kb_baseline_de_2192.mp4",
                "title": "Bundeskanzlerin und Bundeskanzleramt",
                "date": "2018-05-16T07:56:56",
            },
            {
                "videoFileURI": "https://cldf-od.r53.cdn.tv1.eu/1000153copo/ondemand/app144277506/145293313/7211358/7211358_h264_720_400_2000kb_baseline_de_2192.mp4",
                "title": "Generalaussprache (einschl. Kultur sowie Digitales)",
                "date": "2018-03-21T13:31:50",
            },
        ]

        for item in response_items:
            assert item in response.json()["items"]
        assert response.json()["is_last_page"] is True

    def selected_invalid_values_test():
        response = client.get("/v1/politician/119742/speeches?page=6")
        expected = {"detail": "Politician Speech not found"}
        assert response.json() == expected

    selected_values_test()
    selected_invalid_values_test()


def test_read_politician_news():
    def values_test():
        response = client.get("/v1/politician/145862/news")
        expected_items = [
            {
                "id": "024810dce7f23322cef7801e4e13402cc8956af7d2d9c2b77260a7723c2bb89b",
                "highlight": None,
                "images": [],
                "published": "2021-08-13T12:58:54.705000",
                "source": "tagesschau",
                "title": "Wahlrechtsreform: Viel Lärm um wenig",
                "url": "https://www.tagesschau.de/inland/btw21/eilantrag-wahlrechtsreform-103.html",
            },
            {
                "id": "06f776204f16e52e90aafbe6553c5782acdd494a00c0c5f4dbb20dffd016ede5",
                "highlight": None,
                "images": [
                    {
                        "url": "https://bilder.bild.de/fotos-skaliert/von-der-polizei-erwischt-gruenen-politikerin-beschaedigt-wahlplakate-von-fdp-und-cdu-b5084ae811c14489a90a0fbef6ac9718-77564960/20,c=0,h=720.bild.jpg",
                        "title": None,
                        "height": 720,
                        "width": 1280,
                    },
                    {
                        "url": "https://bilder.bild.de/fotos-skaliert/von-der-polizei-erwischt-gruenen-politikerin-beschaedigt-wahlplakate-von-fdp-und-cdu-b5084ae811c14489a90a0fbef6ac9718-77564998/20,c=0,h=658.bild.jpg",
                        "title": None,
                        "height": 658,
                        "width": 658,
                    },
                    {
                        "url": "https://bilder.bild.de/fotos-skaliert/von-der-polizei-erwischt-gruenen-politikerin-beschaedigt-wahlplakate-von-fdp-und-cdu-b5084ae811c14489a90a0fbef6ac9718-77565032/20,c=0,h=1026.bild.jpg",
                        "title": None,
                        "height": 1026,
                        "width": 864,
                    },
                ],
                "published": "2021-09-02T16:38:20",
                "source": "bild",
                "title": "Von der Polizei erwischt: Grünen-Politikerin beschädigt Wahlplakate von FDP und CDU",
                "url": "https://www.bild.de/politik/inland/politik/gruenen-politikerin-soll-wahlplakate-von-fdp-und-cdu-beschmiert-haben-77563930.bild.html",
            },
        ]

        for item in expected_items:
            assert item in response.json()["items"]

    def wrong_input_test():
        response = client.get("/v1/politician/z/news")
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["path", "id"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }

    wrong_input_test()
    values_test()
