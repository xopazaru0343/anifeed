"""
Generate API reference documentation for MkDocs.

This script automatically creates markdown files for each Python module
in the anifeed package, enabling mkdocstrings to generate API documentation.
"""
from pathlib import Path
import mkdocs_gen_files

# Configuration
PACKAGE_NAME = "anifeed"
SOURCE_DIR = Path("src") / PACKAGE_NAME
DOCS_DIR = Path("reference")

# For generating navigation
nav_items = []


def generate_module_docs():
    """Generate documentation pages for all Python modules."""
    for python_file in sorted(SOURCE_DIR.rglob("*.py")):
        # Skip __init__.py files
        if python_file.name == "__init__.py":
            continue

        # Calculate module path relative to package root
        relative_path = python_file.relative_to(SOURCE_DIR).with_suffix("")

        # Create corresponding documentation file path
        doc_file = DOCS_DIR / relative_path.with_suffix(".md")

        # Generate markdown file with mkdocstrings directive
        with mkdocs_gen_files.open(doc_file, "w") as f:
            # Build full module identifier (e.g., "anifeed.services.anime_service")
            module_identifier = f"{PACKAGE_NAME}.{'.'.join(relative_path.parts)}"
            f.write(f"::: {module_identifier}\n")

        # Link generated doc to source file for "Edit on GitHub" functionality
        mkdocs_gen_files.set_edit_path(doc_file, python_file)

        # Store for navigation generation
        nav_items.append((relative_path.parts, doc_file))


def generate_navigation():
    """Generate index.md and navigation for reference section."""
    
    # Create reference/index.md as landing page
    with mkdocs_gen_files.open(DOCS_DIR / "index.md", "w") as index_file:
        index_file.write("# API Reference\n\n")
        index_file.write("Complete API documentation for the AniFeed package.\n\n")
    
    # Organize modules by category
    categories = {}
    core_modules = []
    
    for parts, doc_path in nav_items:
        if len(parts) > 1:
            # Module in a subdirectory (e.g., services/anime_service.py)
            category = parts[0]
            if category not in categories:
                categories[category] = []
            module_name = parts[-1].replace("_", " ").title()
            categories[category].append((module_name, doc_path))
        else:
            # Top-level module (e.g., exceptions.py, main.py)
            module_name = parts[0].replace("_", " ").title()
            core_modules.append((module_name, doc_path))
    
    # Generate SUMMARY.md for literate-nav
    with mkdocs_gen_files.open(DOCS_DIR / "SUMMARY.md", "w") as nav_file:
        # Write Core section first if there are core modules
        if core_modules:
            nav_file.write("* Core\n")
            for module_name, doc_path in sorted(core_modules):
                nav_file.write(f"    * [{module_name}]({doc_path.name})\n")
        
        # Write categorized modules
        for category in sorted(categories.keys()):
            nav_file.write(f"* {category.replace('_', ' ').title()}\n")
            for module_name, doc_path in sorted(categories[category]):
                relative = str(doc_path.relative_to(DOCS_DIR))
                nav_file.write(f"    * [{module_name}]({relative})\n")


# Execute both functions
generate_module_docs()
generate_navigation()
