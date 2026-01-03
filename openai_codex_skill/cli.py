#!/usr/bin/env python3
"""
OpenAI Codex Conductor CLI

Command-line interface for the OpenAI-powered Conductor skill.
"""

import argparse
import sys
from pathlib import Path

# Add the skill directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from conductor import OpenAICodexConductor

def main():
    parser = argparse.ArgumentParser(description="OpenAI Codex Conductor")
    parser.add_argument("--api-key", help="OpenAI API key")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model to use")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    subparsers.add_parser("setup", help="Initialize Conductor in the current project")
    
    # New track command
    new_track_parser = subparsers.add_parser("new-track", help="Create a new track")
    new_track_parser.add_argument("description", help="Track description")
    
    # Implement command
    implement_parser = subparsers.add_parser("implement", help="Implement the current track")
    implement_parser.add_argument("--track", help="Specific track ID to implement")
    
    # Status command
    subparsers.add_parser("status", help="Show project status")
    
    # Revert command
    revert_parser = subparsers.add_parser("revert", help="Revert changes")
    revert_parser.add_argument("--track", help="Track ID to revert")
    revert_parser.add_argument("--target", default="track", choices=["track", "phase", "task"], help="What to revert")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        conductor = OpenAICodexConductor(api_key=args.api_key, model=args.model)
        
        if args.command == "setup":
            conductor.setup()
        elif args.command == "new-track":
            conductor.new_track(args.description)
        elif args.command == "implement":
            conductor.implement(args.track)
        elif args.command == "status":
            conductor.status()
        elif args.command == "revert":
            conductor.revert(args.track, args.target)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()