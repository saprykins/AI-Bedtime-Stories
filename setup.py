#!/usr/bin/env python3
"""
Setup script for Story Teller AI Agent

This script helps users set up the environment and test the installation.
"""

import os
import sys
import subprocess
import shutil


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        "openai",
        "azure.cognitiveservices.speech"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True


def check_environment():
    """Check if environment variables are set."""
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_SPEECH_KEY", 
        "AZURE_SPEECH_REGION"
    ]
    
    missing_vars = []
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✅ {var} is set")
        else:
            missing_vars.append(var)
            print(f"❌ {var} is not set")
    
    if missing_vars:
        print(f"\n⚠️  Missing environment variables: {', '.join(missing_vars)}")
        print("   Please set up your Azure credentials as described in README.md")
        print("   You can copy env.example to .env and fill in your values")
        return False
    
    return True


def create_output_directory():
    """Create the output directory if it doesn't exist."""
    output_dir = os.getenv("OUTPUT_DIR", "./output")
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Output directory ready: {output_dir}")


def main():
    """Main setup function."""
    print("🎭 Story Teller AI Agent Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    print()
    
    # Check and install dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print()
    
    # Check environment variables
    env_ok = check_environment()
    
    print()
    
    # Create output directory
    create_output_directory()
    
    print()
    
    if env_ok:
        print("🎉 Setup completed successfully!")
        print("   You can now run: python story_agent.py \"Your problem description\"")
        print("   Or test with: python test_agent.py")
    else:
        print("⚠️  Setup completed with warnings")
        print("   Please configure your Azure credentials before using the agent")
    
    print("\n📚 For detailed setup instructions, see README.md")


if __name__ == "__main__":
    main()
