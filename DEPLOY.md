# 🚀 Deploy Petit Panthère to Railway

## Quick Deploy (5 minutes)

1. **Push to GitHub:**
   ```bash
   cd "/Users/denisem/Desktop/Katarina's Projects/petit-panthere"
   git init
   git add .
   git commit -m "Initial commit - Petit Panthère"
   ```

   Create a new repo on GitHub, then:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/petit-panthere.git
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to: https://railway.com/new
   - Click "Deploy from GitHub repo"
   - Select `petit-panthere`
   - Railway will auto-detect Python and deploy!

3. **Add Environment Variable:**
   - In Railway dashboard → Variables
   - Add: `ANTHROPIC_API_KEY` = `your_api_key`
   - Redeploy

4. **Get Your URL:**
   - Railway will give you a URL like: `petit-panthere.up.railway.app`
   - Bookmark it on your phone!

## Alternative: Manual Deploy

If you don't want to use GitHub:

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Deploy:
   ```bash
   cd "/Users/denisem/Desktop/Katarina's Projects/petit-panthere"
   railway login
   railway init
   railway up
   ```

3. Add environment variable:
   ```bash
   railway variables --set "ANTHROPIC_API_KEY=your_key_here"
   ```

## After Deploy

Your Petit Panthère will be live at:
- `https://your-project.up.railway.app`

Memory will save to `/tmp/memory/` on Railway (ephemeral), but we can fix that later by connecting Railway to your Mac or using a database.

For Denver, the ephemeral storage is fine — you can copy memories over manually after the trip!
