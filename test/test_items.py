def test_create_item_success(client, test_user): 
    # (Lấy token của test_user vừa được tạo tự động)
    login_res = client.post("/token", data={"username": "testuser", "password": "password123"})
    
    # Kiểm tra login có thành công không
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}


    item_data = {"title": "Test Item From Pytest", "des": "Auto created"}
    response = client.post("/items/", json=item_data, headers=headers)
    
    # KIỂM TRA (Assert)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Item From Pytest"
    
    # Kiểm tra xem owner_id có đúng là ID của ông test_user không
    assert data["owner_id"] == test_user.id

def test_create_item_fail_no_token(client):
    # Cố tình tạo Item mà KHÔNG gửi headers (không đăng nhập)
    item_data = {"title": "Hacker Item", "des": "Should fail"}
    
    response = client.post("/items/", json=item_data)
    
    # Mong đợi lỗi 401 (Unauthorized)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_create_item_fail_no_token(client):
    item_data = {"title":"Hacker item", "des":"Should fail"}

    response = client.post("/items/",json=item_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"