from datetime import date

import pytest
from django.db import IntegrityError, transaction


@pytest.mark.django_db
class TestAwardModel:

    def test_award_title_must_be_unique(self, award_factory):
        award_factory(title="Nobel Prize")

        with pytest.raises(IntegrityError):
            with transaction.atomic():
                award_factory(title="Nobel Prize")

    def test_award_str_returns_title(self, award_factory):
        award = award_factory(title="Nobel Prize in Literature")

        assert str(award) == "Nobel Prize in Literature"

    def test_award_can_be_created_without_authors(self, award_factory):
        award = award_factory(title="Pulitzer Prize")

        assert award.authors.count() == 0

    def test_award_can_be_assigned_to_one_author(self, award_factory, author_factory):
        author = author_factory(name="J. K. Rowling")
        award = award_factory(title="British Book Awards")

        award.authors.add(author)

        assert award.authors.count() == 1
        assert author in award.authors.all()

    def test_award_can_be_assigned_to_multiple_authors(self, award_factory, author_factory):
        author_1 = author_factory(name="Author One")
        author_2 = author_factory(name="Author Two")
        award = award_factory(title="Shared Literary Award")

        award.authors.add(author_1, author_2)

        assert list(award.authors.all()) == [author_1, author_2]

    def test_author_related_name_returns_awards(self, award_factory, author_factory):
        author = author_factory(name="J. K. Rowling")

        award_1 = award_factory(title="Award One")
        award_2 = award_factory(title="Award Two")

        award_1.authors.add(author)
        award_2.authors.add(author)

        assert list(author.awards.all()) == [award_1, award_2]

    def test_award_year_received_can_be_set(self, award_factory):
        received_date = date(2024, 10, 15)

        award = award_factory(
            title="National Book Award",
            year_received=received_date,
        )

        assert award.year_received == date(2024, 10, 15)

    def test_award_year_received_is_optional(self, award_factory):
        award = award_factory(title="Optional Date Award")

        assert award.year_received is None
