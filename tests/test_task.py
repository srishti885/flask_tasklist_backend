def test_create_task(client):
    response = client.post('/api/task', json={
        'task_name': 'Test Task'
    }, headers={'Authorization': 'Bearer your-secret-token'})
    assert response.status_code == 201
