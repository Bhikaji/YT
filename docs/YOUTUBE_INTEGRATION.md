# Autonomous AI Cartoon Studio
## YouTube Data API v3 Integration, OAuth2 & Monetization Compliance

---

## 1. YouTube Data API v3 Architecture

The YouTube integration module (`modules/youtube_engine/`) manages video publication, playlist distribution, and analytics scraping via Google's official API:

```
[Completed & Audited Episode]
              │
              ├──> 1. Duplicate Upload Prevention (SHA-256 Hash Check in DB)
              ├──> 2. Preflight Monetization & COPPA Audit
              ├──> 3. YouTube API Quota Check (< 8,400 units used today)
              ├──> 4. Resumable Chunked Video Upload (POST /upload/youtube/v3/videos)
              ├──> 5. Custom Thumbnail Upload (POST /youtube/v3/thumbnails/set)
              ├──> 6. Automated Playlist Insertion (POST /youtube/v3/playlistItems)
              └──> 7. Record Video ID & Schedule Live Release
```

---

## 2. OAuth2 Authentication & Credential Storage

- **Client Configuration:** Stored in `credentials/client_secret.json` (git-ignored).
- **Authorized Token:** Stored in `credentials/youtube_token.json` (git-ignored) with automated refresh token rotation.
- **Safety Switch:** Video publishing remains strictly disabled until the creator explicitly completes channel authorization and configures the publishing mode (`MANUAL_APPROVAL` vs `FULLY_AUTONOMOUS`).

---

## 3. Daily Quota Management & Rate Limiting

The YouTube Data API free tier provides **10,000 quota units per day**:
- **Video Upload:** Costs **1,600 units**.
- **Thumbnail Set:** Costs **50 units**.
- **Playlist Insert:** Costs **50 units**.
- **Metadata Update:** Costs **50 units**.
- **Total Cost per Uploaded Episode:** **~1,750 units**.

**Maximum Safe Daily Uploads:** Up to **4 videos per day** without exceeding the 10,000-unit ceiling. The scheduler enforces an automated pause if daily quota consumption exceeds 8,500 units.

---

## 4. COPPA & Monetization Compliance Rules

In strict compliance with YouTube Partner Program (YPP) guidelines and FTC COPPA regulations:
1. **Audience Classification:** Content directed primarily at children under 13 is strictly declared as `madeForKids = true`. The system **never** misclassifies children's content to enable comments or higher ad revenue.
2. **Synthetic / AI Content Disclosure:** If required by current YouTube policies for realistic depictions, automated metadata includes the appropriate synthetic media disclosure tags.
3. **Advertiser Suitability:** Titles and descriptions are audited against the YouTube Advertiser-Friendly Content Guidelines before publication.
