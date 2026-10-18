import os
import shutil
import subprocess
from pathlib import Path
import imageio_ffmpeg
import soundfile as sf

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

scenes = [
    {"num": 1, "slide": "scripts/long_video_slides/scene_01.png", "audio": "scripts/long_audio_scenes/scene_01_problem.wav"},
    {"num": 2, "slide": "scripts/long_video_slides/scene_02.png", "audio": "scripts/long_audio_scenes/scene_02_track_justification.wav"},
    {"num": 3, "slide": "scripts/long_video_slides/scene_03.png", "audio": "scripts/long_audio_scenes/scene_03_arc_agi.wav"},
    {"num": 4, "slide": "scripts/long_video_slides/scene_04.png", "audio": "scripts/long_audio_scenes/scene_04_gemini_utilization.wav"},
    {"num": 5, "slide": "scripts/long_video_slides/scene_05.png", "audio": "scripts/long_audio_scenes/scene_05_formal_safety.wav"},
    {"num": 6, "slide": "scripts/long_video_slides/scene_06.png", "audio": "scripts/long_audio_scenes/scene_06_gcp_architecture.wav"},
    {"num": 7, "slide": "scripts/long_video_slides/scene_07.png", "audio": "scripts/long_audio_scenes/scene_07_live_demonstration.wav"}
]

temp_dir = Path("scripts/long_video_temp")
temp_dir.mkdir(parents=True, exist_ok=True)

scene_clips = []

print("Rendering 7 individual scene video clips...")

for sc in scenes:
    audio_info = sf.info(sc["audio"])
    duration = audio_info.duration
    padded_duration = duration + 0.6
    
    clip_output = temp_dir / f"clip_0{sc['num']}.mp4"
    scene_clips.append(clip_output)
    
    print(f"Rendering Scene {sc['num']} (duration: {padded_duration:.2f}s)...")
    
    vf = (
        f"scale=1920:1080,"
        f"zoompan=z='min(zoom+0.00018,1.03)':d={int(padded_duration * 30)}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30,"
        f"format=yuv420p"
    )
    
    af = f"adelay=250|250,apad=whole_dur={padded_duration}"
    
    cmd = [
        ffmpeg_exe, "-y",
        "-loop", "1", "-i", sc["slide"],
        "-i", sc["audio"],
        "-vf", vf,
        "-af", af,
        "-t", f"{padded_duration:.2f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        str(clip_output)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"Scene {sc['num']} rendered: {clip_output.name}")

# Create concat manifest
concat_list = temp_dir / "concat_list.txt"
with open(concat_list, "w") as f:
    for clip in scene_clips:
        f.write(f"file '{clip.resolve().as_posix()}'\n")

merged_no_music = temp_dir / "merged_no_music.mp4"
print("Concatenating all 7 scenes...")
concat_cmd = [
    ffmpeg_exe, "-y",
    "-f", "concat", "-safe", "0",
    "-i", str(concat_list.resolve()),
    "-c", "copy",
    str(merged_no_music)
]
subprocess.run(concat_cmd, check=True, capture_output=True)

# Final step: Mix with 11-minute ambient background music bed
final_output_docs = Path("docs/assets/schemaforge_showcase_video.mp4")
final_output_root = Path("schemaforge_showcase_video.mp4")
final_output_artifacts = Path(r"C:\Users\shiva\.gemini\antigravity-ide\brain\907aef50-850c-418e-af6a-1aa942012776\schemaforge_showcase_video.mp4")
final_output_docs.parent.mkdir(parents=True, exist_ok=True)

print("Mixing narration with ambient background music bed...")
mix_filter = (
    "[1:a]volume=0.20,afade=t=in:st=0:d=3,afade=t=out:st=590:d=8[bg];"
    "[0:a][bg]amix=inputs=2:duration=first:dropout_transition=3[aout]"
)

mix_cmd = [
    ffmpeg_exe, "-y",
    "-i", str(merged_no_music),
    "-i", "scripts/long_ambient_bed.wav",
    "-filter_complex", mix_filter,
    "-map", "0:v",
    "-map", "[aout]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "256k",
    "-shortest",
    str(final_output_docs)
]
subprocess.run(mix_cmd, check=True, capture_output=True)

# Copy to root and artifacts
shutil.copy2(str(final_output_docs), str(final_output_root))
if final_output_artifacts.parent.exists():
    shutil.copy2(str(final_output_docs), str(final_output_artifacts))

print("SUCCESS: 7-Scene Extended Demonstration Video Generated Successfully!")
print(f"File 1: {final_output_docs.resolve()}")
print(f"File 2: {final_output_root.resolve()}")
print(f"File 3: {final_output_artifacts.resolve()}")

# Probe output video
probe_cmd = [ffmpeg_exe, "-i", str(final_output_docs)]
res = subprocess.run(probe_cmd, capture_output=True, text=True)
for l in res.stderr.splitlines():
    if "Duration:" in l or "Stream #" in l:
        print("  " + l.strip())
