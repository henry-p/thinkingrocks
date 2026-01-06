# OpenPanel (Self-Hosted, Cookie-Free) Implementation Plan

## Goal
Deploy OpenPanel on your VPS and embed it in this Astro site with **no cookies**, **no user identification**, and **no persistent browser storage**.

---

## 1) Verify Server Setup (VPS)
- Confirm OpenPanel is reachable over HTTPS at a stable domain (e.g., `https://analytics.example.com`).
- Ensure TLS is active and auto-renewing (Let’s Encrypt or equivalent).
- Confirm the OpenPanel dashboard is accessible and project is created.

---

## 2) Configure OpenPanel for Cookie-Free, Anonymous Tracking
- In OpenPanel settings, **disable user identification** features (no `identify()` calls).
- Avoid storing any PII in event properties (no emails, IDs, usernames, etc.).
- If there’s a setting for **IP anonymization** or **truncation**, enable it.
- Keep retention minimal (only what you need for analytics).

> If OpenPanel exposes a “cookieless” or “privacy” toggle, enable it and confirm in docs for your version.

---

## 3) Tracking Snippet (Site Integration)
- Use the **script tag** embed from OpenPanel for the web SDK.
- Ensure the snippet does **not** call `identify()`.
- Confirm `trackAttributes`, `trackOutgoingLinks`, etc. do **not** include personal data.

Example structure (replace `CLIENT_ID` and API URL):

```html
<script>
  window.op = window.op || function () { (window.op.q = window.op.q || []).push(arguments); };
  window.op('init', {
    clientId: 'YOUR_CLIENT_ID',
    apiUrl: 'https://analytics.example.com/api/op',
    trackScreenViews: true,
    trackOutgoingLinks: true,
    trackAttributes: true
  });
</script>
<script async src="https://analytics.example.com/api/op/op1.js"></script>
```

---

## 4) Validate “No Cookies / No Storage”
- Use browser devtools (Application tab) to confirm **no cookies** are set.
- Verify **no localStorage or sessionStorage** keys are created.
- If storage is present, check OpenPanel config or SDK flags to disable it.

---

## 5) Privacy Policy Update
- Update site privacy policy to mention:
  - Self-hosted analytics
  - No cookies used
  - No personal data collected
  - Data retention window
  - VPS location (country)

---

## 6) Deploy & Verify
- Deploy the site with the OpenPanel snippet.
- Check OpenPanel dashboard for page views/events.
- Confirm ad blockers don’t fully block events (optional: use proxy endpoint if needed).

---

## 7) Ongoing Monitoring
- Periodically audit tracking properties.
- Re-verify cookies/storage after SDK updates.
- Keep OpenPanel version updated.

---

## Acceptance Checklist
- [ ] OpenPanel served over HTTPS from your VPS
- [ ] No cookies or browser storage created
- [ ] No `identify()` calls or PII tracked
- [ ] Privacy policy updated
- [ ] Events visible in OpenPanel dashboard
