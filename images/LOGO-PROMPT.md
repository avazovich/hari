# Logo generation prompt

Paste everything inside the code block into your image-generation agent.
Save results into `images/logo/` using the filenames given.

```
You are designing logo concepts for "Hari" (Korean: 하리), an online store selling original Korean skincare and cosmetics to customers in Uzbekistan. The brand feels soft, fresh, modern and trustworthy — glowing "dewy" skin, gentle Korean minimalism, young women 18–35.

IMPORTANT OUTPUT RULES:
- Generate each concept below as its OWN separate image file. Do NOT put several logos into one image, grid, sheet, or mockup board.
- Produce exactly 8 images, one per numbered item, in the order listed.
- Name each file with the filename given in brackets.
- Every logo must be centered on a plain flat background with generous empty space around it. No mockups, no 3D, no shadows, no photos, no extra text, no taglines unless asked.

BRAND STYLE (apply to all):
- Name spelled exactly: "hari" (all lowercase) — check spelling letter by letter, no extra or missing letters.
- Colors: blush pink #FFB3C7, deeper rose #FF7AA2, near-black plum #1F1A24, white. No other colors.
- Flat vector style, clean geometric shapes, smooth curves, simple enough to work as a tiny app icon and on a cosmetic jar lid.
- Typography: modern rounded sans-serif, soft but confident, slightly heavy weight, tight letter spacing.
- Motif ideas: a single dew drop, a soft glow / shine sparkle, a gentle circle like a cushion compact. Keep it minimal — one motif at most.
- Do not imitate any existing brand logo. Original design only.

CONCEPTS:

1. [logo-wordmark.png] 3:1 — Wordmark only: "hari" in plum #1F1A24 on white. The dot of the "i" is replaced by a small rose-pink #FF7AA2 dew drop.

2. [logo-wordmark-pink-bg.png] 3:1 — Same wordmark as concept 1 but in white on a blush pink #FFB3C7 background, with the dew drop in plum.

3. [logo-monogram-circle.png] 1:1 — Monogram: a lowercase "h" in plum inside a solid blush pink #FFB3C7 circle, with a tiny white sparkle at the top right of the letter, like light reflecting on glowing skin.

4. [logo-dewdrop-symbol.png] 1:1 — Symbol only, no letters: a soft rounded dew drop shape in rose #FF7AA2 with a small white curved highlight, plum-free, on white. Simple enough for a favicon.

5. [logo-combination.png] 3:1 — Combination mark: the dew drop symbol from concept 4 on the left, the "hari" wordmark in plum on the right, aligned on one baseline, on white.

6. [logo-hangul.png] 3:1 — Bilingual lockup: "hari" wordmark in plum, and below it the Korean "하리" in a small, clean, rose #FF7AA2 sans-serif. Render the Korean characters 하 and 리 correctly. On white.

7. [logo-app-icon.png] 1:1 — iOS app icon: rounded-square tile filled with blush pink #FFB3C7 to rose #FF7AA2 soft gradient, centered white lowercase "h" with a tiny white dew drop. No text other than "h".

8. [logo-dark.png] 3:1 — Wordmark "hari" in white with the rose #FF7AA2 dew drop, on near-black plum #1F1A24 background (for dark footers and packaging).

Generate all 8 now, one separate image each.
```

If the agent stops partway, reply: "continue from concept N".

Notes:
- AI image tools often misspell text and garble Korean (하리). Check every letter.
- Use the AI images to pick a direction only. For the final logo, rebuild the chosen concept as a clean vector (SVG) so it stays sharp on the site, packaging and print.
