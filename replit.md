# Surf Shooter Game

## Overview
A fun 2D beach-themed shooting game built with Python and Pygame. Players defend the beach by shooting water balloons at surfers riding the waves.

## Purpose
This is a Python Pygame game migrated to Replit for easy online access and publishing.

## Current State
- Game successfully converted to web-based version using Pygbag
- All dependencies installed (pygame 2.5.2, numpy 1.24.3, pygbag 0.9.2)
- Game runs in browser via WebAssembly
- Ready to publish as web application

## Project Structure
```
surf_shooter/
├── main.py                 # Main game logic
├── assets/
│   └── sprites/            # Game sprites (player, surfer, water balloon)
├── generate_sprites.py     # Sprite generation utility
├── requirements.txt        # Python dependencies
└── build/web/              # WebAssembly build output
server.py                   # HTTP server for web game
```

## Game Features
- Animated ocean waves with realistic motion
- Click to shoot water balloons at surfers
- Dynamic surfer movement following wave patterns
- Win condition when all surfers are hit
- Restart functionality

## How to Play
1. Click anywhere on the screen to shoot water balloons
2. Aim at the surfers riding the waves
3. Hit all surfers to clear the beach
4. Click "Restart" to play again

## Dependencies
- Python 3.11
- pygame==2.5.2
- numpy==1.24.3

## Recent Changes
- 2025-11-09: Initial migration to Replit
- Fixed type hints in load_image function
- Created main.py entry point for easy launching
- Converted game loop to async/await for WebAssembly compatibility
- Built web version using Pygbag (WebAssembly)
- Created server.py to serve the web game on port 5000
- Configured Autoscale deployment for web publishing
- Removed unnecessary stop_mansplaining folder
- Fixed CORS headers to use 'credentialless' policy for CDN resources

## Publishing
This game runs as a web application using WebAssembly. It can be accessed through any modern browser and is configured for Autoscale deployment on Replit. The game is served on port 5000 and is ready to publish.

## Technical Details
- **Web Server**: Python HTTP server (server.py) on port 5000
- **Build Tool**: Pygbag 0.9.2 for WebAssembly conversion
- **Deployment**: Autoscale deployment (scales with traffic)
- **Browser Compatibility**: Chrome, Firefox, Safari (iOS 15+)
- **Assets**: All sprites and game logic bundled in build/web/
