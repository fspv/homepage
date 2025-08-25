#!/usr/bin/env python3
"""
RSS 2.0 Feed Validator

This script validates RSS feeds for both XML syntax and RSS 2.0 compliance.
It can be run manually or as part of a CI/CD pipeline.

Usage:
    python validate_rss.py <rss_file>
    python validate_rss.py <directory>  # Validates all RSS/XML files in directory
"""

import sys
import os
import glob
import feedparser
from urllib.parse import urlparse


def validate_rss(file_path):
    """Validate a single RSS feed file for RSS 2.0 compliance."""
    print(f"\nValidating RSS 2.0 compliance for: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"  ERROR: Cannot read file - {e}")
        return False
    
    # Parse the feed
    feed = feedparser.parse(content)
    
    # Check if it's a valid feed
    if feed.bozo:
        print(f"  ERROR: Feed parsing failed - {feed.bozo_exception}")
        return False
    
    # Check RSS version
    if not hasattr(feed, 'version'):
        print("  ERROR: No RSS version specified")
        return False
    
    if not feed.version.startswith('rss20'):
        print(f"  WARNING: Not RSS 2.0 (found: {feed.version})")
    
    # Check required channel elements
    required_channel = ['title', 'link', 'description']
    missing_elements = []
    for elem in required_channel:
        if not hasattr(feed.feed, elem) or not getattr(feed.feed, elem):
            missing_elements.append(elem)
    
    if missing_elements:
        print(f"  ERROR: Missing required channel elements: {', '.join(missing_elements)}")
        return False
    
    # Validate items
    if not feed.entries:
        print("  WARNING: No items found in feed")
    else:
        errors = []
        warnings = []
        
        for i, entry in enumerate(feed.entries):
            # Check required item elements (at least title or description)
            if not hasattr(entry, 'title') and not hasattr(entry, 'description'):
                errors.append(f"Item {i} missing both title and description")
            
            # Check for guid
            if not hasattr(entry, 'id'):
                warnings.append(f"Item {i} missing guid")
            
            # Check for pubDate
            if not hasattr(entry, 'published'):
                warnings.append(f"Item {i} missing pubDate")
            
            # Check for link
            if not hasattr(entry, 'link'):
                warnings.append(f"Item {i} missing link")
        
        # Print errors and warnings
        for error in errors:
            print(f"  ERROR: {error}")
        for warning in warnings:
            print(f"  WARNING: {warning}")
        
        if errors:
            return False
    
    # Additional checks
    print(f"  INFO: Found {len(feed.entries)} items")
    if hasattr(feed.feed, 'language'):
        print(f"  INFO: Language: {feed.feed.language}")
    if hasattr(feed.feed, 'generator'):
        print(f"  INFO: Generator: {feed.feed.generator}")
    
    print("  PASS: RSS 2.0 validation successful")
    return True


def find_rss_files(path):
    """Find RSS/XML files in a directory."""
    rss_files = []
    
    if os.path.isfile(path):
        return [path]
    
    if os.path.isdir(path):
        # Look for common RSS file patterns
        patterns = ['**/index.xml', '**/rss.xml', '**/feed.xml', '**/atom.xml']
        for pattern in patterns:
            rss_files.extend(glob.glob(os.path.join(path, pattern), recursive=True))
    
    return list(set(rss_files))  # Remove duplicates


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    path = sys.argv[1]
    
    # Find RSS files
    rss_files = find_rss_files(path)
    
    if not rss_files:
        print(f"No RSS files found in: {path}")
        sys.exit(1)
    
    print(f"Found {len(rss_files)} RSS file(s) to validate")
    
    # Validate each file
    all_valid = True
    for rss_file in sorted(rss_files):
        if not validate_rss(rss_file):
            all_valid = False
    
    # Summary
    print("\n" + "="*50)
    if all_valid:
        print("SUCCESS: All RSS feeds are valid!")
        sys.exit(0)
    else:
        print("FAILURE: Some RSS feeds have validation errors!")
        sys.exit(1)


if __name__ == "__main__":
    main()