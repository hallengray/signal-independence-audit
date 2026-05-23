> **Note:** This is the canonical Markdown source. The published version is hosted at <https://hallengray.github.io/signal-independence-audit/MSS_POST.html>. It's a follow-up to the main story, [_Four crypto strategy failures, and the tool that caught one in 3 seconds_](./BLOG_POST.md).

# The fifth failure: I lowered my own bar, combined the losers, and it still didn't work

> _A short, honest story about giving yourself "one more try," including the part where you quietly move the goalposts and then have to admit it._

## Where I'd left things

I'd spent four rounds trying to build a crypto trading strategy that actually made money on BTC and ETH spot at the 4-hour timeframe. All four failed. Not "failed and I tweaked them until they passed," but failed against a standard I set before I started and refused to soften: an out-of-sample Sharpe ratio above 1.0 and a profit factor above 1.4. (The Sharpe ratio scores how much return you earn for the risk you take. Profit factor is simply the dollars you won divided by the dollars you lost. Out-of-sample means measured on data the strategy never saw while it was being built.) So I stopped hunting for a winning strategy and shipped the useful thing those failures had produced instead: a tool that tells you in about three seconds whether a trading idea is even worth testing.

That should have been the end. This is the story of the "one more try" I gave myself anyway, and why I'm oddly glad it didn't work.

## The itch I couldn't leave alone

There was one mechanism I'd never tested. Every strategy I'd built assumed the market behaves one way. But markets have regimes, which is a fancy word for moods: sometimes they trend, sometimes they drift sideways, sometimes they fall. What if a strategy could detect the current regime and switch tactics to match it? That's a regime-switching strategy, and pairing it with a Markov classifier (a standard method for labelling which mood you're in) is what gave my candidate its name: the Markov-Switched Strategy, or MSS.

So I let myself take one last shot, and I did the one thing that keeps a project like this honest. I wrote it down, on the record, as an exception (ADR-0023, for the paper trail), not as a breakthrough that demanded another look. The evidence said stop. I just wanted to test this one idea first.

MSS was a switch-hitter:

- Market trending up (a "bull" regime)? Ride it with a Donchian breakout, which buys when price breaks above its recent high.
- Market drifting sideways? Buy the dips with a Bollinger Band signal, which buys when price drops unusually far below its recent average and expects it to bounce back (this is called mean reversion).
- Market falling (a "bear" regime)? Do nothing. Sit in cash.

