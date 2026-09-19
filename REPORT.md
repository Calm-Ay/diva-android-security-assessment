# DIVA Android Security Assessment Report

## Executive Summary

The assessment confirmed twelve intentionally insecure behaviors in DIVA across data storage, cryptography, input validation, and Android platform interaction. The most important pattern was misplaced trust in the client: secrets, authorization decisions, and sensitive records were accessible to an attacker who could inspect the APK, invoke exported components, or instrument the running process.

No production systems or third-party accounts were tested. All actions occurred inside an isolated Android lab.

## Methodology

Each exercise followed four steps:

1. Review decompiled Java, resources, the manifest, or native-library strings.
2. Form a testable hypothesis about the exposed data or control.
3. Confirm the behavior through the DIVA UI, ADB, Android component tooling, or Frida.
4. Save evidence and map the issue to practical remediation.

## Findings

### 1. Sensitive Data in Application Logs

The application wrote a submitted payment-card value to Logcat. Any actor with log access could recover the value.

**Fix:** Remove sensitive values from log statements, use structured redaction, and disable verbose diagnostic logging in release builds.

### 2. Java Hardcoded Secret

Static analysis found a plaintext vendor key in a Java comparison. The extracted value passed the application check.

**Fix:** Keep long-lived secrets and authorization decisions off the client. Use server-side validation and short-lived, scoped credentials.

### 3–6. Insecure Data Storage

Credentials were recovered from SharedPreferences XML, SQLite, an app-private plaintext file, and external storage. App-private permissions reduce routine cross-app access but do not make plaintext safe after backup exposure, root compromise, or device extraction. External storage introduced broader exposure.

**Fix:** Avoid persisting passwords. Minimize retention, keep necessary data in app-private storage, and protect sensitive values with Android Keystore-backed cryptography. Never place secrets on shared storage.

### 7. SQL Injection

A crafted search value altered the SQL predicate and returned all seeded records, including passwords and payment data.

**Fix:** Use parameterized queries or selection arguments, apply least-data responses, and avoid storing unnecessary sensitive records.

### 8. Unsafe URI Handling

The WebView accepted a `data:` URI and rendered attacker-supplied HTML because input was not restricted to trusted schemes and hosts.

**Fix:** Parse with `Uri`, allow only required HTTPS hosts, disable JavaScript unless necessary, and never expose privileged bridges to untrusted content.

### 9. Exported Credential Activity

An external caller invoked an exported activity through its implicit action and opened a screen containing API credentials.

**Fix:** Set sensitive components to non-exported. Where inter-app use is required, enforce signature permissions and authorize the caller inside the component.

### 10. Intent Extra Authorization Bypass

An external caller supplied `check_pin=false`, bypassing the normal PIN path and displaying third-party credentials.

**Fix:** Treat Intent extras as untrusted input. Perform authorization from trusted application state and enforce it in the receiving component.

### 11. Exported Notes ContentProvider

The PIN protected only the application UI. The exported provider allowed an unprivileged shell caller to query every private note directly.

**Fix:** Keep providers non-exported by default. If sharing is required, enforce a signature-level permission, validate callers, and restrict supported URIs and operations.

### 12. Native Hardcoded Secret

String extraction from the x86_64 native library exposed a candidate secret. The UI accepted it, and a Frida hook observed the plaintext argument reaching `DivaJni.access(String)` and the method returning `1`.

**Fix:** Native code raises reverse-engineering cost but does not provide secret storage. Move sensitive validation to a trusted server and design for client compromise.

## Frida Diagnostic and Resolution

The initial Frida 17.7.3 client/server pair could list processes but failed on attach. Android logs showed the server aborting during injection with `Unsupported Android linker`. Device architecture and client/server versions matched, and SELinux was already permissive.

An isolated Frida 16.6.6 Python environment and matching Android x86_64 server restored attach and Java-bridge functionality. The final hook recorded:

```text
DivaJni.access candidate: [REDACTED TRAINING VALUE]
DivaJni.access return value: 1
```

## Scope Limit

DIVA Challenge 13, which asks the tester to trigger and diagnose a native memory-corruption crash, was not completed during this assessment and is excluded from the result count.

