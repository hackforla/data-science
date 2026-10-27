#!/usr/bin/env python3
"""
MASTER MONTHLY REFRESH SCRIPT

Runs the complete monthly refresh workflow in the correct order:
1. Collect new biographies from Wikipedia
2. Transform to notebook format
3. Re-run all analysis notebooks
4. Generate updated dashboard

Usage:
    python monthly_refresh.py

Options:
    python monthly_refresh.py --skip-notebooks  # Only run data collection
    python monthly_refresh.py --notebooks-only  # Only re-run notebooks
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Colors for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(step_num, total, message):
    """Print formatted step header."""
    print(f"\n{Colors.HEADER}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BOLD}STEP {step_num}/{total}: {message}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'='*70}{Colors.ENDC}\n")

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"{Colors.OKCYAN}▶ {description}{Colors.ENDC}")
    try:
        result = subprocess.run(cmd, check=True, shell=True, text=True)
        print(f"{Colors.OKGREEN}✓ Success{Colors.ENDC}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}✗ Failed with exit code {e.returncode}{Colors.ENDC}")
        return False

def main():
    start_time = datetime.now()
    
    # Parse arguments
    skip_notebooks = '--skip-notebooks' in sys.argv
    notebooks_only = '--notebooks-only' in sys.argv
    
    # Check paths
    ROOT = Path.cwd()
    if ROOT.name == "notebooks":
        ROOT = ROOT.parent
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║         WIKIPEDIA REPRESENTATION GAPS - MONTHLY REFRESH        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    print(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project root: {ROOT}")
    
    steps_completed = []
    steps_failed = []
    
    # ==========================================
    # STEP 1: Collect New Biographies
    # ==========================================
    if not notebooks_only:
        print_step(1, 5, "Collecting new biographies from Wikipedia")
        
        refresh_script = ROOT / "pipelines" / "refresh_step_1.py"
        if not refresh_script.exists():
            print(f"{Colors.FAIL}✗ Script not found: {refresh_script}{Colors.ENDC}")
            print(f"{Colors.WARNING}Place refresh_step_1.py in pipelines/ directory{Colors.ENDC}")
            sys.exit(1)
        
        if run_command(f"python {refresh_script}", "Running refresh_step_1.py"):
            steps_completed.append("Data collection")
        else:
            steps_failed.append("Data collection")
            print(f"\n{Colors.FAIL}Stopping due to error in data collection{Colors.ENDC}")
            sys.exit(1)
    
    # ==========================================
    # STEP 2: Transform to Notebook Format
    # ==========================================
    if not notebooks_only:
        print_step(2, 5, "Transforming data to notebook format")
        
        bootstrap_script = ROOT / "pipelines" / "bootstrap_to_original_artifacts.py"
        if not bootstrap_script.exists():
            print(f"{Colors.FAIL}✗ Script not found: {bootstrap_script}{Colors.ENDC}")
            print(f"{Colors.WARNING}Place bootstrap_to_original_artifacts.py in pipelines/ directory{Colors.ENDC}")
            sys.exit(1)
        
        if run_command(f"python {bootstrap_script}", "Running bootstrap_to_original_artifacts.py"):
            steps_completed.append("Data transformation")
        else:
            steps_failed.append("Data transformation")
            print(f"\n{Colors.FAIL}Stopping due to error in data transformation{Colors.ENDC}")
            sys.exit(1)
    
    if skip_notebooks:
        print(f"\n{Colors.WARNING}Skipping notebook execution (--skip-notebooks flag){Colors.ENDC}")
        print_summary(start_time, steps_completed, steps_failed)
        return
    
    # ==========================================
    # STEP 3: Re-run Analysis Notebooks
    # ==========================================
    print_step(3, 5, "Re-running analysis notebooks")
    
    notebooks_dir = ROOT / "notebooks"
    if not notebooks_dir.exists():
        print(f"{Colors.FAIL}✗ Notebooks directory not found: {notebooks_dir}{Colors.ENDC}")
        sys.exit(1)
    
    notebooks = [
        ("03_aggregate_and_qc.ipynb", "Aggregating and quality checking"),
        ("06_statistical_analysis.ipynb", "Running statistical analysis"),
        ("07_intersectional_analysis.ipynb", "Running intersectional analysis"),
        ("04_visualization.ipynb", "Generating visualizations"),
        ("05_dashboard.ipynb", "Building dashboard")
    ]
    
    for nb_file, description in notebooks:
        nb_path = notebooks_dir / nb_file
        if not nb_path.exists():
            print(f"{Colors.WARNING}⚠ Notebook not found: {nb_file} (skipping){Colors.ENDC}")
            continue
        
        cmd = f"jupyter nbconvert --execute --to notebook --inplace {nb_path}"
        if run_command(cmd, f"{description} ({nb_file})"):
            steps_completed.append(f"Notebook: {nb_file}")
        else:
            steps_failed.append(f"Notebook: {nb_file}")
            print(f"{Colors.WARNING}⚠ Continuing despite error in {nb_file}{Colors.ENDC}")
    
    # ==========================================
    # SUMMARY
    # ==========================================
    print_summary(start_time, steps_completed, steps_failed)

def print_summary(start_time, completed, failed):
    """Print final summary."""
    end_time = datetime.now()
    duration = end_time - start_time
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                         SUMMARY                                ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    print(f"Started:  {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Finished: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}")
    
    print(f"\n{Colors.OKGREEN}✓ Completed steps: {len(completed)}{Colors.ENDC}")
    for step in completed:
        print(f"  • {step}")
    
    if failed:
        print(f"\n{Colors.FAIL}✗ Failed steps: {len(failed)}{Colors.ENDC}")
        for step in failed:
            print(f"  • {step}")
    
    if not failed:
        print(f"\n{Colors.BOLD}{Colors.OKGREEN}🎉 Monthly refresh complete!{Colors.ENDC}")
        print(f"\n{Colors.OKCYAN}Next steps:{Colors.ENDC}")
        print(f"  1. Review updated dashboard")
        print(f"  2. Check representation_gaps.md for updates")
        print(f"  3. Commit changes to version control")
    else:
        print(f"\n{Colors.WARNING}⚠ Some steps failed. Review errors above.{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}✗ Interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n{Colors.FAIL}✗ Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
