app
  .controller('postCtrl', function($scope, $location, $routeParams, $timeout, $mdDialog, getPost, createPost, editPost, delPost, catchErr, toast) {
    var postId = $routeParams.id;
    var isCreatingNew = !angular.isString(postId);

    $scope.isCreatingNew = isCreatingNew;
    $scope.postId = postId;

    $scope.config = {
      UEDITOR_HOME_URL: '/static/lib/ueditor/',
      topOffset: 0,
      autoFloatEnabled: false,
      autoHeightEnabled: false,
      autotypeset: {
        removeEmptyline: true
      },
      blackList: {},
      whiteList: {
        style: 1,
        script: 1
      },
      serverUrl: '',
      enableAutoSave: false,
      // iframeCssUrl: '/static/css/posts.css',
      wordCount: false, //是否开启字数统计
      maximumWords: 99999, //允许的最大字符数
      initialFrameHeight: 500,
      zIndex: 1,
      filterTxtRules: (function() {
        function transP(node) {
          node.tagName = 'p';
          node.setStyle();
        }

        function transDiv(node) {
          node.tagName = 'div';
          node.setStyle();
        }
        return {
          'div': transDiv,
          'caption': transP,
          'th': transP,
          'tr': transP,
          'h1': transP,
          'h2': transP,
          'h3': transP,
          'h4': transP,
          'h5': transP,
          'h6': transP,
          'td': function(node) {
            //没有内容的td直接删掉
            var txt = !!node.innerText();
            if (txt) {
              node.parentNode.insertAfter(UE.uNode.createText(' &nbsp; &nbsp;'), node);
            }
            node.parentNode.removeChild(node, node.innerText());
          }
        };
      })(),
      toolbars: [
        [
          'fullscreen',
          'source',
          '|',
          'undo',
          'redo',
          '|',
          'bold',
          'italic',
          'underline',
          'strikethrough',
          'removeformat',
          'formatmatch',
          'autotypeset',
          'blockquote',
          'pasteplain',
          '|',
          'forecolor',
          'backcolor',
          'insertorderedlist',
          'insertunorderedlist',
          'cleardoc',
          '|',
          'justifyleft',
          'justifycenter',
          'justifyright',
          'justifyjustify',
          '|',
          'link',
          'unlink',
          '|',
          'imagenone',
          'imageleft',
          'imageright',
          'imagecenter',
          '|',
          'simpleupload',
          'insertimage',
          'emotion',
          'background',
          '|',
          'preview',
          '|',
          'customstyle',
          'paragraph',
          'fontfamily',
          'fontsize'
        ]
      ]
    };

    $scope.createPost = function() {
      if ($scope.loading) {
        return false;
      }
      $scope.loading = true;
      createPost($scope.post)
        .then(function(res) {
          toast('保存成功！');
          $location.path('/posts/' + res.data.content.id);
        })
        .catch(catchErr)
        .finally(function() {
          $scope.loading = false;
        });
    };

    $scope.editPost = function() {
      if ($scope.loading) {
        return false;
      }
      $scope.loading = true;
      editPost(postId, $scope.post)
        .then(function() {
          toast('保存成功！');
        })
        .catch(catchErr)
        .finally(function() {
          $scope.loading = false;
        });
    };
    $scope.delPost = function(ev) {
      // Appending dialog to document.body to cover sidenav in docs app
      var confirm = $mdDialog.confirm()
        .parent(angular.element(document.body))
        .title('确定要删除吗？')
        .content('删除后无法恢复。')
        .ariaLabel('Lucky day')
        .ok('确定删除')
        .cancel('不删除了')
        .targetEvent(ev);

      $mdDialog.show(confirm)
        .then(function() {
          delPost($scope.postId)
            .then(function() {
              toast('已删除！');
              $location.path('/posts');
            });
        });
    };

    $scope.preview = function() {
      var newWindow = open();
      var $newBody = $(newWindow.document.body);
      $newBody
        .append('<link rel="stylesheet" href="http://apps.bdimg.com/libs/typo.css/2.0/typo.min.css"/>')
        .append('<link rel="stylesheet" href="http://simplecms.xiachufang.com/static/css/posts.css"/>')
        .append('<div class="post"><div class="view immutable">' + $scope.post.content + '</div></div>')
        .append('<script src="http://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>')
        .append('<script src="http://simplecms.xiachufang.com/static/js/posts.js"></script>');
    };

    $scope.submit = isCreatingNew ? $scope.createPost : $scope.editPost;

    if (isCreatingNew) {
      $scope.post = {
        author: '下厨房',
        category: 'normal'
      };
    } else {
      getPost(postId)
        .then(function(xhr) {
          $scope.post = xhr.data.content;
        })
        .catch(catchErr);
    }
  });
