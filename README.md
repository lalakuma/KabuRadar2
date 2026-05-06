# KabuRadar Refactored (Workspace Copy)

This folder is a cleaned and safer workspace copy based on the investigation of
`C:\share\MorinoFolder\Python\KabuRadar`.

## What is improved

- Centralized config loading (`ini` + environment variable override)
- Removed hardcoded absolute paths from launcher logic
- Removed hardcoded LINE token/user IDs from source code
- Added dependency manifest (`requirements.txt`)
- Added sample environment file (`.env.example`)

## Directory layout

- `src/kaburadar/config.py`: config access helpers
- `src/kaburadar/launcher.py`: time-window batch launcher
- `src/kaburadar/notification/line_notify.py`: LINE notification client
- `bat/1.kabu_main.bat`: launcher entrypoint (compatible naming)
- `bat/2-1.kabu_screening_trade_GetYahooF.bat`: HI workflow
- `bat/2-2.KabuStation_kessai_GetYahooF.bat`: LO workflow
- `bat/2-3.GetKabuka_GetYahooF.bat`: price update workflow
- `bat/screening.bat`: run HI then LO
- `bat/3.suspend.bat`: workspace-safe placeholder
- `config/config_hi.ini`, `config/config_lo.ini`: sample runtime configs

## Quick start

1. Create virtual environment and install dependencies.
2. Copy `.env.example` to `.env` and fill secrets.
3. Adjust `config/config_hi.ini` / `config/config_lo.ini`.
4. Run:

```bat
bat\1.kabu_main.bat
```

## Notes

- This is intentionally non-destructive and kept separate from the original
  project.
- Batch flow names are normalized and can be adjusted in
  `src/kaburadar/launcher.py`.
