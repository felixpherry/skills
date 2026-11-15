# Examples: bad vs good

Write for every reader at once
- Bad: "**Infra:** turn on the new rule. **Product:** nothing changes for you."
- Good: "**Turning on the new rule changes nothing users see.** Infra owns the switch."

The TL;DR says how
- Bad: "**p95 checkout latency drops from 900 ms to 300 ms.**"
- Good: the same claim, then nested bullets: "Batching the price lookups saves 400 ms." "Dropping the second auth call saves 150 ms." "An index on the orders table saves 50 ms."

Tables add up to the text
- Bad: the TL;DR says errors fall 60%, and the table's rows sum to 52%.
- Good: the table gets a "Retries removed: 8%" row and a "Total: 60%" row.

Headers say what the number is out of
- Bad: a column called "Conversion".
- Good: "Conversion (orders ÷ checkout visits)".

One unit, defined once
- Bad: "Conversion falls 4 points, then 3 pp more, a 12% relative drop."
- Good: one line near the top says changes are percentage points; the body says "Conversion falls 4%, then 3% more."

A cell that looks wrong explains itself
- Bad: "Refund rate: 0%" in the first week's row.
- Good: "0% (refunds open after 14 days)".

One plain word per concept
- Bad: "abandoned carts" in one section, "ghost orders" in the next, "stale baskets" in a table.
- Good: "abandoned carts" everywhere, because that's what the team calls them.

Write as the engineer presenting the result
- Bad: "Nobody has asked the payments team, and the commit doesn't say why the timeout is 30 s."
- Good: "The timeout is 30 s. The payments team decides whether it can drop to 5 s."

Trust the reader
- Bad: "The error tracker keeps 1 in 10 events, so we multiplied by 10, then removed duplicates by fingerprint, then..."
- Good: "About 12k users hit the error a day (scaled for sampling; method in the appendix)."

Stay on the question
- Bad: an open item "Whether next month's traffic looks like this month's."
- Good: cut it, or replace it with a check: "Re-measure two weeks after launch."

A research doc opens with its method
- Bad: "This page covers the checkout latency investigation. Read it before planning."
- Good: "**Every number here comes from the raw request logs (1 to 14 Mar), not the sampled dashboard.**" Then status and date as bullets in a note panel below.
