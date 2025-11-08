# Quake-of-the-Day (Make.com upload) — No Google Cloud billing

This builds a 9:16 Short from USGS public-domain data and **sends it to Make.com** to upload to YouTube (OAuth inside Make).

## One-time steps
1) Create a free account at make.com.
2) In Make, create a **Scenario** with 3 modules:
   - **Custom Webhook** (copy the URL)
   - **HTTP — Get a file** (map `download_url` from the webhook)
   - **YouTube — Upload a video** (sign in; map title/description/tags; file = output of HTTP step)
   Turn the scenario **ON**.
3) Create a public GitHub repo and upload this folder.
4) Add a repo **Secret**: `MAKE_WEBHOOK_URL` = the URL from step 2.
5) The workflow runs 3×/day by CRON, creates `work/video.mp4`, publishes a GitHub Release, then POSTs JSON `{download_url,title,description,tags}` to your Make webhook.

Attribution to include in your video description:
`Data: USGS Earthquake Hazards Program (Public Domain). Preliminary; subject to change.`
