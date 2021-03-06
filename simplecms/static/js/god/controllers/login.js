app
  .controller('loginCtrl', function($scope, $location, login, toast) {
    $scope.user = {
      username: '',
      password: ''
    };
    $scope.login = function() {
      login($scope.user)
        .then(function() {
          $location.path('/');
          toast('登录成功！');
        })
        .catch(function(err) {
          toast('登录失败……' + (err.data.msg || ''));
        });
    };
  })
