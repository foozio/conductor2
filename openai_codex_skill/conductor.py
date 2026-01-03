"""
OpenAI Codex Conductor Skill

A Python implementation of the Conductor skill system using OpenAI's API,
providing context-driven development similar to the Claude/OpenCode/Gemini versions.
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import openai
from openai import OpenAI

class OpenAICodexConductor:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.project_root = Path.cwd()
        self.conductor_dir = self.project_root / "conductor"
        
    def setup(self) -> None:
        """Initialize the Conductor environment for a new project."""
        print("Welcome to OpenAI Codex Conductor!")
        print("Setting up context-driven development...")
        
        # Check if already initialized
        setup_state_file = self.conductor_dir / "setup_state.json"
        if setup_state_file.exists():
            with open(setup_state_file) as f:
                state = json.load(f)
            last_step = state.get("last_successful_step", "")
            if last_step == "3.3_initial_track_generated":
                print("Project already initialized. You can create new tracks or start implementing.")
                return
        
        # Create conductor directory
        self.conductor_dir.mkdir(exist_ok=True)
        
        # Initialize state
        self._write_setup_state("")
        
        # Determine project type
        project_type = self._detect_project_type()
        
        if project_type == "greenfield":
            self._setup_greenfield()
        else:
            self._setup_brownfield()
    
    def _detect_project_type(self) -> str:
        """Detect if this is a new or existing project."""
        indicators = [
            self.project_root / ".git",
            self.project_root / "package.json",
            self.project_root / "requirements.txt",
            self.project_root / "go.mod",
            self.project_root / "src",
            self.project_root / "app",
            self.project_root / "lib"
        ]
        
        has_indicators = any(indicator.exists() for indicator in indicators)
        
        if has_indicators:
            return "brownfield"
        else:
            return "greenfield"
    
    def _setup_greenfield(self) -> None:
        """Setup for new projects."""
        print("Detected new project. Let's define your vision!")
        
        # Ask for initial concept
        concept = input("What do you want to build? ")
        
        # Write initial concept
        product_file = self.conductor_dir / "product.md"
        with open(product_file, "w") as f:
            f.write(f"# Initial Concept\n\n{concept}\n")
        
        self._write_setup_state("")
        
        # Generate product guide
        self._generate_product_guide()
        
        # Generate guidelines
        self._generate_product_guidelines()
        
        # Generate tech stack
        self._generate_tech_stack()
        
        # Copy style guides and workflow
        self._copy_templates()
        
        # Generate initial track
        self._generate_initial_track()
    
    def _setup_brownfield(self) -> None:
        """Setup for existing projects."""
        print("Detected existing project.")
        
        # Analyze codebase
        analysis = self._analyze_codebase()
        print(f"Analysis complete. Detected: {analysis}")
        
        # Generate context based on analysis
        self._generate_context_from_analysis(analysis)
        
        # Copy templates
        self._copy_templates()
        
        # Generate initial track
        self._generate_initial_track()
    
    def _analyze_codebase(self) -> Dict[str, Any]:
        """Analyze existing codebase to infer context."""
        analysis = {
            "languages": [],
            "frameworks": [],
            "purpose": "",
            "architecture": ""
        }
        
        # Read README
        readme_file = self.project_root / "README.md"
        if readme_file.exists():
            with open(readme_file) as f:
                content = f.read()
            analysis["purpose"] = self._extract_purpose_from_readme(content)
        
        # Check package.json
        package_file = self.project_root / "package.json"
        if package_file.exists():
            with open(package_file) as f:
                package_data = json.load(f)
            analysis["languages"].append("javascript")
            if "dependencies" in package_data:
                deps = list(package_data["dependencies"].keys())
                analysis["frameworks"].extend(deps[:5])  # Top 5 deps
        
        # Check requirements.txt
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            with open(req_file) as f:
                deps = f.read().splitlines()
            analysis["languages"].append("python")
            analysis["frameworks"].extend(deps[:5])
        
        return analysis
    
    def _extract_purpose_from_readme(self, content: str) -> str:
        """Extract project purpose from README."""
        prompt = f"Based on this README content, summarize the project's main purpose in one sentence:\n\n{content[:1000]}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_product_guide(self) -> None:
        """Generate product.md using OpenAI."""
        print("Generating product guide...")
        
        # Read existing content
        product_file = self.conductor_dir / "product.md"
        existing_content = ""
        if product_file.exists():
            with open(product_file) as f:
                existing_content = f.read()
        
        prompt = f"""Based on the following initial concept, generate a comprehensive product guide for the project.
