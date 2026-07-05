# strumar

**Petik gitar pakai tangan — lewat webcam.**

Tanpa install, tanpa MIDI, tanpa kabel. Cukup kamera + browser.

Dibuat oleh [**Arifian Ilham Nur Riandana**](https://github.com/arifianilhamnrr) · terinspirasi dari [soundgo](https://github.com/Gojaehyeon/soundgo)

---

## Apa ini?

**strumar** mengubah gerakan tangan kamu jadi musik nyata — **sample gitar** (nylon, akustik, elektrik) atau **synth keys** (organ, rhodes), dipetik dengan pola arpeggio atau strum ritmis.

Cocok buat:
- Eksplorasi chord & arpeggio tanpa gitar fisik
- Latihan pola petik campursari & koplo (mis. lagu Dangdut)
- Strum klasik, down-up, atau skank reggae
- Main bareng lagu favorit — chord di-fetch langsung dari **ChordTela** & **Ultimate Guitar**

---

## Fitur

| Fitur | Keterangan |
|-------|------------|
| Hand tracking | MediaPipe Hands — deteksi 2 tangan |
| Suara gitar | Tone.js Sampler — nylon, akustik, elektrik |
| Suara keys | Tone.js Synth — organ & rhodes |
| Chord wheel | Pilih root + kualitas chord (maj, m7, 7, sus4, …) |
| Arpeggio | Pola 1 (dasar) & Pola 2 (campursari 8-step) |
| Strum | Folk, klasik, ballad, campursari, koplo, dangdut, down-up, tiap ketuk |
| Clean tone | Gitar elektrik: compressor + EQ + chorus + reverb |
| Reggae | Skank (&2 &4), offbeat, bubble 16th |
| Meter & tempo | 4/4, 3/4, 6/8, 2/4 · 60–130 BPM |
| Cari lagu online | ChordTela + Ultimate Guitar, langsung ke wheel |
| Siap pakai | MediaPipe, Tone.js & sample gitar **sudah included** — clone langsung jalan |

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

Semua vendor (MediaPipe ~24 MB, Tone.js, sample gitar) **sudah ada di repo** — nggak perlu download tambahan setelah clone.

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

#### Arpeggio

| Pola | Deskripsi |
|------|-----------|
| **Pola 1** | Dasar — 4 petikan/bar (root → 3rd → 5th → 3rd) |
| **Pola 2** | Campursari — bass → 3rd → 5th → 1st → … (8-step, cocok Dangdut) |

#### Strum

Grid ketukan 8th note — **D** = downstroke, **U** = upstroke, **.** = istirahat. Pola menyesuaikan meter (3/4, 6/8, dll).

| Pola | Grid |
|------|------|
| **Folk** | D D U U D U |
| **Klasik** | D _ D U U _ D U |
| **Ballad** | D D U _ U D U |
| **Campursari** | D D U D U D D |
| **Koplo** | D . U D . U D |
| **Dangdut** | D . D U . U D U |
| **Down-Up** | D U D U D U D U |
| **Tiap Ketuk** | D D D D (per beat) |

#### Reggae

Upstroke pendek di offbeat — cocok buat skank & bubble chop.

| Pola | Deskripsi |
|------|-----------|
| **Skank** | Upstroke di &2 dan &4 |
| **Offbeat** | Upstroke di semua offbeat |
| **Bubble** | Chop 16th note |

---

## Kontrol

| Kontrol | Fungsi |
|---------|--------|
| Mode | Two-hand Chord / Melody + Chord |
| Snap | Kunci nada ke skala |
| Simple | Wheel root ABCDEFG (7 slice) vs chromatic (12) |
| Scale | Major, minor, pentatonic, blues, chromatic |
| Suara | Gitar: Nylon / Akustik / Elektrik · Keys: Organ / Rhodes |
| Range | 2–4 oktaf (mode melodi) |
| Meter | 4/4, 3/4, 6/8, 2/4 |
| Tempo | 60–130 BPM |
| Lagu | Pencarian chord online |
| Petik | Arpeggio, Strum, atau Reggae (lihat tabel di atas) |

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
│   └── fetch-vendor.sh # Opsional — update vendor (maintainer)
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