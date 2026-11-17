#!/usr/bin/env python3
"""Builds the media of the website (static/images, static/videos) from the paper and the supplementary video.

    python website/ddr/make_media.py        # builds what is missing
    python website/ddr/make_media.py --force    # rebuilds everything

Run it again after the final supplementary video: the hardware clips follow the cuts, zooms and mirrors saved by
scripts/sync_tool.py (videos/sync.json), and all faces and backgrounds are blurred as in the video.
Needs ffmpeg, pdftoppm and the pipeline of scripts/make_video.py (videos/build must exist).
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import make_video as mv  # noqa: E402

OUT = Path(__file__).resolve().parent / "static"
IMG, VID = OUT / "images", OUT / "videos"
mv.BG_BLUR = False  # the website shows the non-anonymous video: only the faces are blurred
SEG = mv.BUILD / "segments_nobg"
FORCE = False

# Figures of the paper (vector PDF) -> PNG
FIGURES = {
    "fig_keypoints": "Images/fig_keypoint_trio_err_lap_rel_ddr.pdf",
    "fig_cross": "Images/fig_cross_err_abs_ee.pdf",
    "fig_sweep": "Images/fig_sweep_wq_H12_ACCAD.pdf",
    "fig_dynamism": "Images/fig_dynamism_err_lap_all.pdf",
    "fig_delta": "Images/fig_transmission_delta_err_lap_all.pdf",
}
# Comparison shots of the video (segments)
SEGMENTS = {"cmp_kungfu": "S5", "cmp_dynamic": "S6", "cmp_failure": "S7", "cmp_degraded": "S8",
            "sim2real": "S10", "dataset": "S12"}
# Hardware clips (key of make_video.HW_CLIPS)
HARDWARE = ["squat", "kung_fu", "one_foot_balance", "pistol_squat", "balancing_stick", "walk",
            "r1_squat", "r1_crawl_1", "r1_crawl_2", "r1_kick"]


def run(cmd):
    subprocess.run([str(c) for c in cmd], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def web_video(src, dst, width=1280, crf=28, poster_t=None, trim=0.0):
    """H.264, faststart, no audio, at most `width` pixels wide. `trim` s are cut at the start and at the end
    (the shots of the video fade in and out)."""
    if dst.exists() and not FORCE:
        poster(dst, poster_t)
        return
    print(f"  {dst.name}")
    t0, length = trim, mv.probe_duration(src) - 2 * trim
    run(["ffmpeg", "-y", "-ss", t0, "-i", src, "-t", length, "-vf", f"scale='min({width},iw)':-2,fps=30", "-c:v", "libx264", "-crf", crf,
         "-preset", "slow", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart", dst])
    poster(dst, poster_t)


def poster(video, t=None):
    """Poster image: frame at `t` s, by default in the middle of the clip (the clips fade in and out)."""
    dst = video.with_suffix(".jpg")
    if dst.exists() and not FORCE:
        return
    if t is None:
        t = mv.probe_duration(video) / 2
    run(["ffmpeg", "-y", "-ss", t, "-i", video, "-frames:v", 1, "-q:v", 4, dst])


def figures():
    print("Figures")
    for name, rel in FIGURES.items():
        dst = IMG / f"{name}.png"
        if dst.exists() and not FORCE:
            continue
        print(f"  {dst.name}")
        run(["pdftoppm", "-r", 450, "-png", "-singlefile", ROOT / rel, IMG / name])
    dst = IMG / "fig_overview.png"
    if not dst.exists() or FORCE:
        src = ROOT / "Images" / "project_overview.pdf"
        run(["pdftoppm", "-r", 300, "-png", "-singlefile", src, IMG / "fig_overview"])
    dst = IMG / "fig_approaches.png"
    if not dst.exists() or FORCE:
        png = mv.fig2_png()
        if png:
            shutil.copy(png, dst)
        else:
            print("  (fig. 2 could not be compiled)")


def videos():
    print("Videos")
    VID.mkdir(parents=True, exist_ok=True)
    main = ROOT / "videos" / "supplementary_video_nobg.mp4"
    if main.exists():
        web_video(main, VID / "overview.mp4", width=1280, crf=27, poster_t=140)
    for name, seg in SEGMENTS.items():
        if (SEG / f"{seg}.mp4").exists():
            web_video(SEG / f"{seg}.mp4", VID / f"{name}.mp4", width=1280, crf=28, trim=0.4)
    for key in HARDWARE:
        path, _, _ = mv.hw(key)
        if path is None:
            print(f"  {key}: no hardware video, skipped")
            continue
        dst = VID / f"hw_{key}.mp4"
        # Clip cut, zoomed and mirrored as in the video, faces and background blurred
        dur = mv.shot(key, 8)
        clip = mv.prep_hw(f"web_hw_{key}", key, 1280, 720, dur, key)
        web_video(clip, dst, width=1280, crf=28)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="rebuild all the media")
    args = ap.parse_args()
    FORCE = args.force
    IMG.mkdir(parents=True, exist_ok=True)
    figures()
    videos()
    print("Done:", OUT)
