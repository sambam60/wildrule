# Deployment Instructions

This application has two parts that need to be deployed separately:

1. **Frontend** (Static HTML) - Deploy to Vercel
2. **Backend** (Python WebSocket Server) - Deploy to Railway, Render, or Fly.io

## Frontend Deployment (Vercel)

The frontend is already deployed to Vercel. To configure it to connect to your backend:

### Option 1: Edit index.html

Edit `web/index.html` and set the `WS_SERVER_URL`:

```javascript
window.WS_SERVER_URL = "your-backend-domain.com";
```

Then commit and push.

### Option 2: Vercel Environment Variables (coming soon)

You can also use Vercel's environment variables with a serverless function to inject the URL.

## Backend Deployment

Choose one of the following platforms:

### Railway (Recommended)

1. Go to [railway.app](https://railway.app)
2. Create a new project
3. Connect your GitHub repository
4. Add a new service
5. Select "Python" as the runtime
6. Railway will auto-detect the app
7. Set the start command: `python server.py`
8. Expose the port (Railway will set PORT automatically)
9. Deploy!

### Render

1. Go to [render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python server.py`
5. Deploy!

### Fly.io

1. Install Fly CLI: `brew install flyctl`
2. Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "server.py"]
```

3. Run: `fly launch` and follow prompts

## After Deployment

1. Copy your backend URL (e.g., `wildrule-backend.railway.app`)
2. Edit `web/index.html` and set:
   ```javascript
   window.WS_SERVER_URL = "wildrule-backend.railway.app";
   ```
3. Commit and push
4. Your Vercel frontend will now connect to the deployed backend!

## Local Development

To run locally:

```bash
# Terminal 1: Start the server
python server.py

# Terminal 2: Serve the frontend
python -m http.server 3000 -d web

# Open http://localhost:3000
```

## Troubleshooting

- **404 errors**: Make sure the backend is deployed and running
- **Connection errors**: Check that your backend URL in `index.html` is correct
- **CORS issues**: The server already handles CORS for WebSocket connections
