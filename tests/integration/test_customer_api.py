import unittest
import requests
import os
import subprocess
import json
from dotenv import load_dotenv


class TestCustomerAPI(unittest.TestCase):

    SCRIPTS_PATH = os.path.join(os.path.dirname(__file__), "../../setup_scripts")
    load_dotenv(dotenv_path=os.path.join(SCRIPTS_PATH, ".env"))

    API_ENDPOINT = os.getenv("DEFAULT_ENDPOINT")
    CUSTOMER_PATH = "/customers"

    def test_get_customers(self):
        """
        Tests the GET /customers endpoint to ensure it returns a 200 status
        code and the expected hardcoded JSON array.
        """

        script_path = "./get-admin-id-token.sh"
        try:
            process = subprocess.Popen(
                [script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.SCRIPTS_PATH
            )
            stdout, _ = process.communicate()
        except FileNotFoundError:
            self.fail(f"Error: Script not found at {script_path}")

        admin_id_token = stdout.rstrip()

        headers = {
            "Authorization": f"Bearer {admin_id_token}"
        }

        url = f"{self.API_ENDPOINT}{self.CUSTOMER_PATH}"
        response = requests.get(url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        try:
            customers = response.json()  # [{'id': 1000, 'name': 'John Doe'}, {'id': 1001, 'name': 'Jane Smith'}]
            self.assertIsInstance(customers, list)
            self.assertEqual(len(customers), 2)
            self.assertEqual(1000, customers[0]['id'])
            self.assertIn('John Doe', customers[0]['name'])
        except json.JSONDecodeError:
            self.fail("Response body is not valid JSON")


if __name__ == "__main__":
    unittest.main()
