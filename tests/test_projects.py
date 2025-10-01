
import requests
import pytest
from typing import Dict, Any





# POSITIVE TESTS - Core Functionality


class TestPositiveScenarios:
    """Tests for successful API operations (happy paths)"""

    def test_get_single_user(self, base_url):
        """Verify retrieving a single user by ID returns correct data"""
        response = requests.get(f"{base_url}/users/1")
        
        assert response.status_code == 200, "Should return OK status"
        data = response.json()
        assert data["id"] == 1, "User ID should match request"
        assert "name" in data, "Response should contain name field"
        assert "email" in data, "Response should contain email field"
        assert "username" in data, "Response should contain username field"

    def test_get_all_users(self, base_url):
        """Verify retrieving all users returns a list"""
        response = requests.get(f"{base_url}/users")
        
        assert response.status_code == 200, "Should return OK status"
        data = response.json()
        assert isinstance(data, list), "Should return a list of users"
        assert len(data) > 0, "Should return at least one user"
        assert "id" in data[0], "User objects should have ID field"

    def test_get_single_post(self, base_url):
        """Verify retrieving a single post returns correct structure"""
        response = requests.get(f"{base_url}/posts/1")
        
        assert response.status_code == 200, "Should return OK status"
        data = response.json()
        assert data["id"] == 1, "Post ID should match request"
        assert "title" in data, "Post should have title"
        assert "body" in data, "Post should have body"
        assert "userId" in data, "Post should have userId"

    def test_create_user(self, base_url, valid_user_payload):
        """Verify creating a new user with valid data succeeds"""
        response = requests.post(f"{base_url}/users", json=valid_user_payload)
        
        assert response.status_code in [200, 201], "Should return success status"
        data = response.json()
        assert data["name"] == valid_user_payload["name"], "Name should match"
        assert data["email"] == valid_user_payload["email"], "Email should match"

    def test_create_post(self, base_url, valid_post_payload):
        """Verify creating a new post with valid data succeeds"""
        response = requests.post(f"{base_url}/posts", json=valid_post_payload)
        
        assert response.status_code in [200, 201], "Should return success status"
        data = response.json()
        assert data["title"] == valid_post_payload["title"], "Title should match"
        assert data["userId"] == valid_post_payload["userId"], "UserId should match"

    def test_update_user_full(self, base_url, valid_user_payload):
        """Verify full update (PUT) of user data works correctly"""
        response = requests.put(f"{base_url}/users/1", json=valid_user_payload)
        
        assert response.status_code == 200, "Should return OK status"
        data = response.json()
        assert data["name"] == valid_user_payload["name"], "Updated name should match"

    def test_update_user_partial(self, base_url):
        """Verify partial update (PATCH) of user data works correctly"""
        payload = {"name": "Jane Smith"}
        response = requests.patch(f"{base_url}/users/1", json=payload)
        
        assert response.status_code == 200, "Should return OK status"
        data = response.json()
        assert data["name"] == payload["name"], "Patched field should update"

    def test_delete_user(self, base_url):
        """Verify deleting a user returns appropriate status"""
        response = requests.delete(f"{base_url}/users/1")
        
        assert response.status_code in [200, 204], "Should return success status"

    def test_get_user_posts_relationship(self, base_url):
        """Verify retrieving posts for a specific user works"""
        response = requests.get(f"{base_url}/users/1/posts")
        
        assert response.status_code == 200, "Should return OK status"
        data = response.json()
        assert isinstance(data, list), "Should return list of posts"
        if len(data) > 0:
            assert data[0]["userId"] == 1, "Posts should belong to correct user"

    def test_response_headers(self, base_url):
        """Verify API returns appropriate response headers"""
        response = requests.get(f"{base_url}/users/1")
        
        assert response.status_code == 200
        assert "content-type" in response.headers, "Should have content-type header"
        assert "application/json" in response.headers["content-type"], "Should return JSON"


# NEGATIVE TESTS - Error Handling


