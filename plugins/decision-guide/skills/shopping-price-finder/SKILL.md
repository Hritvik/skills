---
name: shopping-price-finder
description: Run a requirements Q&A, then compare live offers for an exact retail product by delivered price and normalized unit cost. Use for recommendation-only shopping research; it does not add to cart, order, subscribe, or purchase.
---

# Shopping Price Finder

Find the best comparable offer, not merely the lowest displayed number. This skill is recommendation-only.

## Requirements Q&A

Always begin before searching. Restate what is already known and ask one compact batch covering only missing or ambiguous requirements:

- exact product, variant, size, flavor, and acceptable substitutes
- desired quantity or comparison basis (single item, pack, or bulk)
- delivery city or area; request a precise pincode only when retailer availability requires it
- urgency, budget, membership eligibility, and whether conditional coupons are acceptable
- priorities besides price, such as seller trust, delivery speed, freshness, or return policy

Wait for the answers, summarize the agreed constraints, and do not repeat established questions. Treat a full address, pincode, or account-specific delivery area as sensitive location data: ask for explicit confirmation before entering it into a retailer site.

## Compact research workflow

Use current web or browser results because prices and stock change. Search the exact identifying phrase once, then verify promising offers on direct product pages. Compare at most five credible retailers and inspect only the strongest three in depth.

For every offer, verify:

- exact product identity, variant, net quantity, pack count, and seller
- stock status and delivery eligibility for the known location
- current item price, mandatory fees, delivery charge, minimum-order constraint, and taxes when shown
- whether a price requires membership, subscription, coupon, new-user status, payment method, or bulk purchase
- expiry or freshness information when visible and materially relevant

For FMCG items such as protein bars, check brand-store listings, credible marketplaces, and quick-commerce options when location is known. Confirm flavor, grams per bar, number of bars, and vegetarian/dietary variant when those values distinguish SKUs.

Exclude or clearly label sponsored snippets, stale search prices, unavailable listings, different sizes, marketplace bundles with ambiguous counts, and offers whose final cost cannot be verified. Never claim a price is delivered when mandatory fees are unknown.

For durable goods, verify the product's current lifecycle status on the manufacturer's regional site before recommending it. Retailer catalogs may continue to show discontinued models. Confirm the exact regional model and hardware revision when revisions can change ports, standards, firmware support, warranty, or compatibility. Treat an unclear revision as a purchase caveat rather than merging specifications from different versions.

When the product depends on an existing installation, ask only for context that can change the recommendation: current equipment, connection or interface type, available wiring, placement, space constraints, and intended future reuse. Prefer a cheaper product when existing infrastructure removes the need for a more expensive capability. Do not treat advertised range, throughput, battery life, or similar laboratory maxima as expected real-world performance.

Recheck price, stock, seller, and lifecycle status immediately before presenting a purchase-ready recommendation when they may have changed during the conversation. If the user wants to verify the offer themselves, open direct product pages in the requested browser surface and leave those tabs available; do not add anything to the cart.

## Comparison

Compute like-for-like values from verified quantities:

- effective item cost = item price minus unconditional discounts
- delivered cost = effective item cost plus mandatory fees shown for the order
- per-unit cost = delivered cost divided by item count
- weight-normalized cost = delivered cost divided by total grams, reported per 100 g when useful

Do not mix a single bar with a multipack or a 30 g SKU with another weight without normalization and an explicit label. Keep conditional offers separate from the unconditional winner. A larger pack is not “best” when it exceeds the requested quantity or creates a materially higher total spend unless the user accepts bulk buying.

For tiered comparisons, show the incremental cost between the strongest value option and the upgrade, then explain what that increment buys in the user's actual setup. Re-rank when a sale makes the higher tier only marginally more expensive. Remove unavailable or discontinued products rather than retaining them as theoretical winners.

For marketplace offers, evaluate listing trust separately from product quality. Check seller identity and tenure, seller rating, platform fulfilment or assurance, invoice availability, warranty terms, support or return window, verified-buyer history, and specification consistency. Flag mismatches between retailer warranty claims and the manufacturer's regional warranty. A steep discount alone is not evidence of fraud when the seller and listing have strong trust signals.

## Boundaries

Never add items to a cart, apply coupons, start trials or subscriptions, place orders, or purchase. Do not enter passwords, OTPs, card details, CVVs, or payment data. If the user requests purchasing, explain that this skill currently stops at verified recommendations and requires a separate secure checkout capability.

Keep cross-turn state compact: exact SKU, location granularity, quantity, accepted conditions, verified offers, rejected mismatches, and verification time.

## Result

Lead with the best unconditional offer, followed by at most two alternatives such as the best bulk value or fastest credible delivery. Include retailer, exact pack, item price, known fees, delivered total or “fees unknown,” normalized cost, conditions, stock/location status, verification time, and a direct product link. Distinguish verified facts from judgement and state that no cart or purchase action was taken.

After the user reports a purchase, stop price shopping unless asked. Assess the purchase against the agreed constraints and give a short acceptance checklist for anything that should be verified within the return or support window, such as identity and revision, serial numbers, invoice and warranty eligibility, included parts, firmware or software updates, ports or core functions, and representative real-world performance.
