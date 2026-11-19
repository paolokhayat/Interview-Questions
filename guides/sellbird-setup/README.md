# Setting up Harvey (now Sellbird) from France, step by step

Checked against the repository on 19 November 2026, at commit `b212385`, version 0.4.0.
I installed it in a cloud sandbox and checked the settings below with Sellbird's own
config loader. Nothing was trained, no Claude login was used and no email was sent.

## What changed since the Eigenflow guide (4 November)

- **Harvey is now Sellbird.** The command is `sellbird`, the config is `sellbird.yaml` /
  `sellbird.local.yaml`, the repo is `github.com/ethanplusai/sellbird` (the old link redirects).
- **The licence is now AGPL-3.0**, not MIT. Running it for yourself is fine. If you modify it
  and offer it to others over a network, you have to publish your changes.
- **French opt-outs are now detected by rule.** In my test, "Merci de me retirer de votre
  liste.", "Non merci", "Pas intéressé.", "Désabonnez-moi svp" and "Ne m'écrivez plus" were
  caught. A bare "merci de me retirer" and "STOP" were **not** caught by the rules, so still
  run the test in step 9.
- **The opt-out line can now be in French.**

## Read this before you start

- **Your Claude subscription.** Sellbird calls `claude` in a loop with your login. Read
  Anthropic's consumer terms and the Claude Code legal page first: the guide's Part 7 still applies.
- **It runs Claude with `--dangerously-skip-permissions`.** Claude then runs without
  asking you first. Put Sellbird in its own folder, ideally under its own user account, with
  nothing else in it.
- **The law (CNIL).** B2B prospecting by email has no prior consent, but each email must be
  linked to the person's job and give an easy way to refuse. Ask a lawyer about
  micro-entrepreneurs before sending at volume.
- **Time to first real volume: 2-4 weeks** of mailbox warmup.

## 0. What you need

| | |
|---|---|
| A computer that stays on | macOS or Linux, ideally. Windows works with Claude. |
| Python 3.11+ | macOS: `brew install python@3.13` |
| Claude Pro or Max | with Claude Code installed and `claude login` done |
| A sending domain | a **second** domain (e.g. `eigenflow-mail.fr`), never `eigenflow.fr` itself |
| A mailbox on it | Google Workspace, about 7 $/month |
| SPF, DKIM, DMARC | set on that domain (Google Workspace admin shows you the records) |
| Warmup | TrulyInbox or another service, running 2-4 weeks before cold email |
| An email verifier | **Reoon** (600 free checks a month). Without one, no address is ever sent to. |

## 1. Install

```bash
git clone https://github.com/ethanplusai/sellbird.git
cd sellbird
python3.13 -m venv .venv && source .venv/bin/activate
pip install -e .
python -m playwright install chromium
```

Check: `sellbird --help` lists the commands.

## 2. Secrets (`.env`)

```bash
cp .env.example .env
```

Open `.env` in an editor and fill in:

- `GMAIL_CLIENT_ID` and `GMAIL_CLIENT_SECRET`. Google Cloud Console → new project →
  enable the Gmail API → Credentials → OAuth client ID, type **Desktop app**.
- `REOON_API_KEY` from reoon.com.

Never paste these into a chat or a commit. `.env` is gitignored.

## 3. France settings, before training

Copy `france_settings.py` (next to this file) into the Sellbird folder, then run:

```bash
python france_settings.py
```

It creates `sellbird.local.yaml` and sets:

| Setting | Value | Why |
|---|---|---|
| `usage.quiet_hours.timezone` | `Europe/Paris` | The default is New York time, which puts quiet hours at 4h-13h in Paris |
| `channels.email.require_approval` | `true` | Every email waits for you in the Outbox |
| `channels.email.send_window` | 09:00-18:00, Monday to Friday, in each recipient's time zone | Office hours only |
| `compliance.opt_out_line` | « Pas intéressé ? Répondez-moi simplement et je ne vous écrirai plus. » | French opt-out under every cold email |
| `compliance.precleared` | `sender_country: FR`, `prospect_country: "FR"` | Ready if you turn the Precleared check on (off by default) |
| `icp.geography` | `France` | Look for French businesses |

Then open `sellbird.local.yaml` and fill in by hand:

```yaml
persona:
  name: "Your first name"              # who signs the emails
  email: "you@your-sending-domain.fr"  # the sending mailbox
channels:
  email:
    provider: "gmail"
    link_domains: ["eigenflow.fr"]     # your main site, since you send from another domain
    warmup:
      start_date: "YYYY-MM-DD"         # the day warmup started
compliance:
  postal_address: "…"                  # a real postal address; Sellbird warns until it's set
  do_not_contact:                      # your clients and competitors, before the first run
    - "client-example.fr"
```

## 4. Connect Gmail

```bash
sellbird gmail auth     # opens a browser to log in, once
sellbird gmail test
```

## 5. Learn the product

```bash
sellbird train https://eigenflow.fr
python france_settings.py      # training resets icp.geography, so put France back
```

Training uses your Claude subscription. Afterwards, open `sellbird.local.yaml` and check
`product` and `icp`: the industries, titles and size it guessed. Fix anything wrong.

## 6. The offer

Every first email ends with one free, useful thing (for example « un audit écrit de vos
relances clients »). Open `sellbird dashboard`, go to **Your company → Your offer**, write it
and click **Use this offer**. Keep it specific and deliverable this week: no discount, no demo.

## 7. Signals and companies

```bash
sellbird signals --confirm free     # the free signals only
sellbird discover --estimate        # what it would cost, then exits
sellbird discover                   # free OpenStreetMap source
```

OpenStreetMap coverage in France is untested. If it finds too few businesses, look at
`sellbird discover --providers`. Every paid source shows its price first.

## 8. Check readiness

```bash
sellbird warmup        # SPF/DKIM/DMARC, domain age, blocklists, warmup progress
sellbird status        # must not say "Postal address: MISSING"
```

## 9. Test before any real prospect

1. Add **only your own second address** as a test: send yourself a reply from it saying
   « merci de me retirer » and « STOP ». Check that the conversation shows as opted out. If not,
   the model may still catch it, but don't count on it: watch every reply by hand at first.
2. `sellbird sending pause` must stop everything. `sellbird sending resume` turns it back on.

## 10. Run it

```bash
sellbird dashboard     # open the private link it prints; don't share it
sellbird run           # the loop; leave it running in its own terminal
```

Start with **about ten companies**. Read every email in the **Outbox** before you approve it,
and open the prospect's site to check the fact it mentions. Keep 10-20 sends a day for the first
weeks. Leave autopilot off.

## Useful later

| Command | What it does |
|---|---|
| `sellbird outbox` | Review, `--approve <id>`, `--reject <id>` |
| `sellbird usage` | How much of your Claude quota it uses |
| `sellbird export` | Just the prospect list, as CSV |
| `sellbird suppressions` | Addresses and domains it never emails |
| `sellbird sending pause` | Stop all sending at once |