Include sections for target users, key features, goals, and success metrics.

Initial Concept:
{existing_content}

Generate the full product.md content:"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )
        
        content = response.choices[0].message.content.strip()
        
        with open(product_file, "w") as f:
            f.write(content)
        
        self._write_setup_state("2.1_product_guide")
        print("Product guide created.")
    
    def _generate_product_guidelines(self) -> None:
        """Generate product-guidelines.md."""
        print("Generating product guidelines...")
        
        prompt = """Generate comprehensive product guidelines including:
- Prose style and tone
- Brand messaging
- Visual identity guidelines
- User experience principles

Make it specific and actionable."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        
        content = response.choices[0].message.content.strip()
        
        guidelines_file = self.conductor_dir / "product-guidelines.md"
        with open(guidelines_file, "w") as f:
            f.write(content)
        
        self._write_setup_state("2.2_product_guidelines")
        print("Product guidelines created.")
    
    def _generate_tech_stack(self) -> None:
        """Generate tech-stack.md."""
        print("Generating tech stack...")
        
        # Read product info
        product_file = self.conductor_dir / "product.md"
        product_content = ""
        if product_file.exists():
            with open(product_file) as f:
                product_content = f.read()
        
        prompt = f"""Based on this product description, recommend a technology stack.
Include programming languages, frameworks, databases, and deployment options.

Product Description:
{product_content[:500]}

Generate the tech-stack.md content:"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )
        
        content = response.choices[0].message.content.strip()
        
        tech_file = self.conductor_dir / "tech-stack.md"
        with open(tech_file, "w") as f:
            f.write(content)
        
        self._write_setup_state("2.3_tech_stack")
        print("Tech stack defined.")
    
    def _copy_templates(self) -> None:
        """Copy style guides and workflow templates."""
        print("Setting up code style guides and workflow...")
        
        # Read tech stack to determine languages
        tech_file = self.conductor_dir / "tech-stack.md"
        languages = ["python", "javascript"]  # Default
        
        if tech_file.exists():
            with open(tech_file) as f:
                content = f.read()
            if "python" in content.lower():
                languages = ["python"]
            elif "javascript" in content.lower() or "typescript" in content.lower():
                languages = ["javascript"]
        
        # Create style guides directory
        style_dir = self.conductor_dir / "code_styleguides"
        style_dir.mkdir(exist_ok=True)
        
        # Copy general style guide
        general_content = """# General Code Style Guide

## Readability
- Use clear, descriptive variable and function names
- Add comments for complex logic
- Keep functions short and focused

## Consistency
- Follow language-specific conventions
- Use consistent indentation
- Maintain consistent naming patterns

## Best Practices
- Write self-documenting code
- Avoid magic numbers
- Handle errors appropriately
"""
        
        with open(style_dir / "general.md", "w") as f:
            f.write(general_content)
        
        # Copy language-specific guides
        for lang in languages:
            lang_content = f"""# {lang.title()} Code Style Guide

## Language-Specific Rules
- Follow {lang} best practices
- Use appropriate data structures
- Write efficient algorithms

## Project Conventions
- Consistent with general guidelines
- Adapted for {lang} idioms
- Team-approved patterns
"""
            with open(style_dir / f"{lang}.md", "w") as f:
                f.write(lang_content)
        
        # Create workflow
        workflow_content = """# Development Workflow

## Test-Driven Development
- Write tests before implementing features
- Target >80% code coverage
- Run tests after each change

## Commit Strategy
- Commit after each completed task
- Use descriptive commit messages
- Attach task summaries as git notes

## Quality Gates
- Code review for all changes
- Automated testing required
- Manual verification for phases

## Phase Completion
- Manual user verification required
- Gap analysis against specifications
- Documentation updates
"""
        
        workflow_file = self.conductor_dir / "workflow.md"
        with open(workflow_file, "w") as f:
            f.write(workflow_content)
        
        self._write_setup_state("2.5_workflow")
        print("Templates copied.")
    
    def _generate_initial_track(self) -> None:
        """Generate the first track."""
        print("Creating initial track...")
        
        # Read product info
        product_file = self.conductor_dir / "product.md"
        product_content = ""
        if product_file.exists():
            with open(product_file) as f:
                product_content = f.read()
        
        # Generate track description
        prompt = f"""Based on this product description, suggest an initial track (feature) to start development with.
Provide a brief description of what this track should accomplish.

Product:
{product_content[:500]}

Suggest one initial track:"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        
        track_desc = response.choices[0].message.content.strip()
        
        # Create track ID
        track_id = f"initial_{datetime.date.today().strftime('%Y%m%d')}"
        
        # Create tracks directory
        tracks_dir = self.conductor_dir / "tracks" / track_id
        tracks_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate spec
        spec_prompt = f"""Generate a detailed specification for this track:

