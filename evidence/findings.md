# Sanitized Evidence Register

The raw lab evidence contains deliberately seeded credentials and training values. This public register preserves the proof while redacting values that do not add technical value.

| Challenge | Evidence captured | Result |
|---:|---|---|
| 1 | Logcat entry from `diva-log` | Submitted card value appeared in application logs |
| 2 | Decompiled Java comparison | Embedded vendor key accepted by the UI |
| 3 | SharedPreferences XML | Username and password stored as plaintext strings |
| 4 | SQLite query against `myuser` | Plaintext credential row recovered |
| 5 | Read of app data file | Plaintext credential pair recovered |
| 6 | Read of `/sdcard/.uinfo.txt` | Sensitive record recovered from shared storage |
| 7 | Search input `' OR '1'='1' -- ` | All three seeded user records returned |
| 8 | `data:text/html,...` URI | WebView rendered supplied HTML |
| 9 | External `VIEW_CREDS` activity action | API credential screen opened |
| 10 | External `VIEW_CREDS2` action with `check_pin=false` | PIN flow bypassed |
| 11 | Query of exported notes provider | All six private notes returned |
| 12 | Native strings plus Frida JNI observation | Extracted value accepted; native method returned `1` |

## Representative Runtime Output

```text
[+] Hook loaded. Enter the native secret and tap the DIVA button.
[+] DivaJni.access candidate: [REDACTED TRAINING VALUE]
[+] DivaJni.access return value: 1
```

