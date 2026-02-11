# ==========================================
# Stage 1: Build the React Frontend (Node.js)
# ==========================================
FROM node:18-alpine as build-step
WORKDIR /app-frontend

# 1. Install dependencies first (better caching)
COPY ./frontend/package.json ./frontend/package-lock.json ./
RUN npm install

# 2. Copy the rest of the source code
COPY ./frontend ./

# 3. Build the static files (Creates /dist folder)
RUN npm run build


# ==========================================
# Stage 2: Build the Python Backend (Flask)
# ==========================================
FROM python:3.9-slim

WORKDIR /app

# 1. Install system dependencies (needed for some python tools)
RUN apt-get update && apt-get install -y gcc

# 2. Install Python dependencies
COPY ./backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 3. Copy Backend Code
COPY ./backend ./

# 4. CRITICAL: Copy React Build from Stage 1 to Flask's static folder
# We rename 'dist' to 'static_react' so Flask doesn't get confused
COPY --from=build-step /app-frontend/dist ./static_react

# 5. Set Environment Variables
ENV FLASK_ENV=production

# 6. Expose the port
EXPOSE 10000

# 7. Run Gunicorn (Production Server)
# We tell it to run 'app:app'
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]