If those two tactics sound familiar, they should. They are the exact trend-following strategy (I'd called it MFD) and mean-reversion strategy (BMR) that had already failed me in earlier rounds, bolted together, with the regime detector deciding which one to use at any moment. The bet was that switching between two losers, at the right times, might add up to a winner.

## The confession I have to make before the result

Here's the uncomfortable part, and I'm putting it before the result on purpose.

To give this idea its best possible shot, I lowered my own bar. The whole project rested on that Sharpe ratio, the return-for-risk score, and for four rounds I'd held its pass mark at 1.0 and refused to budge. For this one experiment I rewrote the scorecard (I called the new version §14-v2) and dropped the Sharpe pass mark to 0.85.

I can dress that up. The new scorecard also made other things stricter: a tighter limit on drawdown (the worst peak-to-trough fall in your account), plus new checks like the Sortino and Calmar ratios, which are close cousins of Sharpe that focus specifically on downside risk. But that would be a dodge. The Sharpe pass mark of 1.0 was the one number every previous strategy had died on. Lowering it is lowering the exact thing that mattered. It was my call, it was not forced by any evidence, and I even wrote in the decision record that it was "operator judgment, not figures the audit evidence compels." If this experiment had succeeded, that lowered bar would hang over the whole result like a question mark.

It didn't succeed. So the question mark is moot, but you deserved to know about it before you saw the outcome, not after.

## For the first time ever, my own filter said "go"

Before spending any real effort tuning it, I ran MSS through that three-second filter I'd built, the one designed to kill bad ideas early. It's called the Signal Independence Audit (SIA), and its job is to check whether a trading signal genuinely carries new information or is just noise dressed up as insight. For the first time in the entire project, it passed.

I want to be precise about what that means, because it's the whole point. Passing SIA means "not obviously dead, go ahead and run the expensive test." It does not mean "this works." Plenty of things clear the metal detector and still turn out to be junk. MSS was about to be a very clean demonstration of that.

## Then I tested it on the future, and it lost money

The real test in this game is called out-of-sample testing, and it's simple to describe. You tune the strategy on years of old data (the in-sample, or training, window), then turn it loose on a stretch of recent data it never saw during tuning. Anyone can make a strategy look brilliant on the data they built it around. The only honest test is the data it has never met.

The tuning itself (the automated parameter search, known as a hyperopt) had only two dials to turn: how tight to set the stop-loss (the automatic "sell if it falls this far" order) for each of the two tactics. I ran that search three separate times from different random starting points (a standard robustness check), kept the best handful of versions from each run, and tested all five survivors on about sixteen months of unseen market action from 2025 into 2026. Realistic costs were baked in: a 0.10% exchange fee plus 0.05% slippage (the gap between the price you expect and the price you actually get) on every trade.

Every single one lost money.

The best version lost about 9% over those sixteen months. Its profit factor was 0.78, meaning that for every dollar it won, it lost about a dollar twenty-eight. Its out-of-sample Sharpe ratio was negative, roughly -0.23, which means it produced a negative return for the risk it took: you would have been better off leaving the money in cash and going for a walk. And remember, that is after I had already lowered the Sharpe pass mark to 0.85. It didn't miss by a whisker. It came in below zero.

## The genuinely interesting bit: why it lost

This is the part worth keeping. I split the results by which tactic, or "leg," made each trade:

- The trend-following leg (the Donchian breakouts) actually made a little money: 145 trades, net positive.
- The mean-reversion leg (the Bollinger dip-buys) bled badly: 240 trades, deeply negative. It kept buying dips that just kept dipping.

So the regime-switching itself worked. The detector correctly handed trades to each tactic; it did not get confused or quietly collapse into using only one of them. MSS failed for a much simpler reason: one of its two ingredients is genuinely unprofitable on real forward data, and the okay ingredient could not carry the dead weight. Two losing strategies did not combine into a winner. They combined into a more complicated loser.

## One thing I won't sweep under the rug

There was so little to tune in this strategy, just those two stop-loss dials, that one of my usual robustness checks was meaningless here. The entire search space was only about 546 possible combinations, so when I say I ran the tuning three times to see whether it agreed with itself, of course it agreed. There was barely anywhere else for it to land. I'm mentioning it because leaving it out would be exactly the kind of quiet dishonesty this whole project exists to avoid. I also skipped the final walk-forward step (re-testing the strategy across several rolling time windows), because a strategy that loses across the entire out-of-sample stretch cannot suddenly pass on smaller slices of it. The verdict was already in.

## So what does this actually mean?

Not that I "failed five times." This last attempt ran under a lower bar, so it doesn't even count as a fair fifth try under the original standard.

What it means is sharper than that. Even after I lowered my own Sharpe bar, even with a brand-new mechanism (regime-switching), even after my SIA filter gave its first-ever green light, the market still said no. The most generous, most favourable shot I was willing to take still lost money out-of-sample. That doesn't weaken the conclusion I'd already reached. It hardens it.

And the discipline held where it counts. I locked the rule for which tuned version I would "pick" into a written decision record (ADR-0026) before I ever looked at a single out-of-sample number, so there was no quietly crowning a winner after the fact. As it turned out, there was no winner to crown.

So where does this leave me? Not declaring victory, and not declaring the question dead either.

What I've run out of is my own current list of ideas, not the appetite to keep looking. Four strategies, plus one regime-switching combination of them, have now failed this market's honest test. That tells me a great deal about what does not work on BTC and ETH spot at the 4-hour timeframe. It does not tell me that nothing works, and it would be arrogant to pretend I've thought of everything.

So I'm doing the opposite of closing the book. If you do this for a living, or you have a signal, a feature, or an angle I haven't tried, drop it in the comments. Tell me what I'm missing. That's a genuine request, not a rhetorical flourish. The whole reason I built the Signal Independence Audit was so that testing a new idea costs about three seconds and a straight yes or no, instead of a month of fooling myself. Bring me something credible and I'll run it through the exact same test you just watched five strategies fail, with the Sharpe bar put back where it belongs at 1.0, and I'll publish whatever comes out, win or lose. If a real candidate survives the screen, there will be another phase, and I'll be glad to write it up.

The strategies were the experiment. The honest test, and the willingness to keep running it, is the real result.

---

_The full technical kill record is in [case-study/11-mss-kill-adr-0027.md](./case-study/11-mss-kill-adr-0027.md). The tool itself, including how to install it and a runnable demo, is in [the repo README](./README.md)._
