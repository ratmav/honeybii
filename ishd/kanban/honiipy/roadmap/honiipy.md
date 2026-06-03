# honiipy

port honeybii (ruby image-to-ascii gem) to a python cli, in place, inside the
honeybii repo. build the python package under `python/honiipy/` and consume it
from the ish shell at the repo root — inside out. keep the ruby under
`lib/honeybii/` runnable as the parity reference until honiipy matches it, then
rip out the ruby and rename the repo to honiipy.

architecture decided in conversation, captured in `docs/conventions.md`: pillow
for images, uv + hatchling + ruff, `source/honiipy` + `tests` layout, strict
output parity with cli ergonomics free to drift.

order: stand up a runnable cli skeleton, wrap it in ish, port the shading
engine, wire parity cli options, verify parity against the ruby on the test
images, then readme/banner/license, rip out ruby, rename.
