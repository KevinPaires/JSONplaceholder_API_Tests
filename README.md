# API Test Automation Project

A comprehensive Python testing suite for REST API validation using pytest and the requests library. This project demonstrates testing best practices including positive tests, negative tests, edge cases, and integration scenarios.

## 🎯 Overview

This project provides a complete API testing framework that validates REST API endpoints for user and post resources. It tests CRUD operations (Create, Read, Update, Delete) and includes comprehensive error handling and edge case validation.

**Default API Under Test:** [JSONPlaceholder](https://jsonplaceholder.typicode.com) - A free fake REST API for testing and prototyping.

## ✨ Features

- **Comprehensive Test Coverage**: Positive, negative, edge case, and integration tests
- **Organized Test Structure**: Tests grouped by scenario type using pytest classes
- **Reusable Fixtures**: Common test data and configuration managed through fixtures
- **Environment Configuration**: Easy API endpoint switching via environment variables
- **Detailed Assertions**: Clear, descriptive test assertions with helpful error messages
- **Performance Testing**: Basic response time and consistency checks
- **Security Testing**: SQL injection and XSS validation
- **Known Issue Tracking**: Tests marked with `@pytest.mark.xfail` for documented bugs

## 🔧 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## 📦 Installation

1. **Clone or download the project**
   ```bash
   cd api-project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Project Structure

```
api-project/
├── tests/
│   ├── __pycache__/          # Python cache files
│   ├── conftest.py           # Pytest fixtures and configuration
│   ├── test_users.py         # Basic user endpoint tests
│   └── test_projects.py      # Comprehensive test suite
├── venv/                     # Virtual environment (not in version control)
├── .gitignore                # Git ignore rules
├── .env                      # Environment variables (create this)
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Project dependencies
└── README.md                 # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root to configure the API endpoint:

```env
API_BASE_URL=https://jsonplaceholder.typicode.com
```

### Pytest Configuration

The `pytest.ini` file contains test execution settings:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = -v
```

## 🚀 Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_users.py
pytest tests/test_projects.py
```

### Run Specific Test Class
```bash
pytest tests/test_projects.py::TestPositiveScenarios
pytest tests/test_projects.py::TestNegativeScenarios
```

### Run Specific Test
```bash
pytest tests/test_users.py::test_get_users
```

### Run with Detailed Output
```bash
pytest -v -s
```

### Run and Show Print Statements
```bash
pytest -v -s
```

### Run Tests Matching a Pattern
```bash
pytest -k "create_user"
```

### Generate HTML Report (requires pytest-html)
```bash
pip install pytest-html
pytest --html=report.html
```

## 📊 Test Coverage

### Test Categories

#### ✅ Positive Tests (`TestPositiveScenarios`)
- **test_get_single_user**: Retrieve user by ID
- **test_get_all_users**: Retrieve all users
- **test_get_single_post**: Retrieve post by ID
- **test_create_user**: Create new user
- **test_create_post**: Create new post
- **test_update_user_full**: Full update (PUT)
- **test_update_user_partial**: Partial update (PATCH)
- **test_delete_user**: Delete user
- **test_get_user_posts_relationship**: User-post relationship
- **test_response_headers**: Verify response headers

#### ❌ Negative Tests (`TestNegativeScenarios`)
- **test_get_nonexistent_user**: 404 handling
- **test_get_user_invalid_id_type**: Invalid ID type
- **test_create_user_missing_required_fields**: Missing fields
- **test_create_user_invalid_email_format**: Email validation
- **test_create_user_empty_payload**: Empty request body
- **test_update_nonexistent_user**: Update missing resource (known bug)
- **test_delete_nonexistent_user**: Delete missing resource
- **test_wrong_http_method**: Method not allowed
- **test_malformed_json**: Invalid JSON handling

#### 🔄 Edge Cases (`TestEdgeCases`)
- **test_create_user_empty_strings**: Empty string values
- **test_create_user_special_characters**: XSS and special chars
- **test_create_user_unicode_characters**: International characters
- **test_create_user_very_long_name**: Length limit testing
- **test_get_user_zero_id**: Zero ID edge case
- **test_sql_injection_attempt**: SQL injection protection

#### 🔗 Integration Tests (`TestIntegrationScenarios`)
- **test_create_update_delete_workflow**: Full CRUD workflow (known bug)
- **test_user_posts_integration**: User-post relationship validation

#### ⚡ Performance Tests (`TestPerformance`)
- **test_response_time**: Response time validation
- **test_multiple_requests_consistency**: Data consistency

## 🧪 Understanding the Tests

### Fixtures

The `conftest.py` file provides reusable fixtures:

- **base_url**: API endpoint URL (configurable via .env)
- **api_headers**: Common request headers
- **valid_user_payload**: Sample user data
- **valid_post_payload**: Sample post data

### Known Issues

Tests marked with `@pytest.mark.xfail` document known bugs:

```python
@pytest.mark.xfail(reason="BUG: PUT /users returns 500 instead of 200")
def test_create_update_delete_workflow(base_url, valid_user_payload):
    # This test fails due to a known API bug
    # Expected: 200 OK
    # Actual: 500 Internal Server Error
```

## 🤝 Contributing

To add new tests:

1. Create test functions following the naming convention `test_*`
2. Use descriptive docstrings
3. Group related tests in classes
4. Use appropriate assertions with clear messages
5. Add fixtures for reusable test data

Example:
```python
def test_new_feature(base_url):
    """Verify new feature works correctly"""
    response = requests.get(f"{base_url}/new-endpoint")
    assert response.status_code == 200, "Should return OK status"
```

## 📝 Dependencies

- **pytest**: Testing framework
- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management
- **pytest plugins**: For enhanced functionality

## 📄 License

This project is provided as-is for educational and testing purposes.

## 🔗 Resources

- [pytest Documentation](https://docs.pytest.org/)
- [requests Documentation](https://docs.python-requests.org/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/)
- [REST API Testing Best Practices](https://www.ministryoftesting.com/articles/api-testing-best-practices)

---

**Happy Testing! 🧪**
