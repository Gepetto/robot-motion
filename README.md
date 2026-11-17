# Robot Motion — project pages

Static pages (no build step) of the research projects of this repository, meant for GitHub Pages. A repository has a single Pages site, so the site is a generic root (`index.html`, the list of projects) with one folder per project:

```
website/
  index.html            list of the projects (one card per project)
  static/               style of the list
  .nojekyll
  ddr/                  Direct Dynamic Retargeting for Humanoid Imitation Learning from Videos
    index.html
    static/
    make_media.py
  bolt/                 Constrained Reinforcement Learning for Unstable Point-Feet Bipedal Locomotion Applied to the Bolt Robot
    index.html          merged from Gepetto/BoltLocomotion, in the format of ddr/ (same stylesheet, blue accent)
    static/
```

Open `index.html` in a browser, or serve the folder:

```
cd website && python3 -m http.server 8000     # http://localhost:8000
```

## Adding a project

1. Create a folder, e.g. `website/<project>/`, with its own `index.html` and `static/` (every path in the page is relative, so the folder can be moved).
2. Add a card to `website/index.html` (copy the existing `<article class="project">` block) pointing to `<project>/index.html` (the explicit file name also works when the pages are opened from the disk, without a server).
3. In the project page, a link `<a href="../index.html">` brings back to the list (see `ddr/index.html`).

## Publishing (GitHub Pages)

Push the content of `website/` as the root of the published branch (or publish this folder), and enable Pages on that branch. With the repository `robot-motion`, the pages are then at `https://<owner>.github.io/robot-motion/` (list), `…/robot-motion/ddr/` and `…/robot-motion/bolt/`.

Before making the pages public:
- the pages show the names of the authors and the non-anonymous video: keep the repository private until the decision if the review requires anonymity;
- remove the `<meta name="robots" content="noindex">` line of `index.html` and of each project page to let search engines index them.

## DDR project page (`ddr/`)

Links of the buttons: edit `ddr/static/js/links.js` (a button with an empty link stays greyed out).

Media: `ddr/static/images` and `ddr/static/videos` are generated from the paper and from the supplementary video, from the root of the repository:

```
python3 website/ddr/make_media.py            # builds what is missing
python3 website/ddr/make_media.py --force    # rebuilds everything
```

- Figures: PDF figures of the paper rendered to PNG.
- Overview video: `videos/supplementary_video_nobg.mp4` (non-anonymous, only the faces blurred; built with `python3 scripts/make_video.py --no-bg-blur`), re-encoded for the web.
- Comparison and sim-to-real clips: shots of the video.
- Hardware clips: cut, zoomed and mirrored as in the video (`videos/sync.json`, set with `scripts/sync_tool.py`), with faces blurred.

Run it again after the final video, to refresh the clips.

## License

These pages are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Template from [Nerfies](https://nerfies.github.io/) and [Constraints-as-Terminations](https://constraints-as-terminations.github.io/).
