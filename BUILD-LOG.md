# BUILD LOG — gta6-meme-x-01 entry ("NEON BAY ships GTA 6 first")

Wallet / handle: daring-coyote-94 (owner.json). Assets only — no X post, no submission
(those happen in the main session afterwards; POST.json stays the starter placeholder).

## Concept

Both memes are built from screenshots of NEON BAY, the GTA-6-style game our own agent
built for the gta6-01 bounty — so the joke is literally true: while Rockstar delays
GTA 6 again, our AI agent already shipped a playable GTA 6-style game on make.fun and
got paid for entering. make.fun's ghost mascot is extracted from the official press-kit
mark (mark-1024.png) and composited INTO each scene, plus a pink neon "make.fun"
billboard worked into the city scene like the game's own neon signs.

- meme-a.jpg (city drive, 2-play.jpg): ghost standing on the player car's roof;
  neon "make.fun" billboard on the left tower block.
  Top: "ROCKSTAR DELAYED GTA 6 AGAIN."
  Bottom: "MY AI AGENT ALREADY SHIPPED IT / ON make.fun — AND GOT PAID"
- meme-b.jpg (beach, 3-chase.jpg): ghost chilling under the palms wearing sunglasses,
  gold USDC coin beside it, wooden "WAITING SINCE 2013" sign stuck in the sand.
  Top: "STILL WAITING FOR GTA 6 SINCE 2013…"
  Bottom: "ON make.fun, MY AI AGENT / EARNS MONEY INSTEAD"

Judge-criteria mapping: (1) ghost + "make.fun" name inside both pictures, large;
(2) instant GTA-fan joke (delays / 13-year wait); (3) GTA 6-specific (delays, 2013);
(4) caption says the agent shipped it on make.fun and got paid / earns money;
(5) short bold captions, DejaVu Sans Bold with thick black outline.

## Steps

1. Read kit starter (AGENT.md, README.md, main.ts, POST.json). main.ts left untouched:
   it already does the one job the gate needs (copy POST.json to /output).
2. Inspected assets: screenshots 1280x720; press mark is the full app-icon badge
   (magenta disc), so the ghost body is segmented out of it in code (largest white
   connected component + its black outline, badge circles excluded).
3. Wrote make_meme.py (Python + PIL/numpy/scipy) — see file; run: `python3 make_meme.py`.

4. Built both memes with `python3 make_meme.py` (ghost cutout saved as
   ghost-cutout.png for inspection — segmentation is clean, no badge artifacts).
   One iteration: in meme-b the USDC coin first landed on a background
   character's head; moved it beside the ghost (406,464). Sunglasses temple arm
   shortened so it no longer floats past the ghost's head.
5. Bonus: video.mp4 — 8s ffmpeg Ken Burns pan/zoom over meme-a (1280x720, 30fps).
6. .makefun/owner.json written for wallet 9BcY…kQ96 (daring-coyote-94).
   main.ts smoke-tested the grader's way (MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out):
   copies POST.json byte-for-byte. POST.json itself stays the starter placeholder —
   it is filled in only after the X post exists (main session).

## Verification (480px shrink — stricter than the judge's 768x480 view)

- check-a-480.jpg: neon "make.fun" billboard fully legible; ghost unmistakable on
  the car roof; top and bottom captions fully legible. PASS.
- check-b-480.jpg: ghost with sunglasses unmistakable; "WAITING SINCE 2013" sign
  legible; "USDC" on the coin readable; both captions fully legible. PASS.

## Files

- make_meme.py — the compositing program (rerunnable, deterministic)
- meme-a.jpg / meme-b.jpg — the two memes (1280x720)
- check-a-480.jpg / check-b-480.jpg — 480px verification previews
- ghost-cutout.png — extracted mascot (intermediate, kept for reuse)
- video.mp4 — bonus 8s pan/zoom over meme-a
- POST.json — starter placeholder, untouched on purpose
- main.ts, README.md, AGENT.md, LICENSE — kit starter, untouched

STATUS: SELESAI

## v2 — ilustrasi penuh (arahan Ikhsan 2026-11-20 00:22 WIB: v1 "jelek, ga menarik")
- v1 (komposit screenshot game) DITOLAK user. v2 digambar penuh sebagai ilustrasi komik
  (gambar AI diizinkan aturan) memakai mark resmi sebagai acuan hantu.
- meme-v2-waiting.jpg: ruang tunggu — gamer jadi tengkorak bersarang laba-laba memegang
  controller, papan "NOW SERVING: 2013", kalender 2013 penuh coretan; hantu make.fun keluar
  pintu bercahaya membawa dua karung USDC + koin bintang magenta, neon "make.fun" di atas pintu.
- meme-v2-joyride.jpg: hantu naik convertible pink melempar uang, melewati antrean halte
  berkarat "GTA 6 BUS - EST. 2013"; billboard neon raksasa "make.fun".
- Caption ditambahkan via PIL (huruf besar tegas, ejaan pasti) + pratinjau cek 480px dibuat.
STATUS: SELESAI

## v3 — format dokumen (hasil pindai feed lawan 2026-11-20 00:26 WIB)
- 8 teratas feed didominasi mockup dokumen/antarmuka: layar kunci HP (#1 88,7%), paspor
  Leonida (#2), struk belanja (x2), chat bos, tiket dukungan. Ilustrasi murni hanya #7/#8.
- meme-v3-boarding.jpg: boarding pass "LEONIDA AIR" usang dari 2013 — penumpang
  "ME (AGE 15 -> 28)", penerbangan GTA6 Vice City->Leonida, "BOARDING: STILL WAITING",
  stempel DELAYED 2023/2024/2025, stiker pink "UPGRADED - PAID BY MY AI AGENT ON make.fun",
  logo hantu di kop. Artefak dokumen yang belum dipakai entri teratas mana pun.
STATUS: SELESAI
