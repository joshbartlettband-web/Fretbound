#!/bin/bash
set -e
cd "$(dirname "$0")"
AJ=/usr/lib/android-sdk/platforms/android-23/android.jar
rm -rf obj bin && mkdir -p obj bin assets && cp ../index.html assets/index.html
# the signing key is never committed: put it in the FRETBOUND_KEYSTORE_B64 environment variable (base64 of fretbound.keystore)
[ -f fretbound.keystore ] || { [ -n "$FRETBOUND_KEYSTORE_B64" ] && echo "$FRETBOUND_KEYSTORE_B64" | base64 -d > fretbound.keystore; } || true
[ -f fretbound.keystore ] || echo "WARNING: no keystore found; a new key will be made and phones with the old build must uninstall it first"
javac -source 8 -target 8 -bootclasspath $AJ -classpath $AJ -Xlint:-options -d obj src/com/fretbound/game/MainActivity.java
dalvik-exchange --dex --output=bin/classes.dex obj
aapt package -f -0 arsc -M AndroidManifest.xml -S res -A assets -I $AJ -F bin/unsigned.apk
(cd bin && aapt add unsigned.apk classes.dex >/dev/null)
zipalign -f -p 4 bin/unsigned.apk bin/aligned.apk
[ -f fretbound.keystore ] || keytool -genkeypair -keystore fretbound.keystore -storepass fretbound -keypass fretbound -alias fretbound -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Fretbound Prototype" >/dev/null 2>&1
apksigner sign --ks fretbound.keystore --ks-pass pass:fretbound --key-pass pass:fretbound --ks-key-alias fretbound --out bin/fretbound.apk bin/aligned.apk
apksigner verify --print-certs bin/fretbound.apk | head -2
aapt dump badging bin/fretbound.apk | grep -E "package:|sdkVersion|targetSdk|launchable" 
ls -la bin/fretbound.apk
