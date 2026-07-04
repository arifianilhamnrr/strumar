# strumar

Petik gitar pakai tangan — lewat webcam. Tanpa install, tanpa MIDI.

by **ar** (Arifian)

## Try it

```bash
python3 -m http.server 8765
# buka http://localhost:8765
```

Izinkan kamera & audio saat diminta. Bekerja di Chrome/Safari/Firefox desktop. Mobile: landscape.

## Cara main

**Two-hand Chord** (default)
- Tangan kiri: pilih root chord di wheel
- Tangan kanan: pilih kualitas chord (`maj`, `m7`, `7`, dll.)
- Masuk ke tengah wheel = diam

**Melody + Chord**
- Tangan kanan: petik melodi di keyboard (X = nada, Y = volume, pinch = petik)
- Tangan kiri: strum chord di wheel (pinch = minor, buka = major)

## Stack

- [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html) — hand tracking (vendored di `vendor/`)
- [Tone.js Sampler](https://tonejs.github.io/) — sample gitar (vendored di `Tone.js`)
- Sample gitar dari [tonejs-instruments](https://github.com/nbrosowsky/tonejs-instruments) — di `samples/`
- Vanilla HTML/CSS/JS — **100% lokal, tanpa CDN, tanpa internet**

## Deploy

Siap deploy ke Vercel/Netlify/GitHub Pages — cukup serve `index.html`.

## Credit

Gesture UI terinspirasi dari [soundgo](https://github.com/Gojaehyeon/soundgo) oleh Gojaehyeon.

## License

MIT