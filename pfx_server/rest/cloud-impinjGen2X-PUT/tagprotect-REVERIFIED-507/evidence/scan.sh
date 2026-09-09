#!/bin/bash
# scan.sh <mode_json_file> <seconds> <outfile> [start_body]
R=10.233.48.49
MODEF=$1; SECS=$2; OUT=$3; STARTBODY=${4:-'{}'}
tok() { curl -sk -m 25 -u 'admin:Zebra@123' https://$R/cloud/localRestLogin \
        | python3 -c "import sys,json;print(json.load(sys.stdin)['message'])"; }
curl -sk -m 40 -X PUT -H "Authorization: Bearer $(tok)" -o /dev/null https://$R/cloud/stop
sleep 1
HTTP=$(curl -sk -m 90 -X PUT -H "Authorization: Bearer $(tok)" -H "Content-Type: application/json" \
        -d @"$MODEF" -o /tmp/mode_resp -w "%{http_code}" https://$R/cloud/mode)
echo "  mode HTTP $HTTP $(head -c 200 /tmp/mode_resp 2>/dev/null)"
[ "$HTTP" != "200" ] && exit 1
timeout $((SECS+20)) mosquitto_sub -h 10.117.229.18 -p 1883 -t 'fxr90-49/tevents' -W $((SECS+3)) > "$OUT" &
SUBPID=$!
sleep 2
HTTP=$(curl -sk -m 60 -X PUT -H "Authorization: Bearer $(tok)" -H "Content-Type: application/json" \
        -d "$STARTBODY" -o /tmp/start_resp -w "%{http_code}" https://$R/cloud/start)
echo "  start HTTP $HTTP $(head -c 200 /tmp/start_resp 2>/dev/null)  body=$STARTBODY"
sleep $SECS
curl -sk -m 40 -X PUT -H "Authorization: Bearer $(tok)" -o /dev/null https://$R/cloud/stop
wait $SUBPID 2>/dev/null
echo "  events: $(wc -l < "$OUT")"
