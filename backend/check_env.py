#!/usr/bin/env python3
"""
Environment Configuration Checker
Diagnoses configuration loading issues for Deep Character Research
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_env_file():
    """Check if .env file exists and show its contents"""
    env_path = Path('.env')
    print("=" * 50)
    print("1. CHECKING .ENV FILE")
    print("=" * 50)

    if env_path.exists():
        print("✓ .env file found")
        print("\nContents:")
        with open(env_path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines, 1):
                if line.strip() and not line.startswith('#'):
                    print(f"  {i:2d}: {line.strip()}")
    else:
        print("✗ .env file NOT found")
        return False
    return True

def check_env_loading():
    """Check environment variable loading"""
    print("\n" + "=" * 50)
    print("2. CHECKING ENVIRONMENT LOADING")
    print("=" * 50)

    # Load environment
    load_dotenv()

    env_vars = [
        'DEFAULT_MODEL',
        'DEFAULT_AI_PROVIDER', 
        'OPENROUTER_API_KEY',
        'FALLBACK_ENABLED'
    ]

    for var in env_vars:
        value = os.getenv(var)
        if value:
            if 'API_KEY' in var:
                # Mask API key for security
                masked = value[:8] + '*' * (len(value) - 12) + value[-4:] if len(value) > 12 else '*' * len(value)
                print(f"  ✓ {var}: {masked}")
            else:
                print(f"  ✓ {var}: {value}")
        else:
            print(f"  ✗ {var}: NOT SET")

def check_config_loading():
    """Check configuration class loading"""
    print("\n" + "=" * 50)
    print("3. CHECKING CONFIG CLASS LOADING")
    print("=" * 50)

    try:
        from config import ResearchConfig
        config = ResearchConfig()

        print(f"  ✓ ResearchConfig loaded")
        print(f"  ✓ default_provider: {config.default_provider}")
        print(f"  ✓ default_model: {config.default_model}")
        print(f"  ✓ fallback_enabled: {config.fallback_enabled}")

        # Check AI config
        ai_config = config.get_ai_config()
        print(f"  ✓ AIConfig default_model: {ai_config.default_model}")

    except Exception as e:
        print(f"  ✗ Error loading config: {e}")
        return False
    return True

def check_ai_providers():
    """Check AI provider configuration"""
    print("\n" + "=" * 50)
    print("4. CHECKING AI PROVIDERS")
    print("=" * 50)

    try:
        from ai_providers import AIConfig
        ai_config = AIConfig()

        print(f"  ✓ AIConfig loaded directly")
        print(f"  ✓ default_provider: {ai_config.default_provider}")
        print(f"  ✓ default_model: {ai_config.default_model}")
        print(f"  ✓ openrouter_api_key: {'SET' if ai_config.openrouter_api_key else 'NOT SET'}")

        # Return True since we got this far without exceptions
        return True

    except Exception as e:
        print(f"  ✗ Error loading AI providers: {e}")
        return False

def main():
    """Main diagnostic function"""
    print("DEEP CHARACTER RESEARCH - ENVIRONMENT DIAGNOSTIC")
    print("=" * 60)
    print(f"Current directory: {Path.cwd()}")
    print(f"Python version: {sys.version}")
    print()

    # Run all checks
    checks = [
        check_env_file(),
        check_env_loading(),
        check_config_loading(),
        check_ai_providers()
    ]

    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    if all(checks):
        print("✓ All checks passed! Configuration should be working.")
    else:
        print("✗ Some checks failed. Please review the issues above.")

    print("\nTo fix environment issues:")
    print("1. Ensure .env file exists and has correct values")
    print("2. Restart your application completely")
    print("3. Clear Python cache: Remove-Item -Recurse -Force __pycache__")

if __name__ == "__main__":
    main()