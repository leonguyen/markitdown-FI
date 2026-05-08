# MarkItDown FastAPI on Fly.io

Wrapper around Microsoft [MarkItDown](https://github.com/microsoft/markitdown) that exposes `/convert` as an HTTP API.

## How to deploy

1. Install flyctl:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. Clone / unpack this repo and `cd` into it.

3. Launch on Fly.io (interactive; pick an app name and region):
   ```bash
   flyctl launch --no-deploy
   ```

4. Deploy the container:
   ```bash
   flyctl deploy
   ```

5. Open the app:
   ```bash
   flyctl open
   ```

Then test with:

```bash
curl -X POST \
  -F "file=@sample.pdf" \
  https://your-app.fly.dev/convert
```
