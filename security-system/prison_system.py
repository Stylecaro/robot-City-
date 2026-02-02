"""
Sistema de Cárcel y Rehabilitación
Encierra avatares por tiempo definido, reduce condena con trabajo voluntario
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
import uuid


class InmateStatus(Enum):
    INCARCERATED = "incarcerated"
    PAROLE = "parole"
    RELEASED = "released"


@dataclass
class Sentence:
    sentence_id: str
    player_id: str
    reason: str
    start_time: datetime
    duration_minutes: int
    remaining_minutes: int
    status: InmateStatus
    good_behavior_points: int = 0
    voluntary_work_minutes: int = 0
    released_at: Optional[datetime] = None

    def to_dict(self) -> Dict:
        return {
            "sentence_id": self.sentence_id,
            "player_id": self.player_id,
            "reason": self.reason,
            "start_time": self.start_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "remaining_minutes": self.remaining_minutes,
            "status": self.status.value,
            "good_behavior_points": self.good_behavior_points,
            "voluntary_work_minutes": self.voluntary_work_minutes,
            "released_at": self.released_at.isoformat() if self.released_at else None
        }


class PrisonManager:
    """Gestor de cárcel y rehabilitación"""

    def __init__(self):
        self.sentences: Dict[str, Sentence] = {}
        self.active_inmates: Dict[str, str] = {}  # player_id -> sentence_id
        self.history: List[str] = []

    def sentence_player(self, player_id: str, reason: str, duration_minutes: int) -> Sentence:
        sentence_id = str(uuid.uuid4())
        sentence = Sentence(
            sentence_id=sentence_id,
            player_id=player_id,
            reason=reason,
            start_time=datetime.now(),
            duration_minutes=duration_minutes,
            remaining_minutes=duration_minutes,
            status=InmateStatus.INCARCERATED
        )
        self.sentences[sentence_id] = sentence
        self.active_inmates[player_id] = sentence_id
        return sentence

    def get_sentence(self, sentence_id: str) -> Optional[Sentence]:
        return self.sentences.get(sentence_id)

    def get_inmate_sentence(self, player_id: str) -> Optional[Sentence]:
        sentence_id = self.active_inmates.get(player_id)
        if not sentence_id:
            return None
        return self.sentences.get(sentence_id)

    def add_good_behavior(self, player_id: str, points: int = 1) -> Optional[Sentence]:
        sentence = self.get_inmate_sentence(player_id)
        if not sentence:
            return None
        sentence.good_behavior_points += max(0, points)
        self._apply_reduction(sentence)
        return sentence

    def add_voluntary_work(self, player_id: str, minutes: int) -> Optional[Sentence]:
        sentence = self.get_inmate_sentence(player_id)
        if not sentence:
            return None
        sentence.voluntary_work_minutes += max(0, minutes)
        self._apply_reduction(sentence)
        return sentence

    def _apply_reduction(self, sentence: Sentence) -> None:
        """Reduce condena según conducta y trabajo voluntario"""
        reduction = (sentence.good_behavior_points * 2) + (sentence.voluntary_work_minutes // 10)
        sentence.remaining_minutes = max(0, sentence.duration_minutes - reduction)
        if sentence.remaining_minutes == 0:
            self.release_player(sentence.player_id)

    def tick_sentence(self, player_id: str, minutes: int = 1) -> Optional[Sentence]:
        sentence = self.get_inmate_sentence(player_id)
        if not sentence:
            return None
        sentence.remaining_minutes = max(0, sentence.remaining_minutes - max(1, minutes))
        if sentence.remaining_minutes == 0:
            self.release_player(player_id)
        return sentence

    def release_player(self, player_id: str) -> Optional[Sentence]:
        sentence = self.get_inmate_sentence(player_id)
        if not sentence:
            return None
        sentence.status = InmateStatus.RELEASED
        sentence.released_at = datetime.now()
        self.history.append(sentence.sentence_id)
        if player_id in self.active_inmates:
            del self.active_inmates[player_id]
        return sentence

    def get_active_inmates(self) -> List[Dict]:
        return [self.sentences[sid].to_dict() for sid in self.active_inmates.values()]


prison_manager = PrisonManager()
