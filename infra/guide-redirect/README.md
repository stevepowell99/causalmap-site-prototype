# guide.causalmap.app redirect

`guide.causalmap.app` was the Causal Map 3 Guide, hosted on bullet.so. Since 28 September 2026 it answers every path with a 301 to `https://garden.causalmap.app/`. The bullet site is still live at `causal-map-3-guide-bullet.pages.dev` and its subscription is unchanged.

## What runs

All of it is in AWS account 740541606095 (profile `default`, the `causalmap-cli` user). Netlify plays no part.

- **DNS:** Route 53 zone `causalmap.app` (`Z0065531E99QDIQAGK2U`). `guide` is an A and AAAA alias to the CloudFront distribution.
- **CloudFront distribution** `E123EIUJS51CHM` (`d358395kr9u7lo.cloudfront.net`), alias `guide.causalmap.app`, config in `distribution.json`. The origin is never contacted, because the function answers first.
- **CloudFront Function** `guide-causalmap-redirect`, code in `redirect.js`, attached to viewer requests.
- **Certificate:** ACM in us-east-1, issued for `guide.causalmap.app` by DNS validation (the validation CNAME sits in the same zone). It renews itself while that CNAME stays.

Running cost is negligible: the function and distribution sit inside the free tier at this traffic.

## Go back to bullet

Replace the alias records with the CNAME saved in `guide-record-before.json`: delete the A and AAAA alias records for `guide.causalmap.app` and create the CNAME to `causal-map-3-guide-bullet.pages.dev` (TTL 300), in one change batch. `dns-cutover.json` is the forward change; reverse its actions to undo it.

## Rebuild from nothing

1. Request an ACM certificate for `guide.causalmap.app` in us-east-1 with DNS validation. Add the validation CNAME it asks for to the zone, then wait for it to issue.
2. Create and publish the function from `redirect.js` (runtime `cloudfront-js-2.0`).
3. Create the distribution from `distribution.json`, replacing the certificate and function ARNs with the new ones.
4. Apply `dns-cutover.json`, replacing the distribution domain name if it changed.

`guide3.causalmap.app` is an old CNAME to `guide.causalmap.app` and follows it.
