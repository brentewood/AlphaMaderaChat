"""Command line utility to test Vision class with images."""

import argparse
from vision import Vision

def main():
    """Run the Vision analysis on an image file using command line arguments."""
    parser = argparse.ArgumentParser(description='Test Vision with an image')
    parser.add_argument('image_path', help='Path to the image file')
    parser.add_argument('--hint', help='Optional hint about the image content')
    parser.add_argument('--prompt', help='Custom prompt for the AI vision analysis')

    args = parser.parse_args()

    try:
        # Initialize Vision with command line arguments
        vision = Vision(
            image_path=args.image_path,
            hint=args.hint,
            prompt=args.prompt
        )

        # Analyze the image
        print(f"\nAnalyzing image: {args.image_path}")
        if args.hint:
            print(f"Hint provided: {args.hint}")

        url, description = vision.analyze()

        # Print results
        print("\nResults:")
        print("-" * 50)
        print(f"Image URL: {url}")
        print("\nDescription:")
        print("-" * 50)
        print(description)

    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"\nError: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())