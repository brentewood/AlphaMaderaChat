"""Command line utility to test FoodVision class with food images."""

import argparse
from food_vision import FoodVision

def main():
    parser = argparse.ArgumentParser(description='Test FoodVision with a food image')
    parser.add_argument('image_path', help='Path to the food image file')
    parser.add_argument('--hint', help='Optional hint about the image content')
    parser.add_argument('--prompt', help='Custom prompt for the AI vision analysis')

    args = parser.parse_args()

    try:
        # Initialize FoodVision with command line arguments
        vision = FoodVision(
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

    except Exception as e:
        print(f"\nError: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())