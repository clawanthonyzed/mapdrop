# Playbook Index: mapdrop

**Owner:** remy | **Written:** 2026-11-25 (Wave 1)
Manager-only model: the manager runs each playbook; steps go to Haiku subagents (do, QC with step_qc.py, save with step_save.py).

| Trigger | Playbook file | What it produces | Needs Anthony? |
|---|---|---|---|
| Monday weekly, or Anthony says do the next city | `MAPDROP-WEEKLY-LISTING-PACK.md` | DRAFT Etsy listing pack for the next queued city plus a render readiness check | Price, Etsy shop, render install |
| Anthony or Remy says render a town, suburb or address; a catalogue town needs its 4 styles; later a paid custom order | `MAPDROP-RENDER-ON-REQUEST.md` | A3 + A4 poster files (300 dpi) and a 900 px preview per style, checked PASS/FAIL by pipeline/render_on_request.py | Only for money, accounts, customer contact |
