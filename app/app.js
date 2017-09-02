(function() {
    var toDo = angular.module('todoList', ['ngMaterial', 'ui.router']);

    toDo.config(function($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');

        $stateProvider
            .state('app', {
                abstract: true,
                views: {
                    'header': {
                        templateUrl: 'header.html',
                        controller: 'designCtrl as ctrl'
                    }
                }
            })
            .state('app.view_tasks', {
                url: '/view/tasks',
                views: {
                    'view_tasks@': {
                        templateUrl: 'tasks.html',
                        controller: 'taskController as vm'
                    }
                }
            })
            .state('app.post_tasks', {
                url: '/post/tasks',
                views: {
                    'post_tasks@': {
                        templateUrl: 'postasks.html',
                        controller: 'taskController as vm'
                    }
                }
            })
            .state('app.home', {
                url: '/',
                views: {
                    'home@': {
                        templateUrl: 'home.html'
                    }
                }
            })
            .state('app.view_task', {
                url: '/view/task',
                views: {
                    'view_task@': {
                        templateUrl: 'task.html',
                        controller: 'taskController as vm'
                    }
                }
            })
            .state('app.edit_task', {
                url: '/edit/task',
                views: {
                    'edit_task@': {
                        templateUrl: 'editasks.html',
                        controller: 'taskController as vm'
                    }
                }
            });
    });
})();