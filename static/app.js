document.getElementById('registerForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    fetch('/user/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        })
    }).then(response => {
        response.json()
        if (response.status === 201) {
            window.location.href = "/pages/login"
        }
    }).catch(e => console.log(e),);
});

document.getElementById('loginForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    fetch('/user/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        })
    }).then(response => response.json())
      .then(data => {
          if (data.access_token) {
              localStorage.setItem('token', data.access_token);
              window.location.href = '/pages/tasks';
          } else {
              document.getElementById('message').innerText = data.message;
          }
      }).catch(e => console.log(e));
});

document.addEventListener('DOMContentLoaded', function() {
    loadTasks();
});

document.getElementById('taskForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const token = localStorage.getItem('token');
    fetch('/task/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            title: document.getElementById('title').value,
            description: document.getElementById('description').value
        })
    }).then(response => response.json())
      .then(data => {
          loadTasks();
          document.getElementById('title').value = '';
          document.getElementById('description').value = '';
      });
});

function loadTasks() {
    const token = localStorage.getItem('token');
    fetch('/task/get-tasks-by-username?username=' + encodeURIComponent(getUsernameFromToken()), {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(async response => {
        if (response.ok) {
            return response.json();
        } else {
            const text = await response.text();
            throw new Error(text);
        }
    }).then(data => {
        if (Array.isArray(data)) {
            let tasksHTML = '';
            data.forEach(task => {
                tasksHTML += `
                    <div class="task-item mt-2">
                        <h5>${task.title}</h5>
                        <p>${task.description}</p>
                        <p>Created At: ${new Date(task.createdAt).toLocaleString()}</p>
                        <button class="btn btn-warning btn-sm" onclick="editTask('${task.id}', '${task.title}', '${task.description}')">Edit</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteTask('${task.id}')">Delete</button>
                    </div>
                `;
            });
            document.getElementById('taskList').innerHTML = tasksHTML;
        } else {
            document.getElementById('taskList').innerHTML = '<p>No tasks found.</p>';
        }
    }).catch(error => {
        console.error('Error fetching tasks:', error);
        document.getElementById('taskList').innerHTML = '<p>Error loading tasks.</p>';
    });
}

function getUsernameFromToken() {
    const token = localStorage.getItem('token');
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub;
}
function editTask(taskId, currentTitle, currentDescription) {
    const newTitle = prompt("Enter new title:", currentTitle);
    const newDescription = prompt("Enter new description:", currentDescription);

    if (newTitle !== null && newDescription !== null) {
        const token = localStorage.getItem('token');
        fetch('/task/update', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                id: taskId,
                title: newTitle,
                description: newDescription
            })
        }).then(response => response.json())
          .then(data => {
              loadTasks();
          });
    }
}

function deleteTask(taskId) {
    const token = localStorage.getItem('token');
    fetch('/task/delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ id: taskId })
    }).then(response => response.json())
      .then(data => {
          loadTasks();
      });
}

document.getElementById('updateUserForm')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const newUsername = document.getElementById('newUsername').value;
    const newPassword = document.getElementById('newPassword').value;
    const token = localStorage.getItem('token');

    fetch('/user/update', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            username: newUsername,
            password: newPassword
        })
    }).then(response => response.json())
      .then(data => {
          document.getElementById('updateMessage').innerText = data.message;

          return fetch('/user/auth', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                  username: newUsername,
                  password: newPassword
              })
          });
      }).then(response => response.json())
      .then(data => {
          if (data.access_token) {
              localStorage.setItem('token', data.access_token);
              window.location.href = "/pages/tasks";
          } else {
              document.getElementById('message').innerText = data.message;
          }
      }).catch(e => {
          console.error(e);
          document.getElementById('message').innerText = "An error occurred.";
      });
});


document.getElementById('deleteUserForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    const token = localStorage.getItem('token');
    fetch('/user/delete', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        }
    }).then(response => response.json())
      .then(data => {
          document.getElementById('deleteMessage').innerText = data.message;
          if (data.message === 'User deleted successfully') {
              localStorage.removeItem('token');
              window.location.href = '/login';
          }
      });
});

document.getElementById('tasksPage') && loadTasks();
