#!/usr/bin/env python3
"""Estimate BPM from Renara fingerpicking tutorial (youtu.be/oG_ihm7xvBU).

Pattern 6-3-2-3 / 5-3-2-3: four picks per bar in 4/4, one pick per beat.
BPM = 60 / median_inter_pick_interval_seconds.
"""
import json
import wave
from collections import Counter
from pathlib import Path

import numpy as np

WAV = Path(__file__).parent / (
    "petikan-dasar-POLA PETIKAN GITAR PALING GAMPANG UNTUK PEMULA (Tutorial Gitar).wav"
)

# Timestamps from petikan-dasar.id.vtt
SEGMENTS = [
    ("demo_pemula", 41.5, 54.0, 70),
    ("elvis_lambat", 74.0, 95.0, 65),
    ("viral_cepat", 112.0, 130.0, 95),
]


def load_segment(path, start, end, sr=22050):
    with wave.open(str(path), "rb") as wf:
        file_sr = wf.getframerate()
        ch = wf.getnchannels()
        raw = wf.readframes(wf.getnframes())
    data = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    if ch == 2:
        data = data.reshape(-1, 2).mean(axis=1)
    data = data[int(start * file_sr) : int(end * file_sr)]
    if file_sr != sr:
        x_old = np.linspace(0, len(data), num=len(data), endpoint=False)
        x_new = np.linspace(0, len(data), num=int(len(data) * sr / file_sr), endpoint=False)
        data = np.interp(x_new, x_old, data)
    return data / 32768.0, sr


def pick_times(y, sr, min_gap_s=0.55, pct=85):
    hop = int(sr * 0.03)
    env = np.array([np.sqrt(np.mean(y[i * hop : (i + 1) * hop] ** 2)) for i in range(1 + (len(y) - hop) // hop)])
    env = np.convolve(env, np.ones(5) / 5, mode="same")
    diff = np.maximum(0, np.diff(env, prepend=env[0]))
    thresh = np.percentile(diff, pct)
    min_gap = int(min_gap_s * sr / hop)
    peaks, last = [], -min_gap
    for i, v in enumerate(diff):
        if v < thresh:
            continue
        if i - last < min_gap:
            continue
        peaks.append(i * hop / sr)
        last = i
    return np.array(peaks)


def estimate_bpm(times):
    ibis = np.diff(times)
    ibis = ibis[(ibis > 0.35) & (ibis < 2.0)]
    if len(ibis) < 4:
        return None
    med = float(np.median(ibis))
    mode = Counter(np.round(ibis, 1)).most_common(1)[0][0]
    return {
        "median_ibi_ms": round(med * 1000, 1),
        "mode_ibi_ms": round(float(mode) * 1000, 1),
        "bpm_median": round(60 / med),
        "bpm_mode": round(60 / float(mode)),
        "onsets": len(times),
    }


def main():
    out = []
    for name, start, end, app_bpm in SEGMENTS:
        y, sr = load_segment(WAV, start, end)
        times = pick_times(y, sr)
        est = estimate_bpm(times) or {}
        out.append({
            "segment": name,
            "start": start,
            "end": end,
            "app_bpm": app_bpm,
            **est,
        })
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()