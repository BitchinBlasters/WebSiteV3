# /image-assets/ — site-wide hero & banner images

One shared `assets.txt` file, one heading per named location on the site,
plus every image file it refers to.

## Template — assets.txt

```
## Homepage Hero
Image: hero-home.jpg

#Desktop
Scale: 100%
Alignment: top-left
Opacity: 100
Nudge: 0px 0px

#Mobile
Scale: 80%
Alignment: top
Opacity: 100
Nudge: 0px -20px

## Your Build Hero
Image: hero-your-build.jpg

#Desktop
Scale: 120%
Alignment: center
Opacity: 85
Nudge: 0px -8px
```

- `Image` — filename in this same folder. Sits once under the `##`
  heading, shared by both devices.
- `#Desktop` / `#Mobile` — each carries its own Scale/Alignment/Opacity/
  Nudge, so you can crop or reposition the same image differently per
  device. "Mobile" is any screen 900px wide or under — the same
  breakpoint the nav switches on, so it stays consistent with the rest
  of the site.
  - Leave `#Mobile` out entirely and mobile just uses the desktop
    values — no need to duplicate the block if you don't want a
    different crop on phones.
  - Include `#Mobile` but only set some of its fields, and the rest
    fall back to the matching desktop value — you only need to write
    down what's actually different.
- `Alignment` — the anchor point that stays put, no matter how much you
  scale up or down — only the edges away from it move. Nine options:
  `center`, `top`, `bottom`, `left`, `right`, `top-left`, `top-right`,
  `bottom-left`, `bottom-right`.
- `Scale` — a plain percentage. `100%` (or leave it blank) always fills
  the space completely with no empty gaps — this is the default and
  normal choice. Above 100% zooms in further, pivoting on the anchor
  (crops more, e.g. `130%`). Below 100% zooms out from the anchor and
  will show empty space around the image — only do this on purpose,
  since it's the one setting that can leave gaps.
- `Opacity` — 0–100.
- `Nudge` — fine pixel offset (x y) on top of `Alignment`. It's the one
  thing that can move the anchor's exact position — `0px 0px` = no
  nudge. Stays a fixed pixel amount no matter what `Scale` is set to.

## Available location names

These headings must match exactly (case-sensitive) for the build script
to find them:

- `Homepage Hero`
- `Who We Are Hero`
- `Your Build Hero`
- `3D Printing Hero`
- `Store Hero`
- `Build Gallery Hero`
- `Brands Hero`

Terms & Conditions has no hero image. If you add a heading name that
doesn't match any of the above, it's just ignored. Any location left out
of `assets.txt` entirely falls back to the site's existing default image
for that spot, centered, at 100% scale.
