import pytest
from core.pagination import BasePagination
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


class DummyPagination(BasePagination):
    page_size = 10


@pytest.fixture
def request_factory():
    return APIRequestFactory()


@pytest.fixture
def items():
    return list(range(100))


def build_request(request_factory, path, params=None):
    django_request = request_factory.get(path, params or {})
    return Request(django_request)


def paginate(request, data, pagination_class=DummyPagination):
    paginator = pagination_class()
    page = paginator.paginate_queryset(data, request)
    response = paginator.get_paginated_response(page)
    return response


class TestBasePagination:
    def test_get_paginated_response_returns_expected_structure(self, request_factory, items):
        request = build_request(request_factory, "/authors/")

        response = paginate(request, items[:15])

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) == {
            "count",
            "pages",
            "current_page",
            "page_size",
            "next",
            "previous",
            "results",
        }
        assert response.data["count"] == 15
        assert response.data["pages"] == 2
        assert response.data["current_page"] == 1
        assert response.data["page_size"] == 10
        assert response.data["previous"] is None
        assert len(response.data["results"]) == 10

    def test_previous_is_none_on_first_page(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page": 1})

        response = paginate(request, items[:15])

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert response.data["previous"] is None

    def test_next_link_exists_on_first_page(self, request_factory, items):
        request = build_request(request_factory, "/authors/")

        response = paginate(request, items[:15])

        next_link = response.data["next"]

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert next_link is not None
        assert next_link == "http://testserver/authors/?page=2"

    def test_next_link_keeps_page_size_query_param(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page_size": 5})

        response = paginate(request, items[:15])

        next_link = response.data["next"]

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 1
        assert next_link is not None
        assert "page=2" in next_link
        assert "page_size=5" in next_link

    def test_next_link_is_none_on_last_page(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page": 2})

        response = paginate(request, items[:15])

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["next"] is None

    def test_previous_link_for_second_page_points_to_page_1(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page": 2})

        response = paginate(request, items[:15])

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 2
        assert response.data["previous"] == "http://testserver/authors/?page=1"
        assert response.data["next"] is None
        assert len(response.data["results"]) == 5

    def test_previous_link_for_later_pages_keeps_page_size_query_param(self, request_factory, items):
        request = build_request(
            request_factory,
            "/authors/",
            {"page": 3, "page_size": 10},
        )

        response = paginate(request, items[:25])

        previous_link = response.data["previous"]

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 3
        assert previous_link is not None
        assert "page=2" in previous_link
        assert "page_size=10" in previous_link
        assert response.data["next"] is None
        assert len(response.data["results"]) == 5

    def test_previous_link_keeps_other_query_params(self, request_factory, items):
        request = build_request(
            request_factory,
            "/authors/",
            {
                "page": 3,
                "page_size": 10,
                "search": "rowling",
                "ordering": "-id",
            },
        )

        response = paginate(request, items[:25])

        previous_link = response.data["previous"]

        assert response.status_code == status.HTTP_200_OK
        assert response.data["current_page"] == 3
        assert previous_link is not None
        assert "page=2" in previous_link
        assert "page_size=10" in previous_link
        assert "search=rowling" in previous_link
        assert "ordering=-id" in previous_link
        assert response.data["next"] is None
        assert len(response.data["results"]) == 5

    def test_page_size_query_param_overrides_default(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page_size": 5})

        response = paginate(request, items[:15])

        assert response.status_code == status.HTTP_200_OK
        assert response.data["page_size"] == 5
        assert response.data["pages"] == 3
        assert len(response.data["results"]) == 5

    def test_page_size_does_not_exceed_max_page_size(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page_size": 100})

        response = paginate(request, items[:60])

        assert response.status_code == status.HTTP_200_OK
        assert response.data["page_size"] == 50
        assert response.data["pages"] == 2
        assert len(response.data["results"]) == 50

    def test_invalid_page_size_fallback_to_default(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page_size": "abc"})

        response = paginate(request, items[:15])

        assert response.status_code == status.HTTP_200_OK
        assert response.data["page_size"] == 10
        assert len(response.data["results"]) == 10

    def test_out_of_range_page_returns_404(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page": 99})
        paginator = DummyPagination()

        with pytest.raises(NotFound):
            paginator.paginate_queryset(items[:10], request)

    def test_invalid_page_number_returns_404(self, request_factory, items):
        request = build_request(request_factory, "/authors/", {"page": "invalid_page"})
        paginator = DummyPagination()

        with pytest.raises(NotFound):
            paginator.paginate_queryset(items[:10], request)
