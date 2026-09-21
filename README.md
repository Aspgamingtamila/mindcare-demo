# MindCare local demo

The page can still be opened directly for an offline UI-only demo. To use the
SQLite database and working browser interaction together, start the local
server from this folder:

```powershell
python server.py
```

Then open [http://localhost:8000](http://localhost:8000) in Chrome or Edge.

The first run creates `mindcare-demo.db`. The page saves check-ins, history,
and the demo counselor queue to that local SQLite file.

## Deploy from GitHub with SQLite

GitHub stores this code, but it cannot run the Python server or SQLite itself.
This project includes `Dockerfile` and `render.yaml` to deploy it from a GitHub
repository to Render. The Render service hosts both the website and the SQLite
API; its attached disk keeps `mindcare-demo.db` after redeploys.

1. Create an empty GitHub repository and push this folder to it.
2. In Render, choose **New** → **Blueprint** and select the repository.
3. Approve the `mindcare-demo` web service and its 1 GB `mindcare-data` disk.
4. Open the URL Render gives you.

The persistent disk requires a Render plan that supports disks. This is a
prototype: it has no authentication or production-grade privacy/security
controls, so do not use it for real health information.
