(function() {
    angular.module('todoList').service('requestService', function($http) {
        var service = this;
        var _user;
        service.view_task = {};
        service.current_id = 0;
        Object.defineProperties(service, {
            user: {
                get: function() {
                    return _user;
                },
                set: function(data) {
                    _user = data;
                }
            }
        });

        service.fetchTasks = function() {
            return $http.get('/api/multido');
        };

        service.sendEmail = function sendEmail() {
            $http.get('/api/deadline');
        }

        service.fetchTask = function(id) {
            service.view_task = {};
            var promise = $http.get('/api/singledo/' + id).then(function(response) {
                task = new Task({
                    name: response.data['name'],
                    description: response.data['description'],
                    deadline: response.data['deadline'],
                    state: response.data['state']
                });
                service.view_task = task;
            });
            return promise
        };

        service.changeTask = function(task) {
            return $http.post('/api/singledo/' + service.current_id, task);
        };

        service.login = function() {
            window.location.replace('/api/login');
        };

        service.putTask = function(data) {
            return $http.post('/api/multido', data);
        };

        service.deleteTasks = function(id) {
            return $http.delete('/api/singledo/' + id);
        };
    })
})();