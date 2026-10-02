#!/bin/bash
# Playwright (pip) may want a newer Chromium build than the one pre-installed in /opt/pw-browsers (and cannot download one when the network blocks cdn.playwright.dev).
# This links the installed build under the names Playwright asks for, so the plain p.chromium.launch() used by tests/*.py works.
set -e
B=${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}
OLD=$(ls -d $B/chromium-[0-9]* | head -1); OLDH=$(ls -d $B/chromium_headless_shell-[0-9]* | head -1)
NEW=$(python3 - <<'PY'
import json,glob,os
d=os.path.join(os.path.dirname(__import__('playwright').__file__),'driver','package','browsers.json'); j=json.load(open(d))
print({b['name']:b['revision'] for b in j['browsers']}['chromium'])
PY
)
[ -e $B/chromium-$NEW ] || ln -s $OLD $B/chromium-$NEW
mkdir -p $B/chromium_headless_shell-$NEW/chrome-headless-shell-linux64
ln -sf $OLDH/chrome-linux/headless_shell $B/chromium_headless_shell-$NEW/chrome-headless-shell-linux64/chrome-headless-shell
echo "linked chromium $NEW -> $(basename $OLD)"
