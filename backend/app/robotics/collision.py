"""Self-collision detection for planar robot chains: 2D segment-segment intersection tests."""
from __future__ import annotations


def segments_intersect(
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    p4: tuple[float, float],
) -> bool:
    """Return True if segment p1-p2 crosses segment p3-p4.

    Classic orientation-based test: segments AB and CD properly cross if and only if A and B are
    on opposite sides of line CD, AND C and D are on opposite sides of line AB. "Side" is given by
    the sign of a cross product (the counter-clockwise / orientation test):

        ccw(a, b, c) = (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)
    """
    # ccw calculates the counter-clockwise orientation of three points. It is calculated using the cross
    # product formula so that it returns True if the points a, b, c are arranged in a counter-clockwise order.
    # This is used to determine if two line segments intersect by checking the relative orientation of their endpoints.
    def ccw(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float]) -> bool:
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def find_self_collisions(joint_positions: list[tuple[float, float]]) -> list[tuple[int, int]]:
    """Find every pair of non-adjacent links that cross each other.

    `joint_positions` is the full chain including the base, i.e.
    [(0, 0), joint_1, joint_2, ..., end_effector] - link i connects joint_positions[i] to
    joint_positions[i + 1].

    Adjacent links (e.g. link i and link i+1) always share an endpoint by construction, so they're
    excluded from the check - that's not a collision, just two connected links meeting at a joint.
    """
    collisions = []
    n = len(joint_positions) - 1  # number of links
    for i in range(n):
        for j in range(i + 2, n):
            if segments_intersect(joint_positions[i], joint_positions[i + 1], joint_positions[j], joint_positions[j + 1]):
                collisions.append((i, j))
    return collisions
