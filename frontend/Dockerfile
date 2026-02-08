# Multi-stage build for the Next.js frontend
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Copy the rest of the application
COPY . .

# Build the Next.js app
RUN npm install
RUN npm run build

# Production stage
FROM node:18-alpine AS runner

WORKDIR /app

# Copy necessary files from builder stage
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules

# Install only production dependencies
RUN npm ci --only=production

EXPOSE 3000

# Add a non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001
USER nextjs

CMD ["npx", "next", "start", "-H", "0.0.0.0", "-p", "3000"]