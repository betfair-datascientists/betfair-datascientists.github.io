# 10 Golden Rules of Automation

Automation can be one of the most powerful tools in the arsenal of Betfair punters, but it can also be dangerous if handled and implemented without the requisite preparation for, and understanding of, the operating environment.

So let's walk through the key areas that need to be properly attended to when deciding to launch an automated strategy. This walkthrough will primarily focus on those who write their own code, but many concepts should also be applied to code that someone else might have written for you.

---

## 1. Study the Market Dynamics

A solid understanding of the markets you plan to bet into is the strongest possible foundation for developing an automated strategy. This means taking the time to study how those markets behave: how liquidity builds and evolves both pre-play and in-play, where it concentrates, and how much is available at each stage. Observing how liquidity moves helps you form views on what money is likely to be sharp and what is more recreational.

Not all edges are purely statistical. Some arise from market structure and behavioural responses. For example, cricket markets often overreact to the fall of a wicket before correcting, or a horse known to jump poorly but finish strongly may be mispriced early in a race.

It’s also important to understand data that sits outside the market itself and how it influences prices. Factors such as trainer information, mounting yard behaviour, or weather can all affect outcomes and market reactions. In AFL, in-play odds tend to closely reflect on-field events, while pre-play markets are more sensitive to news such as injuries, suspensions, or team selection. Some participants even believe indicators like a greyhound defecating before a race carry predictive value. The key is to study the data, test your assumptions, and decide for yourself what genuinely matters and what can be ignored.

## 2. Understand the Market Rules

Study the market rules. The importance of this cannot be overstated. Before running any automation, you must understand how your bets can be affected by events outside your control.

Betfair market rules often differ from those of traditional wagering operators. Common examples include:

 - In greyhound markets, if there is a scratching, all matched and unmatched **LIMIT** bets are voided, while **SP** bets stand. Hedging via BSP can therefore leave you unexpectedly exposed.
 - In the event of a late scratching, certain markets, such as Exotics and Cashback 2nd, are typically voided in their entirety.
 - In tennis, match odds markets are voided if a walkover occurs before one set has been completed.
 - In soccer, matches using video assistant referees (VAR) can have bets voided if a goal is overturned. This can create problems if you place a bet pre-play and rely on leaving it in-play to hedge.
 - Betfair Australia cannot offer bets on participants under 18. This affects sports such as golf, tennis, and AFL, and can result in delayed markets, voided markets, or separate Australian-only markets without access to global liquidity.
 - Outcomes that are no longer possible are not always removed from markets. Managing these positions is your responsibility. For example, in a soccer match that is 1–1, it may still be possible to bet on 0–0 in the correct score market.
 - In head-to-head racing markets, if neither runner qualifies for prize money, the entire market is voided.

Understanding these rules is critical, as automation will execute exactly as instructed, regardless of whether the market behaviour aligns with your assumptions.

## 3. Avoid Data Leakage

It’s very easy to make backtests look profitable if you introduce data leakage. Data leakage occurs when your model uses information that is available now, but would not have been known at the time the bet was placed.

The most common example is using the final BSP to decide whether to place a bet. Like the Tote, the final BSP is not known until after it has been reconciled, at which point no further SP bets can be placed. In horse racing, you may still be able to place a bet that could be matched in-play, but there is no guarantee of a match. In greyhound racing, once the BSP is reconciled, no further bets can be placed at all. This is why some strategies focus specifically on predicting BSP, rather than using it directly.

Another frequent source of data leakage comes from statistical datasets that update after the event has occurred, or that calculate minimums, maximums, or aggregate figures based on a participant’s full history, rather than only the data available prior to that race or match. For this reason, many modellers discard pre-calculated fields and instead derive features manually from raw, time-stamped data.

A practical way to check for data leakage is to paper trade a strategy for a week or two, then run a backtest over the same period using only information that would have been available at the time. If the results differ materially, data leakage is likely present.

## 4. Do Not Overfit

Overfitting can occur both during model development and at the betting strategy stage, particularly when there is insufficient data to distinguish a genuine edge from natural randomness or variance.

