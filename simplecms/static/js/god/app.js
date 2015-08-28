(function(angular) {
  window.app = angular
    .module('god', ['ngRoute', 'ngMaterial', 'ng.ueditor'])
    .config(['$routeProvider', function($routeProvider) {
      $routeProvider
        .when('/login', {
          controller: 'loginCtrl',
          templateUrl: '/static/js/god/template/login.html'
        })
        .when('/posts', {
          controller: 'postsCtrl',
          templateUrl: '/static/js/god/template/posts.html'
        })
        .when('/posts/new', {
          controller: 'postCtrl',
          templateUrl: '/static/js/god/template/post.html'
        })
        .when('/posts/:id', {
          controller: 'postCtrl',
          templateUrl: '/static/js/god/template/post.html'
        })
        .when('/magazine', {
          controller: 'magazineCtrl',
          templateUrl: '/static/js/god/template/magazine.html'
        })
        .otherwise({
          redirectTo: '/posts'
        });
    }])
})(window.angular);