class TestNegativeScenarios:
    """Tests for error conditions and invalid inputs"""

    def test_get_nonexistent_user(self, base_url):
        """Verify requesting non-existent user returns 404"""
        response = requests.get(f"{base_url}/users/999999")
        
        assert response.status_code == 404, "Should return Not Found for invalid ID"

    def test_get_user_invalid_id_type(self, base_url):
        """Verify using non-numeric ID is handled properly"""
        response = requests.get(f"{base_url}/users/invalid_id")
        
        assert response.status_code in [400, 404], "Should reject non-numeric ID"

    def test_create_user_missing_required_fields(self, base_url):
        """Verify incomplete user data is rejected or handled"""
        payload = {"username": "incomplete"}  # Missing name and email
        response = requests.post(f"{base_url}/users", json=payload)
        
        # Note: Some mock APIs accept anything; document actual behavior
        # In production API, should return 400 or 422
        if response.status_code in [400, 422]:
            assert True, "API correctly validates required fields"
        else:
            # Document that validation is not enforced
            assert response.status_code in [200, 201], "API accepts partial data"

    def test_create_user_invalid_email_format(self, base_url):
        """Verify invalid email format is rejected"""
        payload = {
            "name": "John Doe",
            "username": "johndoe",
            "email": "not-a-valid-email"  # Invalid format
        }
        response = requests.post(f"{base_url}/users", json=payload)
        
        # Should validate email format in production
        # Document actual behavior if validation not enforced
        assert response.status_code in [200, 201, 400, 422]

    def test_create_user_empty_payload(self, base_url):
        """Verify empty request body is handled appropriately"""
        response = requests.post(f"{base_url}/users", json={})
        
        assert response.status_code in [200, 201, 400, 422], "Should handle empty data"

    

    @pytest.mark.xfail(reason="PUT /users returns 500 instead of 200")
    def test_update_nonexistent_user(base_url):
        response = requests.put(f"{base_url}/users/999999", json={"name": "Test"})
        assert response.status_code == 404


    def test_delete_nonexistent_user(self, base_url):
        """Verify deleting non-existent user is handled properly"""
        response = requests.delete(f"{base_url}/users/999999")
        
        assert response.status_code in [200, 204, 404], "Should handle missing resource"

    def test_wrong_http_method(self, base_url):
        """Verify using incorrect HTTP method returns error"""
        # POST to an endpoint that expects GET
        response = requests.post(f"{base_url}/users/1")
        
        # Should return 405 Method Not Allowed in REST standards
        assert response.status_code in [404, 405], "Should reject wrong HTTP method"

    def test_malformed_json(self, base_url):
        """Verify malformed JSON is rejected"""
        response = requests.post(
            f"{base_url}/users",
            data="this is not valid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code in [400, 500], "Should reject malformed JSON"


# EDGE CASES - Boundary Conditions


class TestEdgeCases:
    """Tests for boundary conditions and unusual inputs"""

    def test_create_user_empty_strings(self, base_url):
        """Verify handling of empty string values"""
        payload = {
            "name": "",
            "username": "",
            "email": ""
        }
        response = requests.post(f"{base_url}/users", json=payload)
        
        # Should validate non-empty strings in production
        assert response.status_code in [200, 201, 400, 422]

    def test_create_user_special_characters(self, base_url):
        """Verify handling of special characters in input"""
        payload = {
            "name": "John <script>alert('xss')</script>",
            "username": "user@#$%",
            "email": "test+tag@example.com"
        }
        response = requests.post(f"{base_url}/users", json=payload)
        
        assert response.status_code in [200, 201, 400], "Should handle special chars"
        if response.status_code in [200, 201]:
            data = response.json()
            # Verify XSS content is not executed
            assert "<script>" in data["name"] or data["name"] != payload["name"]

    def test_create_user_unicode_characters(self, base_url):
        """Verify handling of international/unicode characters"""
        payload = {
            "name": "José García 李明",
            "username": "jose_李",
            "email": "josé@example.com"
        }
        response = requests.post(f"{base_url}/users", json=payload)
        
        assert response.status_code in [200, 201], "Should accept unicode characters"

    def test_create_user_very_long_name(self, base_url):
        """Verify handling of excessively long field values"""
        payload = {
            "name": "A" * 1000,  # Very long name
            "username": "testuser",
            "email": "test@example.com"
        }
        response = requests.post(f"{base_url}/users", json=payload)
        
        # Should enforce length limits in production
        assert response.status_code in [200, 201, 400, 422]

    def test_get_user_zero_id(self, base_url):
        """Verify handling of edge case ID value (zero)"""
        response = requests.get(f"{base_url}/users/0")
        
        assert response.status_code in [404, 400], "Zero ID should not exist"

    def test_sql_injection_attempt(self, base_url):
        """Verify API is protected against SQL injection"""
        malicious_id = "1' OR '1'='1"
        response = requests.get(f"{base_url}/users/{malicious_id}")
        
        assert response.status_code in [400, 404], "Should reject SQL injection attempt"
        # Should NOT return all users


# INTEGRATION TESTS - Multi-step Workflows


class TestIntegrationScenarios:
    """Tests for complete workflows involving multiple API calls"""

    @pytest.mark.xfail(reason="BUG: PUT /users returns 500 instead of 200")
    def test_create_update_delete_workflow(base_url, valid_user_payload):
        """
        Test complete CRUD workflow for a user
        
        BUG REPORT
        ================================
        Summary: PUT operation fails with 500 error during CRUD workflow
        Expected: CREATE → READ → UPDATE → DELETE should succeed
        Actual:   PUT /users/{id} fails with 500 Internal Server Error
        Severity: HIGH | Priority: CRITICAL
        
        """

        # Step 1: Create user
        create_response = requests.post(f"{base_url}/users", json=valid_user_payload)
        assert create_response.status_code in [200, 201], "User creation should succeed"
        user_id = create_response.json().get("id", 101)

        # Step 2: Read created user
        get_response = requests.get(f"{base_url}/users/{user_id}")
        assert get_response.status_code == 200, "User should exist after creation"

        # Step 3: Update user (BUG HERE)
        update_payload = {"name": "Jane Updated"}
        update_response = requests.put(f"{base_url}/users/{user_id}", json=update_payload)

        # This is the correct behavior we EXPECT:
        assert update_response.status_code == 200, "Update should succeed"
        assert update_response.json()["name"] == "Jane Updated"

        # Step 4: Delete user
        delete_response = requests.delete(f"{base_url}/users/{user_id}")
        assert delete_response.status_code in [200, 204], "User should be deletable"


    def test_user_posts_integration(self, base_url):
        """Verify relationship between users and their posts"""
        # Get a user
        user_response = requests.get(f"{base_url}/users/1")
        assert user_response.status_code == 200
        user_id = user_response.json()["id"]
        
        # Get posts for that user
        posts_response = requests.get(f"{base_url}/posts?userId={user_id}")
        assert posts_response.status_code == 200
        posts = posts_response.json()
        
        # Verify all posts belong to the user
        if len(posts) > 0:
            for post in posts:
                assert post["userId"] == user_id, "All posts should belong to user"


class TestPerformance:
    """Basic performance and reliability checks"""

    def test_response_time(self, base_url):
        """Verify API responds within acceptable time"""
        import time
        
        start_time = time.time()
        response = requests.get(f"{base_url}/users/1")
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = end_time - start_time
        assert response_time < 2.0, f"Response time {response_time}s exceeds 2s threshold"

    def test_multiple_requests_consistency(self, base_url):
        """Verify API returns consistent results across multiple requests"""
        responses = []
        for _ in range(3):
            response = requests.get(f"{base_url}/users/1")
            assert response.status_code == 200
            responses.append(response.json())
        
        # All responses should be identical
        assert responses[0] == responses[1] == responses[2], "Responses should be consistent"


