# strumar

**Petik gitar pakai tangan — lewat webcam.**

Tanpa install, tanpa MIDI, tanpa kabel. Cukup kamera + browser.

Dibuat oleh [**Arifian Ilham Nur Riandana**](https://github.com/arifianilhamnrr) · terinspirasi dari [soundgo](https://github.com/Gojaehyeon/soundgo)

---

## Apa ini?

**strumar** mengubah gerakan tangan kamu jadi petikan gitar nyata — bukan synth, tapi **sample gitar** (nylon, akustik, elektrik) yang dipetik dengan pola ritmis.

Cocok buat:
- Eksplorasi chord & arpeggio tanpa gitar fisik
- Latihan pola petik campursari (mis. lagu Dangdut/Koplo)
- Main bareng lagu favorit — chord di-fetch langsung dari **ChordTela** & **Ultimate Guitar**

---

## Fitur

| Fitur | Keterangan |
|-------|------------|
| Hand tracking | MediaPipe Hands — deteksi 2 tangan |
| Sample gitar | Tone.js Sampler — nylon, akustik, elektrik |
| Chord wheel | Pilih root + kualitas chord (maj, m7, 7, sus4, …) |
| Pola petik | Pola 1 (dasar) & Pola 2 (campursari 8-step) |
| Meter & tempo | 4/4, 3/4, 6/8, 2/4 · 60–130 BPM |
| Cari lagu online | ChordTela + Ultimate Guitar, langsung ke wheel |
| 100% lokal | Semua asset di repo — MediaPipe, Tone.js, sample MP3 |

---

## Quick start

### 1. Clone & jalankan

```bash
git clone https://github.com/arifianilhamnrr/strumar.git
cd strumar
python3 scripts/dev-server.py
```

Buka **http://127.0.0.1:8765** · izinkan **kamera** & **audio**.

> Pakai `dev-server.py`, bukan `http.server` biasa — diperlukan buat **API pencarian lagu** (`/api/search`, `/api/chords`).

### 2. Vendor belum lengkap?

Kalau wheel tangan tidak muncul atau preflight error:

```bash
./scripts/fetch-vendor.sh
```

Lalu refresh halaman.

---

## Cara main

### Mode Two-hand Chord *(default)*

```
Tangan kiri  → wheel CHORD/ROOT  (pilih chord)
Tangan kanan → wheel QUALITY     (maj, m, 7, m7, …)
```

- Arahkan jari ke **slice** wheel yang diinginkan
- Chord dipetik otomatis dengan pola ritmis
- Masuk ke **tengah wheel** = off (dengan grace period biar nggak putus-putus)

### Mode Melody + Chord

```
Tangan kanan → keyboard (X = nada, Y = volume, pinch = petik)
Tangan kiri  → chord wheel (pinch = minor, buka = major)
```

### Cari lagu

1. Ketik judul di field **Lagu** (mis. `Sugeng Dalu`)
2. Pilih dari dropdown — sumber **ChordTela** atau **UG**
3. Wheel otomatis berisi chord lagu · meter, tempo & pola petik disesuaikan

### Pola petik

| Pola | Deskripsi |
|------|-----------|
| **Pola 1** | Dasar — 4 petikan/bar (root → 3rd → 5th → 3rd) |
| **Pola 2** | Campursari — bass → 3rd → 5th → 1st → … (8-step, cocok Dangdut) |

---

## Kontrol

| Kontrol | Fungsi |
|---------|--------|
| Mode | Two-hand Chord / Melody + Chord |
| Snap | Kunci nada ke skala |
| Simple | Wheel root ABCDEFG (7 slice) vs chromatic (12) |
| Scale | Major, minor, pentatonic, blues, chromatic |
| Guitar | Nylon / Acoustic / Electric |
| Range | 2–4 oktaf (mode melodi) |
| Meter | 4/4, 3/4, 6/8, 2/4 |
| Tempo | 60–130 BPM |
| Lagu | Pencarian chord online |
| Petik | Pola 1 / Pola 2 |

---

## Struktur project

```
strumar/
├── index.html          # App utama
├── Tone.js             # Audio engine (vendored)
├── songs.json          # Lagu lokal / preset
├── api/                # Proxy chord online (Vercel + dev-server)
│   ├── chord_lib.py
│   ├── search.py
│   └── chords.py
├── scripts/
│   ├── dev-server.py   # Server lokal + API
│   └── fetch-vendor.sh
├── samples/            # Sample gitar MP3
└── vendor/mediapipe/   # Hand tracking (offline)
```

---

## Deploy

### Vercel *(disarankan)*

1. Import repo ke [Vercel](https://vercel.com)
2. Deploy — `vercel.json` sudah disiapkan
3. API `/api/search` & `/api/chords` jalan otomatis di serverless Python

### Static hosting lain

GitHub Pages / Netlify bisa serve file statis, tapi **pencarian lagu online tidak akan jalan** tanpa backend proxy.

---

## Persyaratan

- Browser modern (Chrome, Firefox, Safari, Edge)
- Webcam + HTTPS atau `localhost`
- Desktop disarankan · mobile: **landscape**
- Pencarian lagu butuh koneksi internet

---

## Credit

- Gesture UI terinspirasi [soundgo](https://github.com/Gojaehyeon/soundgo) oleh Gojaehyeon
- Sample gitar dari [tonejs-instruments](https://github.com/nbrosowsky/tonejs-instruments)
- Hand tracking [MediaPipe Hands](https://google.github.io/mediapipe/solutions/hands.html)
- Audio [Tone.js](https://tonejs.github.io/)

## License

MIT