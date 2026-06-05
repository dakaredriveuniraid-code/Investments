# Djimagem Finance — Daily Trading Simulation

## What this repo is

A **paper-trading simulation** that runs every day automatically via Claude Code on the web.
It simulates a €5,000 portfolio investing in stocks available on Revolut, using a buy-the-dip strategy.
At the end of each run it pushes the updated `portfolio.json` to this repo and sends a push notification via ntfy.sh.

## Your job when this session starts

**Run the full daily trading cycle below. Do not skip any step.**

---

## Daily cycle (run every step in order)

### 1. Read the current portfolio
Read `portfolio.json`. Note every holding's ticker, cost_eur, buy_price_usd, stop_loss_price_eur, take_profit_price_eur, and the current cash_eur.

### 2. Get current prices for all holdings
For each ticker in `holdings`, do a web search:
`"<TICKER> stock price today"` — get the current USD price from a credible source (Yahoo Finance, CNBC, MarketBeat, etc.).

### 3. Apply exit rules to each holding
Convert current USD price to EUR using assumed_fx_eur_usd (default 1.08, update if you find a better rate).
Current value EUR = (current_price_usd / fx) * shares

For each holding decide:
- **STOP-LOSS:** if current price EUR <= stop_loss_price_eur → SELL (cut loss)
- **TAKE-PROFIT:** if current price EUR >= take_profit_price_eur → SELL (lock gain)
- **EARLY EXIT:** if news/momentum signals reversal even before TP → SELL (preserve profit)
- **HOLD:** otherwise

For sells: calculate pnl_eur = current_value_eur - cost_eur. Add to closed_trades. Remove from holdings. Add proceeds to cash_eur.

### 4. Scan for new buy opportunities (buy-the-dip)
Rules:
- Universe: all stocks available on Revolut (US large/mid caps, some EU stocks)
- Look for stocks that dropped significantly (>5%) recently with a strong rebound thesis
- Only buy if the drop is exaggerated (sentiment/contagion) NOT structural (guidance cuts, fraud, fundamental deterioration)
- Max €200 per new position, max €1,000 deployed total per day (across buys and sells reinvested)
- Do web searches: `"stocks biggest losers today oversold rebound"`, `"[sector] stocks oversold June 2026"`, Kavout Kai Score picks, analyst upgrades
- Skip: stocks with guidance cuts, regulatory issues, fraud, structural problems

For each buy: set stop_loss_price_eur = buy_price_eur * 0.90, take_profit_price_eur = buy_price_eur * 1.20

### 5. Update portfolio.json
- Update holdings (add new buys, remove sells)
- Update cash_eur
- Add entry to closed_trades for each sell
- Add entry to daily_log for today

### 6. Commit and push
```bash
cd /workspace/Investments  # or wherever the repo is checked out
git add portfolio.json
git commit -m "Daily update $(date +%Y-%m-%d)"
git push -u origin main
```

The remote URL with auth is already set in the local git config from setup.

### 7. Send ntfy notification
Use `notify.py` to send ONE notification (never multiple) with this format:

```
DATA: <date>
Investido: <X> EUR | Cash: <Y> EUR | Saldo total: <Z> EUR

POSICOES (<n> abertas):
- <TICKER>  <valor_atual EUR>  <+/-X.X%>  ↑/↓
- ...

VENDAS hoje:
- <TICKER> vendido a <preco> → <+/-X EUR> (<motivo: SL/TP/saida antecipada>)
(ou "nenhuma")

COMPRAS hoje:
- <TICKER>  <X EUR>  <tese em 1 linha>
(ou "nenhuma")
```

Run: `python3 notify.py "<message>"`

---

## Rules summary
- Max €200 per position, max €1,000/day deployed
- Stop-loss: -10% from entry
- Take-profit: +20% from entry
- Early exit if momentum reversal detected (even below +20%)
- Only buy exaggerated dips, never structural falls
- Universe: all Revolut stocks (US + some EU)
- Source: credible financial news (Reuters, Bloomberg, CNBC, Yahoo Finance, Kavout, MarketBeat)

## Files
- `portfolio.json` — single source of truth for the portfolio state
- `notify.py` — sends ntfy push notification to iPhone
- `requirements.txt` — Python dependencies

## Important
- Always push portfolio.json after every run
- Never send more than 1 notification per day
- This is a simulation — not real money, not financial advice