Track: {track_desc}

Include:
- Requirements
- Acceptance criteria
- Technical considerations

Make it comprehensive but focused."""
        
        spec_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": spec_prompt}],
            max_tokens=600
        )
        
        spec_content = spec_response.choices[0].message.content.strip()
        
        # Generate plan
        plan_prompt = f"""Create a phased implementation plan for this track:

Track: {track_desc}
Spec: {spec_content[:300]}

Structure as a markdown checklist with phases and tasks.
Follow TDD principles.
Include phase completion verification tasks."""
        
        plan_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": plan_prompt}],
            max_tokens=800
        )
        
        plan_content = plan_response.choices[0].message.content.strip()
        
        # Write files
        with open(tracks_dir / "spec.md", "w") as f:
            f.write(f"# Track Specification: {track_desc}\n\n{spec_content}")
        
        with open(tracks_dir / "plan.md", "w") as f:
            f.write(f"# Implementation Plan: {track_desc}\n\n{plan_content}")
        
        # Create metadata
        metadata = {
            "track_id": track_id,
            "type": "feature",
            "status": "new",
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "description": track_desc
        }
        
        with open(tracks_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Update tracks.md
        tracks_file = self.conductor_dir / "tracks.md"
        tracks_content = f"""# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.

---

## [ ] Track: {track_desc}
*Link: [./conductor/tracks/{track_id}/](./conductor/tracks/{track_id}/)*
"""
        
        with open(tracks_file, "w") as f:
            f.write(tracks_content)
        
        self._write_setup_state("3.3_initial_track_generated")
        print(f"Initial track '{track_desc}' created with ID: {track_id}")
    
    def _generate_context_from_analysis(self, analysis: Dict[str, Any]) -> None:
        """Generate context files from codebase analysis."""
        # Generate product.md from analysis
        product_content = f"""# Product Description

## Purpose
{analysis['purpose']}

## Technology Stack
- Languages: {', '.join(analysis['languages'])}
- Frameworks: {', '.join(analysis['frameworks'][:3])}

## Architecture
{analysis['architecture']}
"""
        
        with open(self.conductor_dir / "product.md", "w") as f:
            f.write(product_content)
        
        # Generate minimal guidelines and tech stack
        guidelines_content = """# Product Guidelines

