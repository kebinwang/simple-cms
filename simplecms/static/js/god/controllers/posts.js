app
  .controller('postsCtrl', function($scope, $timeout, getPosts, catchErr) {
    getPosts()
      .then(function(xhr) {
        $scope.posts = xhr.data.content;
      })
      .catch(catchErr);
  })
