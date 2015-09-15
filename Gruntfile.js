module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'src/<%= pkg.name %>.js',
        dest: 'build/<%= pkg.name %>.min.js'
      }
    },
    jshint: {
    all: ['Gruntfile.js', 'maker/data/app/**/*.js']
    },
    copy: {
            contrib: {
                files: [
                {
                    expand: true,
                    cwd: 'node_modules/angular/',
                    src: ['angular.js'],
                    dest: 'server/static/js/contrib/'
                },
                {
                    expand: true,
                    cwd: 'node_modules/angular/',
                    src: ['angular.js'],
                    dest: 'maker/data/contrib/'
                },
                {
                    expand: true,
                    cwd: 'node_modules/restangular/dist/',
                    src: ['restangular.js'],
                    dest: 'server/static/js/contrib/'
                },
                {
                    expand: true,
                    cwd: 'node_modules/restangular/dist/',
                    src: ['restangular.js'],
                    dest: 'maker/data/contrib/'
                },
                {
                    expand: true,
                    cwd: 'node_modules/angular-ui-router/release/',
                    src: ['angular-ui-router.js'],
                    dest: 'maker/data/contrib/'
                }
		]
            }
        }
  });

  // Load the plugin that provides the "uglify" task.
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-copy');

  // Default task(s).
  grunt.registerTask('default', ['jshint']);

};