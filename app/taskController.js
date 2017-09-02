var vm;
(function() {
    angular.module('todoList').config(function($mdIconProvider) {
        $mdIconProvider.fontSet('md', 'material-icons');
    });

    angular.module('todoList').controller('taskController', function(requestService, $state, $mdDialog) {
        vm = this;
        vm.tasks = [];
        vm.task_name = '';
        vm.task_description = '';
        vm.task_deadline = '';
        vm.view_task = requestService.view_task;
        vm.current_id = requestService.current_id;

        vm.createTask = function(name, description, deadline) {
            task = new Task({
                name: name,
                description: description,
                deadline: deadline
            });
            vm.task_name = '';
            vm.task_description = '';
            vm.task_deadline = '';
            vm.putTask(task);
        };

        vm.ediTask = function(id) {
            requestService.current_id = id;
            $state.go('app.edit_task');
        };

        vm.goTo = function(state) {
            $state.go(state)
        };

        vm.changeTask = function(task) {
            requestService.changeTask(task).then(function() {
                vm.edit_task = {};
            }, function(err) {
                if (err.status == 204) {
                    alert('Tarefa não encontrada');
                    vm.edit_task = {};
                }
            });
        };

        vm.loadTasks = function() {
            requestService.fetchTasks().then(function(response) {
                vm.tasks = response.data;
            }, function(err) {
                if (err.status == 401) {
                    requestService.login();
                };
            });
        };

        vm.viewTask = function(id) {
            requestService.fetchTask(id).then(function() {
                $state.go('app.view_task');
            }, function(err) {});
        };

        vm.putTask = function(data) {
            requestService.putTask(data).then(function(response) {}, function(err) {
                if (err.status == 401) {
                    requestService.login();
                };
            });
        };

        vm.synchronizeTask = function(id) {
            for (var i = vm.tasks.length - 1; i >= 0; i--) {
                if (vm.tasks[i].id == id) {
                    vm.tasks.splice(i, 1);
                };
            };
        };

        vm.deleteTasks = function(id) {
            var confirm = $mdDialog.confirm()
                .clickOutsideToClose(true)
                .title('Confirmar Remoção')
                .textContent('Confirmar a remoção dessa task?')
                .ariaLabel('Confirmar Remoção')
                .targetEvent(event)
                .ok('Sim')
                .cancel('Não');

            var promise = $mdDialog.show(confirm);

            promise.then(function() {
                requestService.deleteTasks(id).then(function(response) {
                    if (response.status === 204) {
                        alert('Essa tarefa não existe');
                    } else {
                        vm.synchronizeTask(id);
                    }
                }, function(err) {
                    if (err.status == 401) {
                    requestService.login();
                    };
                });
            })
        };
    });
})();