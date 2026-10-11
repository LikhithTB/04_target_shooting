"""
hit_detection: figures out whether a click landed on a target.
"""


def check_hit(targets, click_pos):
    """
    Returns the target that was clicked, or None if the click missed
    every target.

    A target is a circle centered at (target.x, target.y), so a click
    hits it when the click's distance from the center is <= radius.
    Squared distances are compared to avoid a square root.
    """
    click_x, click_y = click_pos
    for target in targets:
        dx = click_x - target.x
        dy = click_y - target.y
        if dx * dx + dy * dy <= target.radius * target.radius:
            return target
    return None