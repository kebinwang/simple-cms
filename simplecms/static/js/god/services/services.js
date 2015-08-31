app
  .service('getPosts', function($http) {
    return function() {
      return $http.get('/api/posts');
    };
  })
  .service('getPost', function($http) {
    return function(id) {
      return $http.get('/api/posts/' + id);
    };
  })
  .service('createPost', function($http) {
    return function(post) {
      return $http.post('/api/posts/new', post);
    };
  })
  .service('editPost', function($http) {
    return function(id, post) {
      return $http.post('/api/posts/' + id + '/update', post);
    };
  })
  .service('delPost', function($http) {
    return function(id) {
      return $http.post('/api/posts/' + id + '/delete');
    };
  })
  .service('createMagazine', function($http) {
    return function(magazine) {
      return $http.post('/api/magazines/new', magazine);
    };
  })
  .service('getMagazine', function($http) {
    return function(id) {
      return $http.get('/api/magazines/' + id);
    };
  })
  .service('editMagazine', function($http) {
    return function(id, magazine) {
      return $http.put('/api/magazines/' + id, magazine);
    };
  })
  .service('createMagazinePost', function($http) {
    return function(magazine, post) {
      return $http.post('/api/magazines/' + magazine.id + '/posts/new', post);
    };
  })
  .service('updateMagazinePost', function($http) {
    return function(magazine, post) {
      post = _.pick(
        post,
        'id', 'title', 'desc', 'cover', 'category', 'category_icon', 'post_id'
      );

      return $http.post('/api/magazines/' + magazine.id + '/posts/' + post.id + '/update', post);
    };
  })
  .service('deleteMagazinePost', function($http) {
    return function(magazine, post) {
      return $http.post('/api/magazines/' + magazine.id + '/posts/' + post.id + '/delete');
    };
  })
  .service('login', function($http, $q) {
    return function(user) {
      return $http.post('/api/login', user);
    };
  })
  .service('catchErr', function($http, $location) {
    return function(err) {
      if (err.status === 401) {
        return $location.path('/login');
      }

      try {
        console.error(err);
        alert(err.data.msg);
      } catch (e) {
        console.error(e);
        alert('出错了……');
      }
    };
  })
  .service('toast', ['$mdToast', function($mdToast) {
    return function(text) {
      $mdToast.show(
        $mdToast.simple()
        .content(text)
        .position('bottom left')
        .hideDelay(3000)
      );
    };
  }]);