At the model training stage, overfitting often appears as a large gap between training and test performance. This is commonly caused by having too many features relative to the amount of data, or by an overall lack of data. To assess robustness, validate the model on truly out-of-sample data that is unseen by both the training and test sets. When creating features, prioritise simple, explainable rules that hold up across different market conditions, rather than complex constructions that only work in a narrow regime.

Overfitting can also creep in when developing the betting strategy itself. Not every betting angle will be profitable, but there may be regions where bets on one side of a parameter threshold perform well while those on the other do not. These cutoffs should be grounded in logic, not chosen arbitrarily, and the profitable sample must represent a meaningful proportion of the data. Statistical significance can be assessed using measures such as p-values.

A useful diagnostic is to plot profitability on the y-axis against the parameter of interest on the x-axis. A clear, consistent structure, such as a stable peak or trough, is a positive signal. If the plot shows no discernible pattern and is dominated by noise, it is usually a sign that the parameter should be reconsidered or discarded.

## 5. Know When A Backtest Is Too Good To Be True

Use realistic assumptions in your backtesting. Where possible, run simulations on actual market stream files to estimate fill rates accurately. Even if money at your target price is matched, your position in the queue often means you don’t get filled, and the market may then move against you. This is known as fill bias (often called “odds slippage”) and is a real, observable behaviour in both financial and betting markets, where losing bets are more likely to be filled and winning bets go unmatched.

To mitigate this, calibrate your fill assumptions using live paper trading or small-stakes real betting. Only scale once real-world execution aligns with your backtest assumptions. It’s also important to define how your strategy responds when prices move against you. Do you take a worse price to exit, take SP, leave a bet in-play, or allow it to lapse? These execution rules materially affect outcomes and must be explicitly tested.

Beyond mechanics, think creatively when designing your backtests. Ask yourself: what can I do differently from the market in a scalable way? If you’re betting at BSP, which everyone can observe historically, where does your advantage come from? It may be through a disciplined staking approach, superior execution, or identifying moments when the market over-corrects to new information and temporarily misprices an outcome. As a rule of thumb, the easier an edge is to identify, the more competition you should expect.

## 6. Do Not Underestimate The Importance of A Staking Plan

A poor staking plan can undo an otherwise strong model, so it deserves just as much thought as the model itself. A sound staking approach should be aligned with both your edge and your risk tolerance. For example, if you are running a lay strategy, consider how liability scales with price. Laying longshots at prices above $100 can quickly become problematic if you are not prepared for occasional large losses. Conversely, when backing short-priced favourites, you need to account for the impact when a “near certainty” loses.

There are several common staking approaches:

 - **To lose $X**: Flat staking for backs, or flat liability for lays. Simple and robust, but may underutilise a strong edge.
 - **To win $X**: Stakes vary to target a fixed profit, increasing exposure at shorter prices.
 - **Proportional staking**: Stakes are scaled relative to price, often by dividing a fixed amount by the odds. Care is needed here, particularly for laying, as linear scaling is not always optimal.
 - **Kelly staking**: Stakes are set in proportion to the estimated edge. This can maximise long-term growth, but is highly sensitive to estimation error, and large drawdowns can occur if the edge is overstated.
 - **Martingale**: Stakes increase after losses rather than decrease. This approach dramatically increases risk and is generally unsuitable for sustainable betting.

Each method has trade-offs. The key is to choose a staking plan that matches the reliability of your edge, controls downside risk, and allows you to survive the inevitable variance long enough for that edge to express itself.

## 7. Know How To Manage Your Bankroll

Bankroll management can be challenging, particularly on exchanges that do not offer separate wallets or multiple accounts. The most important principle is to avoid over-exposure to any single outcome. Your automation should include safeguards that limit both the number of open bets and the total exposure at any given time. Balance checks should also be a standard part of the bet placement process to prevent **INSUFFICIENT_FUNDS** errors.

