from crews.outline_crew import OutlineCrew
import os

def main():
    """Main function that serves as the entry point of the script."""

    os.environ["OPENAI_API_KEY"]="_"

    inputs = {
    'seminararbeitthema': 'AI Agents' }
  
    OutlineCrew().crew().kickoff(inputs=inputs)


if __name__ == "__main__":
    main()