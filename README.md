# Hari — K-beauty store for Uzbekistan

Korean cosmetics e-commerce storefront (prototype). Layout modelled on pont.uz, adapted for skincare.

## Run locally
    python3 -m http.server 8765
Then open http://localhost:8765

## Structure
- `index.html` — whole site (HTML + CSS + JS, product data inside `const P = [...]`)
- `brand/` — full Hari brand kit (logos in SVG/EPS/PNG/WebP, favicons, app icons, colour tokens). Source of truth — don't edit.
- `assets/` — web copies used by the site: tightly-cropped logo SVGs, favicon, app icons, web manifest
- `data/catalogue.js` — verified product data (official names, sizes/shades, SKUs, barcodes, descriptions, key ingredients, usage). Generated — edit `scripts/build_catalogue.py`, then run `python3 scripts/build_catalogue.py`
- `data/research-*/` — raw product data saved from official brand stores, used by the build script. Kept locally only (git-ignored), so the script runs on the original machine; the site itself only needs `data/catalogue.js`
- `images/` — put generated images here (see `images/IMAGE-PROMPT.md` for the prompt and filenames)

## Status
- [x] Catalogue, skin-type filter, search (RU aliases), brands, collections, routines
- [x] Product modal (volume/shade, skin types, how-to, delivery), cart with free-shipping bar, split ×2
- [x] Responsive product detail layout: separate thumbnail strip, variant-aware photos and price/discount panel, expandable information, keyboard focus handling; consistent card/cart pricing and category navigation
- [x] Generated lifestyle images wired in (originals in images/originals/)
- [x] Drawn packshots per product (shape + label); real photos auto-override from images/products/ (see README.txt there)
- [x] Hari logo in header + footer, favicon, app icon, web manifest
- [x] All 42 products verified against official brand stores (names, sizes/shades, SKUs, barcodes, photos); per-size prices; no invented expiry dates or ratings. 15 products whose brand stores were unreachable were replaced with same-category products from reachable official stores.
- [ ] Before going public: set HARI_BRAND_IMAGES to false and use distributor-approved photos in images/products/
- [ ] Real UZS prices, stock, expiry per batch, photos, reviews — from supplier
- [ ] Uzbek language (O'zbekcha) switch
- [ ] Backend + admin panel
- [ ] Click / Payme / Uzum Nasiya payments, orders to Telegram bot
