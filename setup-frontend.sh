#!/bin/bash

# Setup script for Next.js frontend

echo "🚀 Setting up Trading Research Agent Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js version: $(node --version)"

# Create Next.js app with TypeScript and Tailwind
echo "📦 Creating Next.js app..."
npx create-next-app@latest frontend \
  --typescript \
  --tailwind \
  --app \
  --no-src-dir \
  --import-alias "@/*" \
  --use-npm

cd frontend

# Install additional dependencies
echo "📦 Installing additional dependencies..."
npm install \
  @radix-ui/react-dialog \
  @radix-ui/react-dropdown-menu \
  @radix-ui/react-tabs \
  @radix-ui/react-toast \
  @radix-ui/react-select \
  @radix-ui/react-progress \
  class-variance-authority \
  clsx \
  tailwind-merge \
  lucide-react \
  recharts \
  framer-motion \
  react-markdown \
  remark-gfm

echo "✅ Frontend setup complete!"
echo ""
echo "To start the development server:"
echo "  cd frontend"
echo "  npm run dev"

