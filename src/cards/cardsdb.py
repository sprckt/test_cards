# -*- coding: utf-8 -*-

"""
cardsdb :  The API
"""

import tinydb
from typing import List

from dataclasses import dataclass, field, asdict


@dataclass
class Card:
    summary: str = None
    owner: str = None
    done: bool = None
    id: int = field(default=None, compare=False)

    @classmethod
    def from_dict(cls, d):
        return Card(**d)

    def to_dict(self):
        return asdict(self)

# --- actions on db


class CardsDB:

    def __init__(self, db_path):
        self._db = tinydb.TinyDB(db_path)

    def add(self, card: Card) -> int:
        """Add a card to the db."""
        card.id = self._db.insert(card.to_dict())
        self._db.update(card.to_dict(), doc_ids=[card.id])
        return card.id

    def get(self, card_id: int) -> Card:
        """Return a card with a matching id."""
        return Card.from_dict(self._db.get(doc_id=card_id))

    def list_cards(self, noowner=None, owner=None, done=None) -> List[Card]:
        """Return a list of all cards."""
        q = tinydb.Query()
        if noowner and owner:
            results = self._db.search(
                (q.owner == owner) |
                (q.owner == None) |  # noqa : is None doesn't work for TinyDb
                (q.owner == ''))
        elif noowner or owner == '':
            results = self._db.search((q.owner == None) |  # noqa
                                      (q.owner == ''))
        elif owner:
            results = self._db.search(q.owner == owner)
        else:
            results = self._db

        if done is None:
            # return all cards
            return [Card.from_dict(t) for t in results]
        elif done:
            # only done cards
            return [Card.from_dict(t) for t in results if t['done']]
        else:
            # only not done cards
            return [Card.from_dict(t) for t in results if not t['done']]

    def count(self, noowner=None, owner=None, done=None) -> int:
        """Return the number of cards in db."""
        return len(self.list_cards(noowner, owner, done))

    def update(self, card_id: int, card_mods: Card) -> None:
        """Update a card with modifications."""
        d = card_mods.to_dict()
        changes = {k: v for k, v in d.items() if v is not None}
        self._db.update(changes, doc_ids=[card_id])

    def delete(self, card_id: int) -> None:
        """Remove a card from db with given card_id."""
        self._db.remove(doc_ids=[card_id])

    def delete_all(self) -> None:
        """Remove all tasks from db."""
        self._db.purge()
