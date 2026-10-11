from game.target import Target
from game.hit_detection import check_hit

t = Target(100, 100, radius=25)

cases = [
    # (click, expected_hit, description)
    ((100, 100), True,  "dead center"),
    # four sides: exactly on the boundary, then one pixel outside
    ((125, 100), True,  "right edge, exactly on boundary"),
    ((126, 100), False, "right edge, 1px outside"),
    ((75, 100),  True,  "left edge, exactly on boundary"),
    ((74, 100),  False, "left edge, 1px outside"),
    ((100, 125), True,  "bottom edge, exactly on boundary"),
    ((100, 126), False, "bottom edge, 1px outside"),
    ((100, 75),  True,  "top edge, exactly on boundary"),
    ((100, 74),  False, "top edge, 1px outside"),
    # just inside
    ((124, 100), True,  "right, 1px inside"),
    ((100, 76),  True,  "top, 1px inside"),
    # diagonal boundary (15-20-25 triangle)
    ((115, 120), True,  "diagonal, exactly on boundary"),
    ((116, 120), False, "diagonal, just outside"),
    ((115, 121), False, "diagonal, just outside"),
    # cases the old buggy rect got wrong
    ((85, 85),   True,  "upper-left of center (old bug: miss)"),
    ((140, 140), False, "lower-right empty space (old bug: hit)"),
    # square-corner of the bounding box is NOT part of the circle
    ((124, 124), False, "corner of bounding square, outside circle"),
]

failed = 0
for pos, expected, desc in cases:
    got = check_hit([t], pos) is t
    status = "ok  " if got == expected else "FAIL"
    if got != expected:
        failed += 1
    print(f"{status} {pos} expected {expected}: {desc}")

assert check_hit([], (100, 100)) is None
a, b = Target(100, 100, 25), Target(300, 300, 25)
assert check_hit([a, b], (300, 300)) is b
assert check_hit([a, b], (200, 200)) is None

print("\nAll passed" if not failed else f"\n{failed} FAILED")