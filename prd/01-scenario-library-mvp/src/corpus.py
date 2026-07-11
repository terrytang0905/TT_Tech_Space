"""Controlled corpus representations derived from the same scene facts."""

from dataclasses import dataclass
from typing import Iterable, Sequence, Tuple

from .schemas import Scene


@dataclass(frozen=True)
class CorpusItem:
    scene_id: str
    text: str


def atomic_facts(scene: Scene) -> Tuple[str, ...]:
    """Return the fact values shared by both experiment representations."""
    return (
        scene.environment.weather,
        scene.environment.lighting,
        scene.environment.road_type,
        scene.environment.surface,
        *scene.actors,
        scene.trigger,
        scene.system_behavior,
        scene.expected_behavior,
        scene.risk,
        *scene.evidence,
    )


def render_raw_chunk(scene: Scene) -> str:
    """Render facts as an unlabeled document chunk."""
    return "。".join(atomic_facts(scene)) + "。"


def render_scene_unit(scene: Scene) -> str:
    """Render the identical facts with a fixed scene-field structure."""
    environment = "、".join((
        scene.environment.weather,
        scene.environment.lighting,
        scene.environment.road_type,
        scene.environment.surface,
    ))
    return "\n".join((
        f"环境：{environment}",
        f"参与者：{'、'.join(scene.actors)}",
        f"触发事件：{scene.trigger}",
        f"系统响应：{scene.system_behavior}",
        f"期望行为：{scene.expected_behavior}",
        f"风险：{scene.risk}",
        f"证据：{'；'.join(scene.evidence)}",
    ))


def build_corpus(scenes: Iterable[Scene], representation: str) -> Tuple[CorpusItem, ...]:
    renderers = {"raw": render_raw_chunk, "structured": render_scene_unit}
    if representation not in renderers:
        raise ValueError("representation must be raw or structured")
    renderer = renderers[representation]
    return tuple(CorpusItem(scene.scene_id, renderer(scene)) for scene in scenes)
