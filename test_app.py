"""
=============================================================================
Prakriti: Nature & Belief Explorer - Comprehensive Automated Test Suite
=============================================================================
Tests all routes, views, database queries, and admin operations.
=============================================================================
"""

import os
import sys

# Ensure current directory is in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import database
from app import app, ADMIN_PASSWORD

def run_tests():
    print("=" * 70)
    print("Starting Automated Test Suite for 'Prakriti: Nature & Belief Explorer'")
    print("=" * 70)

    # 1. Test Database Initialization and Seed
    database.init_db()
    database.seed_db()
    stats = database.get_stats()
    print(f"[TEST 1] Database Stats: {stats}")
    assert stats["elements"] >= 12, f"Expected >= 12 elements, found {stats['elements']}"
    assert stats["beliefs"] >= 12, f"Expected >= 12 beliefs, found {stats['beliefs']}"
    assert stats["festivals"] >= 8, f"Expected >= 8 festivals, found {stats['festivals']}"
    assert stats["quiz_questions"] >= 10, f"Expected >= 10 quiz questions, found {stats['quiz_questions']}"
    print("  -> PASSED: Database seeded with accurate and sufficient records.")

    # 2. Test Flask Client Requests
    client = app.test_client()

    # Route: / (Home)
    res = client.get("/")
    assert res.status_code == 200, f"Home page returned status {res.status_code}"
    assert b"Where Sacred Tradition Meets" in res.data
    assert b"Surya (The Sun)" in res.data
    print("  -> PASSED: Home page ('/') rendered correctly.")

    # Route: /browse (Browse without filters)
    res = client.get("/browse")
    assert res.status_code == 200, f"Browse page returned status {res.status_code}"
    assert b"Explore Sacred Nature Elements" in res.data
    assert b"Peepal Tree" in res.data
    print("  -> PASSED: Browse page ('/browse') rendered correctly.")

    # Route: /browse with Category Filter
    res = client.get("/browse?category=Flora+%26+Sacred+Plants")
    assert res.status_code == 200
    assert b"Tulsi (Holy Basil)" in res.data
    print("  -> PASSED: Browse category filtering works.")

    # Route: /browse with Search Query
    res = client.get("/browse?search=Ganga")
    assert res.status_code == 200
    assert b"Maa Ganga" in res.data
    print("  -> PASSED: Browse search filtering works.")

    # Route: /element/1 (Surya Detail)
    res = client.get("/element/1")
    assert res.status_code == 200
    assert b"Surya (The Sun)" in res.data
    assert b"Sacred Tradition &amp; Cultural Belief" in res.data or b"Sacred Tradition & Cultural Belief" in res.data
    assert b"Ecological &amp; Scientific Rationale" in res.data or b"Ecological & Scientific Rationale" in res.data
    assert b"Chhath Puja" in res.data
    print("  -> PASSED: Element detail page ('/element/1') rendered with Belief vs Science card and festivals.")

    # Route: /element/4 (Peepal Detail)
    res = client.get("/element/4")
    assert res.status_code == 200
    assert b"Peepal Tree" in res.data
    print("  -> PASSED: Element detail page ('/element/4') works.")

    # Route: /festivals
    res = client.get("/festivals")
    assert res.status_code == 200
    assert b"Festivals Honoring Nature" in res.data
    assert b"Chhath Puja" in res.data
    assert b"Nag Panchami" in res.data
    assert b"Raja Parba" in res.data
    print("  -> PASSED: Festivals page ('/festivals') rendered all nature festivals.")

    # Route: /quiz
    res = client.get("/quiz")
    assert res.status_code == 200
    assert b"Superstition or Science?" in res.data
    assert b"quizDataJson" in res.data
    print("  -> PASSED: Quiz page ('/quiz') rendered with interactive quiz questions.")

    # Route: /api/quiz
    res = client.get("/api/quiz")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) >= 10
    assert "question" in data[0]
    assert "correct_option" in data[0]
    assert "explanation" in data[0]
    print(f"  -> PASSED: API endpoint ('/api/quiz') returned {len(data)} questions as JSON.")

    # Route: /admin/login (GET)
    res = client.get("/admin/login")
    assert res.status_code == 200
    assert b"Admin Portal" in res.data
    print("  -> PASSED: Admin login page rendered.")

    # Unauthorized access to /admin should redirect to /admin/login
    res = client.get("/admin", follow_redirects=False)
    assert res.status_code == 302
    assert "/admin/login" in res.headers["Location"]
    print("  -> PASSED: Unauthorized access to '/admin' correctly blocked and redirected.")

    # Test Admin Login with incorrect password
    res = client.post("/admin/login", data={"password": "wrongpassword"}, follow_redirects=True)
    assert b"Incorrect password" in res.data
    print("  -> PASSED: Incorrect admin password correctly rejected.")

    # Test Admin Login with correct password
    res = client.post("/admin/login", data={"password": ADMIN_PASSWORD}, follow_redirects=True)
    assert b"Welcome back, Curator" in res.data
    assert b"Prakriti Content Management" in res.data
    print("  -> PASSED: Admin authentication succeeded with correct password.")

    # Test Admin Add Element
    new_elem_payload = {
        "name": "Bael Tree (Bilva / Aegle marmelos)",
        "category": "Flora & Sacred Plants",
        "description": "Sacred to Lord Shiva with trifoliate leaves symbolizing the Trinity. Rich in digestive marmelosin.",
        "image_url": "/static/images/peepal.svg"
    }
    res = client.post("/admin/element/add", data=new_elem_payload, follow_redirects=True)
    assert b"successfully added" in res.data
    assert b"Bael Tree" in res.data
    print("  -> PASSED: Admin Add Element works.")

    # Find the newly added element ID
    elements = database.get_all_elements(search="Bael Tree")
    assert len(elements) > 0
    bael_id = elements[0]["id"]

    # Test Admin Edit Element
    edit_elem_payload = {
        "name": "Bael Tree (Sacred Bilva)",
        "category": "Flora & Sacred Plants",
        "description": "Updated description: Sacred to Lord Shiva with potent antimicrobial and hypoglycemic properties.",
        "image_url": "/static/images/peepal.svg"
    }
    res = client.post(f"/admin/element/edit/{bael_id}", data=edit_elem_payload, follow_redirects=True)
    assert b"successfully updated" in res.data
    print("  -> PASSED: Admin Edit Element works.")

    # Test Admin Delete Element
    res = client.post(f"/admin/element/delete/{bael_id}", follow_redirects=True)
    assert b"deleted successfully" in res.data
    print("  -> PASSED: Admin Delete Element works.")

    # Test Admin Logout
    res = client.get("/admin/logout", follow_redirects=True)
    assert b"logged out of the Admin Portal" in res.data
    print("  -> PASSED: Admin logout works.")

    print("=" * 70)
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