## Development Principles
- Maintain code quality
- Follow existing patterns
- Document changes appropriately
"""
        
        with open(self.conductor_dir / "product-guidelines.md", "w") as f:
            f.write(guidelines_content)
        
        tech_content = f"""# Technology Stack

## Languages
{chr(10).join(f'- {lang}' for lang in analysis['languages'])}

## Frameworks
{chr(10).join(f'- {fw}' for fw in analysis['frameworks'])}
"""
        
        with open(self.conductor_dir / "tech-stack.md", "w") as f:
            f.write(tech_content)
    
    def _write_setup_state(self, step: str) -> None:
        """Write the current setup state."""
        state_file = self.conductor_dir / "setup_state.json"
        state = {"last_successful_step": step}
        with open(state_file, "w") as f:
            json.dump(state, f)
    
    def new_track(self, description: str) -> None:
        """Create a new track."""
        print(f"Creating new track: {description}")
        
        # Generate track ID
        track_id = f"{description.replace(' ', '_').lower()}_{datetime.date.today().strftime('%Y%m%d')}"
        
        # Create directory
        tracks_dir = self.conductor_dir / "tracks" / track_id
        tracks_dir.mkdir(parents=True, exist_ok=True)
        
        # Read context files
        context = self._read_context_files()
        
        # Generate spec
        spec_prompt = f"""Generate a detailed specification for this new track.

Track Description: {description}

Context:
Product: {context['product'][:300]}
Tech Stack: {context['tech'][:200]}

Include requirements, acceptance criteria, and technical details."""
        
        spec_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": spec_prompt}],
            max_tokens=600
        )
        
        spec_content = spec_response.choices[0].message.content.strip()
        
        # Generate plan
        plan_prompt = f"""Create an implementation plan for this track.

Track: {description}
Spec: {spec_content[:400]}

Structure with phases and tasks following TDD principles."""
        
        plan_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": plan_prompt}],
            max_tokens=800
        )
        
        plan_content = plan_response.choices[0].message.content.strip()
        
        # Write files
        with open(tracks_dir / "spec.md", "w") as f:
            f.write(f"# Specification: {description}\n\n{spec_content}")
        
        with open(tracks_dir / "plan.md", "w") as f:
            f.write(f"# Plan: {description}\n\n{plan_content}")
        
        # Metadata
        metadata = {
            "track_id": track_id,
            "type": "feature",
            "status": "new",
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "description": description
        }
        
        with open(tracks_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Update tracks.md
        tracks_file = self.conductor_dir / "tracks.md"
        if tracks_file.exists():
            with open(tracks_file, "a") as f:
                f.write(f"\n## [ ] Track: {description}\n*Link: [./conductor/tracks/{track_id}/](./conductor/tracks/{track_id}/)*\n")
        else:
            with open(tracks_file, "w") as f:
                f.write(f"""# Project Tracks

## [ ] Track: {description}
*Link: [./conductor/tracks/{track_id}/](./conductor/tracks/{track_id}/)*
""")
        
        print(f"New track created: {track_id}")
    
    def implement(self, track_id: Optional[str] = None) -> None:
        """Implement the current track or specified track."""
        if not track_id:
            track_id = self._get_current_track()
        
        if not track_id:
            print("No active track found. Create a new track first.")
            return
        
        print(f"Implementing track: {track_id}")
        
        tracks_dir = self.conductor_dir / "tracks" / track_id
        plan_file = tracks_dir / "plan.md"
        
        if not plan_file.exists():
            print("Plan file not found.")
            return
        
        # Read plan
        with open(plan_file) as f:
            plan_content = f.read()
        
        print("Current plan:")
        print(plan_content)
        
        # Find next pending task
        lines = plan_content.split('\n')
        next_task = None
        task_line_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('[ ]'):
                next_task = line.strip()[3:].strip()
                task_line_index = i
                break
        
        if not next_task or task_line_index == -1:
            print("No pending tasks found.")
            return
        
        print(f"Next task: {next_task}")
        
        # Execute task using OpenAI
        self._execute_task(track_id, next_task, task_line_index)
    
    def _get_current_track(self) -> Optional[str]:
        """Get the current active track."""
        tracks_dir = self.conductor_dir / "tracks"
        if not tracks_dir.exists():
            return None
        
        # Find tracks with status "in_progress" or first "new" track
        for track_dir in tracks_dir.iterdir():
            if track_dir.is_dir():
                metadata_file = track_dir / "metadata.json"
                if metadata_file.exists():
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                    if metadata.get("status") in ["new", "in_progress"]:
                        return track_dir.name
        
        return None
    
    def _execute_task(self, track_id: str, task: str, line_index: int) -> None:
        """Execute a task using OpenAI."""
        print(f"Executing: {task}")
        
        # Read context
        context = self._read_context_files()
        spec_content = self._read_track_file(track_id, "spec.md")
        
        # Generate implementation
        prompt = f"""Implement this task for the project.