There are differing views on whether an automation should include daily stop-loss or take-profit rules, effectively halting betting once a defined loss or profit threshold is reached. Whatever approach you choose, your bankroll must be large enough to comfortably absorb your maximum possible net exposure. It’s also worth noting that Betfair Australia accounts have a default exposure limit of $15,000. Any increase requires an application and is subject to a mandatory seven-day cooling-off period before taking effect.

A common question is how to separate automation funds from general betting funds. Since Betfair does not provide separate wallet functionality, there are two practical options. One is to withdraw the funds and hold them in a bank account until needed. The other is to “hide” funds from your automation by placing them as an unmatched bet, typically in a long-term futures market at an extremely high back price or a very low lay price where matching is highly unlikely. When you want to redeploy the funds, simply cancel the bet.

In all cases, the goal is the same: ensure your automation operates within well-defined financial limits so that execution errors or short-term variance don’t threaten the survival of the strategy.

## 8. Be Committed To Clean, Maintainable Code

Writing modular, readable, version-controlled code can feel like a tall order when you’re first learning to program. As your skills improve, however, regularly reviewing and refactoring existing code should become a normal part of your workflow. Making urgent changes to spaghetti code is rarely enjoyable and often leads to extended downtime, especially when fixes are needed but time is limited. Stable systems tend to produce fewer unpleasant surprises.

Aim to create small, well-named helper functions and organise them logically. Use separate configuration and credentials files to keep sensitive details and environment-specific settings out of your core logic, and minimise hard-coded values wherever possible. This compartmentalisation makes the codebase easier to reason about and safer to change.

Even if the code is only for your own use, good code hygiene pays dividends. It reduces friction for future you, lowers the risk of errors, and steadily improves your overall programming discipline.

## 9. Have An Error Logging and Error Handling Framework

If you’re using a pre-built framework such as Flumine, much of the error handling is already taken care of. If you’re building your own system, however, you’ll need to spend significant time understanding the finer details of the Betfair API: what errors can occur, why they occur, and how they should be handled. Errors can arise at the market, bet, or account level, and all of these need to be addressed in any ground-up implementation. Left unhandled, errors can lead to transaction charges, temporary API lockouts, or, in the worst case, suspension or closure of your Betfair account.

To manage this properly, start by familiarising yourself with both the wrapper documentation (if applicable) and the Betfair API documentation itself. When testing and deploying an automation, log as much detail as is practical to structured log files, and make sure you understand what each log entry represents. If you ever need to raise a ticket with Betfair support, API logs are a standard requirement, and for issues involving the streaming API, connection IDs will also be requested. Your logs are your forensic trail.

Many automated punters also implement watchdogs or kill switches that monitor bet placement, running profit and loss, or other key metrics, with the ability to halt the system if something goes wrong. These alerts and controls are often integrated with tools such as Discord, WhatsApp, or other messaging services via webhooks. They’re particularly useful when you’re away from your computer, or once a strategy has been running long enough to justify moving to a lower level of active supervision.

## 10. Remember That Every Bet Is A Choice That You Make

While automation removes emotion and executive decision-making from the act of placing bets, those same factors remain critically important during system design, along with discipline. Running an automated strategy can feel less like trading on the floor of an exchange and more like being strapped into a rollercoaster, where outcomes unfold beyond your immediate control. When things are going well, this can be enjoyable and satisfying. When negative variance hits, however, awareness of your risk tolerance and emotional responses becomes essential.

Automated betting should be treated as a long-term engineering project, not a sequence of individual bets. Manual betting can be entertaining, but those discretionary bets are not equivalent to an automated strategy and should be viewed as data points at most. During periods of drawdown, resist the urge to “tinker” around the edges. This is especially important because logging, version control, and disciplined evaluation tend to break down under emotional pressure.

If changes are required, be explicit about why they are being made and document the reasoning. Adjustments should be grounded in real-world behaviour, supported by data, and aligned with the original design intent. This mindset is often the difference between a system that survives variance and one that quietly self-destructs.

---

Each of these 10 rules has been only briefly touched on here, but they are all as important as one another, so taking the time to understand them will only improve your automation skills! 