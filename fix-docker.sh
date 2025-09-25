#!/bin/bash
# Quick fix for Docker issues

echo "🔧 Docker Connection Fix"
echo "========================"
echo ""

# Make scripts executable
chmod +x demo-scripts/*.sh

echo "1. Checking Docker status..."
if docker ps &> /dev/null; then
    echo "✅ Docker is running"
else
    echo "❌ Docker is not responding"
    echo ""
    echo "Please try:"
    echo "  1. Restart Docker Desktop"
    echo "  2. Check Docker Desktop settings"
    echo "  3. Run: docker system prune -a (to clean up)"
    exit 1
fi

echo ""
echo "2. Testing Docker Hub connection..."
if docker pull hello-world &> /dev/null; then
    echo "✅ Docker Hub connection OK"
    docker rmi hello-world &> /dev/null
else
    echo "⚠️ Docker Hub connection issues detected"
    echo ""
    echo "Possible fixes:"
    echo "  1. Check internet connection"
    echo "  2. Try: docker logout && docker login"
    echo "  3. Check if behind proxy/firewall"
    echo "  4. Try alternative registry mirrors"
fi

echo ""
echo "3. Available options:"
echo "----------------------"
echo ""
echo "Option A: Run demos locally without Docker (RECOMMENDED FOR NOW)"
echo "  ./demo-scripts/run-local-demos.sh"
echo ""
echo "Option B: Try minimal Docker setup with alternative images"
echo "  ./demo-scripts/start-minimal.sh"
echo ""
echo "Option C: Retry with original images (with retry logic)"
echo "  ./demo-scripts/start-all-retry.sh"
echo ""
echo "For your presentation, Option A (local demos) will work perfectly"
echo "and doesn't require Docker at all!"
