import requests
import sys
import json
from datetime import datetime

class EmergentDocHubTester:
    def __init__(self, base_url="https://llm-component-roles.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test_result(self, test_name, passed, details=""):
        """Log test results for reporting"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        if passed:
            self.tests_passed += 1

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        request_headers = {'Content-Type': 'application/json'}
        if self.token:
            request_headers['Authorization'] = f'Bearer {self.token}'
        if headers:
            request_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=request_headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=request_headers, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=request_headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=request_headers, timeout=30)

            success = response.status_code == expected_status
            
            response_data = {}
            try:
                response_data = response.json()
            except:
                response_data = {"text": response.text}

            details = f"Status: {response.status_code}, Response: {json.dumps(response_data, indent=2)[:200]}..."
            
            if success:
                print(f"✅ Passed - Status: {response.status_code}")
                self.log_test_result(name, True, details)
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                self.log_test_result(name, False, details)

            return success, response_data

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"❌ Failed - {error_msg}")
            self.log_test_result(name, False, error_msg)
            return False, {}

    def test_register(self, email, name, password):
        """Test user registration"""
        success, response = self.run_test(
            f"Register User ({email})",
            "POST",
            "auth/register",
            200,
            data={"email": email, "name": name, "password": password}
        )
        if success and 'token' in response:
            self.token = response['token']
            print(f"   ✅ Token received and set")
            return True
        return False

    def test_login(self, email, password):
        """Test user login"""
        success, response = self.run_test(
            f"Login User ({email})",
            "POST",
            "auth/login",
            200,
            data={"email": email, "password": password}
        )
        if success and 'token' in response:
            self.token = response['token']
            print(f"   ✅ Token received and set")
            return True
        return False

    def test_get_me(self):
        """Test get current user"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        return success

    def test_get_categories(self):
        """Test get all categories"""
        success, response = self.run_test(
            "Get Categories",
            "GET",
            "categories",
            200
        )
        if success:
            print(f"   ✅ Found {len(response)} categories")
        return success, response

    def test_get_documents(self):
        """Test get all documents"""
        success, response = self.run_test(
            "Get All Documents",
            "GET",
            "documents",
            200
        )
        if success:
            print(f"   ✅ Found {len(response)} documents")
        return success, response

    def test_search_documents(self, query="kubernetes"):
        """Test search functionality"""
        success, response = self.run_test(
            f"Search Documents (q={query})",
            "GET",
            f"search?q={query}",
            200
        )
        if success:
            print(f"   ✅ Found {len(response)} matching documents")
        return success, response

    def test_create_document(self, title, content, category_id):
        """Test create new document"""
        success, response = self.run_test(
            "Create New Document",
            "POST",
            "documents",
            200,
            data={"title": title, "content": content, "category_id": category_id, "order": 0}
        )
        if success and 'id' in response:
            return response['id']
        return None

    def test_get_document(self, doc_id):
        """Test get specific document"""
        success, response = self.run_test(
            f"Get Document ({doc_id[:8]}...)",
            "GET",
            f"documents/{doc_id}",
            200
        )
        return success, response

    def test_update_document(self, doc_id, update_data):
        """Test update document"""
        success, response = self.run_test(
            f"Update Document ({doc_id[:8]}...)",
            "PUT",
            f"documents/{doc_id}",
            200,
            data=update_data
        )
        return success, response

    def test_bookmarks(self, doc_id):
        """Test bookmark functionality"""
        # Toggle bookmark on
        success1, response1 = self.run_test(
            f"Toggle Bookmark ON ({doc_id[:8]}...)",
            "POST",
            f"bookmarks/{doc_id}",
            200
        )
        
        # Get bookmarks
        success2, response2 = self.run_test(
            "Get User Bookmarks",
            "GET",
            "bookmarks",
            200
        )
        
        # Toggle bookmark off
        success3, response3 = self.run_test(
            f"Toggle Bookmark OFF ({doc_id[:8]}...)",
            "POST",
            f"bookmarks/{doc_id}",
            200
        )
        
        return success1 and success2 and success3

    def test_delete_document(self, doc_id):
        """Test delete document"""
        success, response = self.run_test(
            f"Delete Document ({doc_id[:8]}...)",
            "DELETE",
            f"documents/{doc_id}",
            200
        )
        return success

def main():
    print("🚀 Starting Emergent Document Hub API Testing...")
    
    # Setup
    tester = EmergentDocHubTester()
    test_user_email = "test@test.com"
    test_user_name = "Test User"
    test_user_password = "test1234"
    existing_user_email = "demo@emergent.com"
    existing_user_password = "demo1234"

    # Test 1: Register new user
    print("\n" + "="*60)
    print("PHASE 1: USER REGISTRATION & AUTHENTICATION")
    print("="*60)
    
    register_success = tester.test_register(test_user_email, test_user_name, test_user_password)
    if not register_success:
        print("⚠️  Registration failed, trying to login with existing credentials...")
        login_success = tester.test_login(test_user_email, test_user_password)
        if not login_success:
            print("❌ Both registration and login failed, stopping tests")
            return 1

    # Test current user endpoint
    tester.test_get_me()

    # Test 2: Try login with existing demo user
    print(f"\n🔄 Testing login with existing user: {existing_user_email}")
    demo_login = tester.test_login(existing_user_email, existing_user_password)

    # Test 3: Get data endpoints
    print("\n" + "="*60)
    print("PHASE 2: DATA RETRIEVAL ENDPOINTS")
    print("="*60)
    
    categories_success, categories = tester.test_get_categories()
    documents_success, documents = tester.test_get_documents()
    search_success, search_results = tester.test_search_documents("kubernetes")
    
    # Additional search tests
    tester.test_search_documents("transformer")
    tester.test_search_documents("agent")

    # Test 4: Document CRUD operations
    print("\n" + "="*60)
    print("PHASE 3: DOCUMENT CRUD OPERATIONS")
    print("="*60)
    
    if categories_success and len(categories) > 0:
        # Find a suitable category for testing
        test_category_id = categories[0]['id'] if categories else None
        
        if test_category_id:
            # Create new document
            new_doc_id = tester.test_create_document(
                "Test Document", 
                "# Test Document\n\nThis is a test document created by automated testing.\n\n## Features\n\n- Testing CRUD operations\n- Markdown content\n- Categories\n\n```python\nprint('Hello, World!')\n```",
                test_category_id
            )
            
            if new_doc_id:
                # Get the created document
                tester.test_get_document(new_doc_id)
                
                # Update the document
                tester.test_update_document(new_doc_id, {
                    "title": "Updated Test Document",
                    "content": "# Updated Test Document\n\nThis document has been updated by automated testing."
                })
                
                # Test bookmark functionality
                tester.test_bookmarks(new_doc_id)
                
                # Delete the test document
                tester.test_delete_document(new_doc_id)
                
    # Test 5: Additional API endpoints
    print("\n" + "="*60)
    print("PHASE 4: ADDITIONAL ENDPOINT TESTS")
    print("="*60)
    
    # Test root endpoint
    tester.run_test("Root API Endpoint", "GET", "", 200)
    
    # Print final results
    print("\n" + "="*60)
    print("FINAL TEST RESULTS")
    print("="*60)
    print(f"📊 Tests passed: {tester.tests_passed}/{tester.tests_run}")
    print(f"📈 Success rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    # Show failed tests
    failed_tests = [r for r in tester.test_results if not r['passed']]
    if failed_tests:
        print(f"\n❌ Failed tests ({len(failed_tests)}):")
        for test in failed_tests:
            print(f"   • {test['test']}: {test['details'][:100]}...")
    
    # Show passed tests summary
    passed_tests = [r for r in tester.test_results if r['passed']]
    if passed_tests:
        print(f"\n✅ Passed tests ({len(passed_tests)}):")
        for test in passed_tests:
            print(f"   • {test['test']}")
    
    return 0 if tester.tests_passed == tester.tests_run else 1

if __name__ == "__main__":
    sys.exit(main())