#!/bin/bash
# Make all demo scripts executable

chmod +x demo-scripts/*.sh

echo "✅ All demo scripts are now executable!"
echo ""
echo "Available demo scripts:"
ls -la demo-scripts/*.sh
echo ""
echo "To run demos with Docker:"
echo "  ./demo-scripts/demo-3-a2a.sh"
echo "  ./demo-scripts/demo-4-mcp.sh"
echo ""
echo "To test locally without Docker:"
echo "  ./demo-scripts/test-a2a-local.sh"
echo "  ./demo-scripts/test-mcp-local.sh"
