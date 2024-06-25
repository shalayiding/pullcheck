from dotenv import load_dotenv
import os

# Load environment variables from .env file
# load_dotenv()
current_script_dir = os.path.dirname(os.path.abspath(__file__))
# Access environment variables
TABLE_DIR = os.path.join(current_script_dir, "table")