Task: {task}

Context:
Product: {context['product'][:300]}
Tech Stack: {context['tech'][:200]}
Spec: {spec_content[:400]}

Provide the code changes needed. Focus on the specific task."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        implementation = response.choices[0].message.content.strip()
        
        print("Suggested implementation:")
        print(implementation)
        
        # Ask user to apply changes
        apply = input("Apply these changes? (y/n): ")
        if apply.lower() == 'y':
            # Here we would apply the changes, but for now just mark as complete
            self._mark_task_complete(track_id, line_index)
            print("Task marked as complete.")
        else:
            print("Task not applied.")
    
    def _read_context_files(self) -> Dict[str, str]:
        """Read context files."""
        context = {}
        
        for filename in ["product.md", "tech-stack.md", "workflow.md"]:
            file_path = self.conductor_dir / filename
            if file_path.exists():
                with open(file_path) as f:
                    context[filename.split('.')[0]] = f.read()
            else:
                context[filename.split('.')[0]] = ""
        
        return context
    
    def _read_track_file(self, track_id: str, filename: str) -> str:
        """Read a track file."""
        file_path = self.conductor_dir / "tracks" / track_id / filename
        if file_path.exists():
            with open(file_path) as f:
                return f.read()
        return ""
    
    def _mark_task_complete(self, track_id: str, line_index: int) -> None:
        """Mark a task as complete in the plan."""
        plan_file = self.conductor_dir / "tracks" / track_id / "plan.md"
        
        with open(plan_file) as f:
            lines = f.readlines()
        
        if line_index < len(lines):
            lines[line_index] = lines[line_index].replace('[ ]', '[x]')
        
        with open(plan_file, "w") as f:
            f.writelines(lines)
        
        # Update metadata
        metadata_file = self.conductor_dir / "tracks" / track_id / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)
            metadata["status"] = "in_progress"
            metadata["updated_at"] = datetime.datetime.now().isoformat()
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)
    
    def status(self) -> None:
        """Show project status."""
        tracks_file = self.conductor_dir / "tracks.md"
        if tracks_file.exists():
            with open(tracks_file) as f:
                print(f.read())
        else:
            print("No tracks found. Run setup first.")
    
    def revert(self, track_id: Optional[str] = None, target: str = "track") -> None:
        """Revert changes using git-aware rollback."""
        print(f"Reverting {target} for track: {track_id or 'current'}")
        
        # For now, provide guidance on manual revert
        print("Revert functionality uses git to rollback changes.")
        print("To revert a complete track:")
        print("1. Find the commits for the track using: git log --oneline")
        print("2. Use: git reset --hard <commit-before-track>")
        print("3. Or: git revert <commit-range>")
        print("\nFor safety, create a backup branch first:")
        print("git branch backup-before-revert")
        
        # Could implement automated git operations here
        print("\nAutomated revert not yet implemented. Please use git commands manually.")