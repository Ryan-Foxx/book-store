# $ ---------- Base Stage ----------
FROM node:24.21.0-alpine3.24 AS base
WORKDIR /app
COPY package*.json package-lock.json ./

# $ ---------- Development Stage ----------
FROM base AS dev
ENV NODE_ENV=development
RUN npm ci
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# $ ---------- Production Stage ----------
FROM base AS prod
ENV NODE_ENV=production
RUN npm ci --only=production && npm cache clean --force
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["sh", "-c", "npm", "run", "start"]
